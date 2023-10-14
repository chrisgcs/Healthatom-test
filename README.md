# Healthatom-test
 
## Descripcion
Este repositorio contiene la solucion al desafio tecnico para el cargo de Data Engineer en HealthAtom

En este repositorio se encuentr el script solicitado y mas abajo en este README se encuentran las respuestas a las preguntas

## Herramientas
Para resolver este problema se utilizo el lenguaje Python 3.9.7 y la base de datos MySQL.

Para levantar la base de datos se utilizo el software XAAMP.

## Uso
Para una correcta ejecucion es necesario tener una base de datos MySQL en localhost con un usuario de nombre **healthatom_test** y contraseña **HAtest**

Ademas, es necesario instalar la libreria de python que permite la conexion con MySQL

`py -m pip install mysql-connector-python`

Para ejecutar la solucion solo es necesario ejecutar el comando

`py solution.py`

Ante lo cual se le solicitará su API key del CMF para poder realizar los request necesarios.

De forma automatica se crearan la base de datos **healthatom_test** y posteriormente la tabla **currency_exchange**

Finalmente se realiza la insercion de 2 registros, correspondientes a los valores del Dolar y del Euro en la fecha actual (e.g `(USD, CLP, 900.0, 2023-10-13)` )

## Preguntas y respuestas de la prueba

#### ¿Qué consideraciones tendrías sobre donde guardar estos datos en el datawarehouse?


#### ¿Cómo disponbilizarías estos datos, junto a la información de venta, para el área comercial?
- La mejor forma de disponibilizar los datos de venta junto a los cambios de moneda es mediante una nueva tabla que tenga ya calculadas las conversiones a Dolar y Euro.

    De esta forma se puede evitar el error humano de cruzar los datos de forma erronea y el area comercial puede dedicarse a las visualizaciones y el analisis de la informacion entregada.

#### ¿Sobre qué campos realizarás el cruce con la información de venta? ¿Qué consideraciones hay que tener sobre estos datos?
- Para el cruce con la informacion de ventas se deberian utilizar 2 campos, el `currency_origin` con el currency del registro de venta y los campos `date` de la tabla `currency_exchange` con la fecha de la transacción. Ademas es necesario agregar un filtro en la query para seleccionar la moneda a utilizar (USD, Euro). Finalmente es necesario hacer la division entre el valor de la venta y `rate` para obtener el monto en USD o Euro

    La consideracion a tener con estos datos es que es muy importante siempre agregar la fecha para que la transformacion se realice con el valor que tenia el dolar y el euro al momento de la transacción.

#### ¿Cuál sería tu estrategia para actualizar estos datos en el tiempo?
- Para actualizar los datos la opcion mas viable es ejecutar el script de forma diaria y de esta forma se cree nuevos registros en la tabla.

    Para evitar duplicados, la creacion de la tabla define como llave primaria los campos `currency_origin`, `currency_destiny` y `date`