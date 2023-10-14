import requests
import mysql.connector
import json

import requests
import json

class Api_Connector:
    # Api_Connector class provides methods to connect to a currency exchange API and retrieve exchange rates.

    """
    Attributes:
        url (str): The base URL of the API endpoint.
        currency_dict (dict): A dictionary mapping currency codes to their corresponding API resource names.
        connector_name (str): Name of the API connector.
        apikey (str): API key for authentication.
    """

    url = "https://api.sbif.cl/api-sbifv3/recursos_api/{currency}?apikey={apikey}&formato=json"
    currency_dict = {
        "USD": "dolar",
        "EUR": "euro"
    }


    """
    Constructor method to initialize the Api_Connector object.
    Args:
            connector_name (str): Name of the API connector.
            api_key (str): API key for authentication.
    """
    def __init__(self, connector_name, api_key):
        self.connector_name = connector_name
        self.apikey = api_key

    """
    Method to retrieve exchange rate data for a specific currency.
    Args:
            currency (str): Currency code (e.g., "USD", "EUR"). Posibility to extend to other currencies in future
    Returns:
            requests.Response: Response object containing the API response.
    """
    def get(self, currency):
        final_url = self.url.format(currency=self.currency_dict[currency], apikey=self.apikey)
        return requests.get(final_url)


    """
    Method to unpack and format the retrieved exchange rate data.
    Args:
            currency (str): Currency code (e.g., "USD", "EUR"). Posibility to extend to other currencies in future
    Returns:
            list: A list of tuples containing unpacked exchange rate data (currency_from, currency_to, rate, date).
    """
    def unpack_values(self, currency):
        values_to_insert = []
        response = self.get(currency)
        currency_key = "Dolares" if currency == "USD" else "Euros"
        packed_values = json.loads(response.content)[currency_key]
        for values in packed_values:
            rate = values["Valor"].replace(',', '.')
            date = values["Fecha"]
            values_to_insert.append((currency, "CLP", rate, date))
        return values_to_insert


class MySQL_Connector:
    # MySQL_Connector class provides methods to connect to a MySQL database and perform operations like
    # creating a database, creating a table, and inserting data into the table.

    """
    Attributes:
        host (str): Hostname of the MySQL server.
        user (str): Username for authentication.
        password (str): Password for authentication.
    """


    """
        Initializes the MySQL_Connector object with the provided host, user, and password.

        Args:
            host (str): Hostname of the MySQL server.
            user (str): Username for authentication.
            password (str): Password for authentication.
    """
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password


    """
        Establishes a connection to the MySQL database.

        Args:
            db_name (str, optional): Name of the database to connect to. Defaults to an empty string.
    """
    def get_conn(self, db_name=''):
        try:
            self.conn = mysql.connector.connect(
                        host =self.host, 
                        user = self.user,
                        password = self.password, 
                        database = db_name
                    )
        except:
            print(f"db {db_name} does not exist. Connecting to MySQL")
            self.conn = mysql.connector.connect(
                        host =self.host, 
                        user = self.user,
                        password = self.password 
                    )

    """
        Creates a new database if it does not already exist.

        Args:
            db_name (str): Name of the database to be created.
    """
    def create_db(self, db_name):
        create_flag = True
        db_cursor = self.conn.cursor()
        db_cursor.execute("SHOW DATABASES")
        for db in db_cursor:
            if db[0] == db_name:
                print("db already exists")
                create_flag = False
        if create_flag:
            db_cursor.execute(f"CREATE DATABASE {db_name}")
        db_cursor.close()


    """
        Creates a table 'currency_exchange' in the connected database if it does not already exist.
    """
    def create_table(self):
        create_flag = True
        db_cursor = self.conn.cursor()
        db_cursor.execute("SHOW TABLES")
        for table in db_cursor:
            if table[0] == "currency_exchange":
                print("table already exists")
                create_flag = False
        if create_flag:
            db_cursor.execute("CREATE TABLE currency_exchange (currency_origin VARCHAR(10), currency_destiny VARCHAR(10), rate FLOAT, date DATE, PRIMARY KEY (currency_origin,currency_destiny,date))")
            self.conn.commit()
        db_cursor.close()


    """
        Inserts data into the 'currency_exchange' table.

        Args:
            values_list (list): List of tuples containing data to be inserted into the table. List used to add posibility of backfill
    """
    def insert_into(self, values_list):
        INSERT_STATEMENT = "INSERT INTO currency_exchange (currency_origin , currency_destiny, rate, date) VALUES (%s,%s,%s,%s)"
        db_cursor = self.conn.cursor()
        for values in values_list:
            try:
                db_cursor.execute(INSERT_STATEMENT, values)
                print("correctly inserted ", values)
            except mysql.connector.IntegrityError as e:
                print("ERROR : ", e)
        self.conn.commit()
        db_cursor.close()

    

print("Por favor, ingresar apikey:")
apikey = input()
CMF = Api_Connector(connector_name = 'CMF', api_key = apikey)

mysqlconn = MySQL_Connector(host="localhost",
                            user="healthatom_test",
                            password="HAtest"
            )

#first attempt to connect fails to connect to db because it does not exist. It connects directly to MySQL
mysqlconn.get_conn(db_name = "healthatom_test") 

mysqlconn.create_db("healthatom_test")

mysqlconn.create_table()

mysqlconn.get_conn(db_name = "healthatom_test") #second attempt works because db was created

mysqlconn.insert_into(CMF.unpack_values("USD"))
mysqlconn.insert_into(CMF.unpack_values("EUR"))
