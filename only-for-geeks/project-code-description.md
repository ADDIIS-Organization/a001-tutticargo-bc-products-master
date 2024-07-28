
# Importación y Almacenamiento de Datos de Excel a PostgreSQL para app Tutti Cargo

## Resumen
Este script en Python carga datos de un archivo Excel, realiza la transformación de los datos y los inserta en una base de datos PostgreSQL. A través del uso de la biblioteca `pandas` para la manipulación de datos y `psycopg2` para la interacción con PostgreSQL, el código ejemplifica un flujo de trabajo robusto y eficiente para la gestión de datos.

## Dependencias
- Python 3.x
- pandas
- openpyxl
- psycopg2

## Descripción del Código

### Importaciones
```python
import pandas as pd
import psycopg2
from datetime import datetime
```
Se importan las bibliotecas necesarias para la manipulación de datos (`pandas`), la conexión con la base de datos PostgreSQL (`psycopg2`) y la manipulación de fechas y horas (`datetime`).

### Carga de Datos
```python
df = pd.read_excel('../SKU_TOTALES.xlsx')
print(df.columns)
```
El archivo Excel ubicado en `../SKU_TOTALES.xlsx` se carga en un DataFrame de pandas. Se imprimen los nombres de las columnas para verificar que los datos se han cargado correctamente.

### Renombrado de Columnas
```python
df = df.rename(columns={
    'ESTATUS': 'status',
    'SKU': 'sku',
    'CXP GYE NORTE ': 'cxp',
    'DESCRIPCIÓN ': 'name',
    'UXC': 'uxc',
    'CATEGORIA': 'category_name',
    'UNIDAD DE MEDIDA': 'unit_name',
    'Planchas': 'planchas',
    'Numero de planchas': 'number_of_planchas',
    'UBICACIONES PARA SAP': 'warehouse_location'
})
```
Se renombraron las columnas del DataFrame para que coincidan con los nombres de las columnas de la base de datos.

### Función para Insertar Datos en la Base de Datos
```python
def insert_into_db(dataframe):
    try:
        connection = psycopg2.connect(
            user="tutti_cargo_admin",
            password="8Qz$%+W=q17*",
            host="5.161.189.5",
            port="5432",
            database="tutti_cargo"
        )
        cursor = connection.cursor()
        
        # Iniciar una transacción
        connection.autocommit = False

        # Diccionarios para almacenar los mapeos de IDs
        category_id_mapping = {}
        unit_id_mapping = {}
        location_id_mapping = {}

        for index, row in dataframe.iterrows():
            category_name = row['category_name']
            unit_name = row['unit_name']
            warehouse_location = row['warehouse_location']

            # Check if category_name, unit_name, and warehouse_location are not null, NaN, or empty
            if pd.isna(category_name) or pd.isna(unit_name) or pd.isna(warehouse_location):
                print(f"Skipping row {index} due to missing data")
                continue

            if row['status'] == 'INACTIVO':
                print(f"Skipping row {index} due to inactive status")
                continue

            print(f"current category: {category_name}")
            print(f"current unit: {unit_name}")
            print(f"current location: {warehouse_location}")

            # Obtener y almacenar el ID de la categoría si no está ya en el diccionario
            if category_name not in category_id_mapping:
                cursor.execute("SELECT id FROM product_types WHERE name = %s LIMIT 1", (category_name,))
                result = cursor.fetchone()
                category_id_mapping[category_name] = result[0] if result else None

            # Obtener y almacenar el ID de la unidad de medida si no está ya en el diccionario
            if unit_name not in unit_id_mapping:
                cursor.execute("SELECT id FROM units_of_measure WHERE name = %s LIMIT 1", (unit_name,))
                result = cursor.fetchone()
                unit_id_mapping[unit_name] = result[0] if result else None

            # Obtener y almacenar el ID de la ubicación de almacén si no está ya en el diccionario
            if warehouse_location not in location_id_mapping:
                cursor.execute("SELECT id FROM warehouse_locations WHERE code_sap = %s LIMIT 1", (warehouse_location,))
                result = cursor.fetchone()
                location_id_mapping[warehouse_location] = result[0] if result else None
            
            print(f"warehouse location ID: {location_id_mapping[warehouse_location]} and it's suppose to be in location_id_mapping: {warehouse_location}")

            # Insertar en la tabla de productos con manejo de duplicados
            cursor.execute(
                """
                INSERT INTO products (code, cxp, ean, name, uxc, product_types_id, units_of_measure_id, active, warehouse_locations_id, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE, %s, %s, %s)
                ON CONFLICT (warehouse_locations_id) DO UPDATE SET
                code = EXCLUDED.code,
                cxp = EXCLUDED.cxp,
                ean = EXCLUDED.ean,
                name = EXCLUDED.name,
                uxc = EXCLUDED.uxc,
                product_types_id = EXCLUDED.product_types_id,
                units_of_measure_id = EXCLUDED.units_of_measure_id,
                updated_at = EXCLUDED.updated_at
                RETURNING id
                """,
                (
                    row['sku'],
                    row['planchas'] + row['number_of_planchas'],
                    row['sku'],
                    row['name'],
                    row['uxc'],
                    category_id_mapping[category_name],
                    unit_id_mapping[unit_name],
                    location_id_mapping[warehouse_location],
                    datetime.now(),
                    datetime.now()
                )
            )
        
        # Commit de la transacción
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        if connection:
            connection.rollback()  # Revertir la transacción en caso de error
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
```
La función `insert_into_db` toma un DataFrame como entrada y realiza la inserción de los datos en la base de datos PostgreSQL. Utiliza diccionarios para almacenar los mapeos de IDs y maneja duplicados mediante la cláusula `ON CONFLICT`.

### Ejecución de la Función
```python
insert_into_db(df)
```
Finalmente, se llama a la función `insert_into_db` pasando el DataFrame `df` para insertar los datos en la base de datos.
