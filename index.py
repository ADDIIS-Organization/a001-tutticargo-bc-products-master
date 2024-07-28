import pandas as pd
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv # type: ignore

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Cargar datos desde un archivo Excel
df = pd.read_excel('../SKU_TOTALES.xlsx')

# Imprimir los nombres de las columnas para verificar
print(df.columns)

# Renombrar columnas si es necesario
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

def insert_into_db(dataframe):
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
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

            # Eliminar el primer carácter si es '0'
            if warehouse_location.startswith('0'):
                warehouse_location = warehouse_location[1:]

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

insert_into_db(df)
