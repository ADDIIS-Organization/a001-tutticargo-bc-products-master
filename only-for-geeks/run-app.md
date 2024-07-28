
# Instrucciones para Iniciar la Aplicación

Este documento proporciona instrucciones paso a paso para configurar y ejecutar la aplicación.

## Paso 1: Crear Variables de Entorno

Primero, necesitamos definir las variables de entorno necesarias para la conexión a la base de datos PostgreSQL. Crea un archivo llamado `.env` en el directorio raíz de tu proyecto y añade las siguientes variables:

```
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=tu_host
DB_PORT=tu_puerto
DB_NAME=tu_nombre_de_base_de_datos
```

Asegúrate de reemplazar `tu_usuario`, `tu_contraseña`, `tu_host`, `tu_puerto` y `tu_nombre_de_base_de_datos` con tus propias credenciales y detalles de la base de datos.

## Paso 2: Instalar Dependencias

La aplicación utiliza varias dependencias que necesitan ser instaladas. Asegúrate de tener `pip` instalado y luego ejecuta el siguiente comando en tu terminal:

```
pip install pandas psycopg2-binary python-dotenv
```

Esto instalará las bibliotecas `pandas`, `psycopg2-binary` y `python-dotenv` necesarias para el funcionamiento del script.

## Paso 3: Cargar Variables de Entorno

El módulo `os` y `dotenv` se utilizan para cargar las variables de entorno definidas en el archivo `.env`. El siguiente código en tu script carga estas variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
```

## Paso 4: Cargar Datos desde un Archivo Excel

Asegúrate de tener un archivo Excel llamado `SKU_TOTALES.xlsx` en el directorio correcto. El siguiente código carga los datos del archivo Excel:

```python
import pandas as pd

df = pd.read_excel('../SKU_TOTALES.xlsx')
```

## Paso 5: Ejecutar la Función `insert_into_db`

Finalmente, ejecuta la función `insert_into_db` para insertar los datos en la base de datos PostgreSQL:

```python
insert_into_db(df)
```

Esta función se encarga de conectar a la base de datos utilizando las variables de entorno, procesar los datos del DataFrame, y realizar las inserciones necesarias en la base de datos.

## Conclusión

Siguiendo estos pasos, deberías poder configurar y ejecutar la aplicación sin problemas. Asegúrate de tener todos los requisitos previos instalados y las variables de entorno correctamente definidas para evitar errores durante la ejecución.
