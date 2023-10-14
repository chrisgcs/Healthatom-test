# Healthatom-test
 
## Descripción
Este repositorio contiene la solución al desafío técnico para el cargo de Data Engineer en HealthAtom

En este repositorio se encuentra el script solicitado y más abajo en este README se encuentran las respuestas a las preguntas

## Herramientas
Para resolver este problema se utilizó el lenguaje Python 3.9.7 y la base de datos MySQL.

Para levantar la base de datos se utilizó el software XAAMP.

## Uso
Para una correcta ejecución es necesario tener una base de datos MySQL en localhost con un usuario de nombre **healthatom_test** y contraseña **HAtest**

Además, es necesario instalar la librería de python que permite la conexión con MySQL

`py -m pip install mysql-connector-python`

Para ejecutar la solución solo es necesario ejecutar el comando

`py solution.py`

Ante lo cual se le solicitará su API key del CMF para poder realizar los request necesarios.

De forma automática se crearán la base de datos **healthatom_test** y posteriormente la tabla **currency_exchange**

Finalmente se realiza la inserción de 2 registros, correspondientes a los valores del Dolar y del Euro en la fecha actual (e.g `(USD, CLP, 900.0, 2023-10-13)` )

## Preguntas y respuestas de la prueba

#### ¿Qué consideraciones tendrías sobre donde guardar estos datos en el datawarehouse?
- La tabla se puede guardar de forma normal en un datawarehouse. No sería necesario el uso de particiones dado que la tabla no llegaría a tener un volumen significativo, ni aun si se realiza un backfill para tener toda la data disponible en la API (creo que hay registros desde el 2009 en adelante)

    Lo que si importa es definir las primary keys. En este caso se define una compuesta por 3 campos para evitar duplicados.

    Además se determina que la tabla debe tener 4 columnas pensando que a futuro puede ser necesario incluir nuevas monedas para las conversiones

#### ¿Cómo disponbilizarías estos datos, junto a la información de venta, para el área comercial?
- La mejor forma de disponibilizar los datos de venta junto a los cambios de moneda es mediante una nueva tabla que tenga ya calculadas las conversiones a Dolar y Euro.

    De esta forma se puede evitar el error humano de cruzar los datos de forma incorercta y el área comercial puede dedicarse a las visualizaciones y el análisis de la información entregada.

#### ¿Sobre qué campos realizarás el cruce con la información de venta? ¿Qué consideraciones hay que tener sobre estos datos?
- Para el cruce con la información de ventas se deberían utilizar 2 campos, el `currency_origin` con el currency del registro de venta y los campos `date` de la tabla `currency_exchange` con la fecha de la transacción. Además es necesario agregar un filtro en la query para seleccionar la moneda a utilizar (USD, Euro). Finalmente es necesario hacer la división entre el valor de la venta y `rate` para obtener el monto en USD o Euro

    La consideración a tener con estos datos es que es muy importante siempre agregar la fecha para que la transformación se realice con el valor que tenía el dolar y el euro al momento de la transacción.

#### ¿Cuál sería tu estrategia para actualizar estos datos en el tiempo?
- Para actualizar los datos la opción más viable es ejecutar el script de forma diaria y de esta forma se cree nuevos registros en la tabla.

    Para evitar duplicados, la creación de la tabla define como llave primaria los campos `currency_origin`, `currency_destiny` y `date`