# Tutti Cargo Data Importer

## Descripción

Este proyecto es un script en Python diseñado para cargar datos desde un archivo Excel, transformarlos y almacenarlos en una base de datos PostgreSQL. Utiliza `pandas` para la manipulación de datos y `psycopg2` para la conexión y operación con PostgreSQL.

## Requisitos

- Python 3.x
- `pandas`
- `openpyxl`
- `psycopg2`
- `python-dotenv`

## Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/tutti_cargo_data_importer.git
cd tutti_cargo_data_importer
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
```

3. Instala las dependencias:

```bash
pip install pandas openpyxl psycopg2-binary python-dotenv
```

    3.1. pandas: Para la manipulación de datos.
    3.2. openpyxl: Para la lectura de archivos Excel.
    3.3. psycopg2-binary: Para la conexión con PostgreSQL.
    3.4. python-dotenv: Para la carga de variables de entorno desde un archivo `.env`.

## Configuración

1. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```plaintext
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=tu_host
DB_PORT=tu_puerto
DB_NAME=tu_nombre_de_base_de_datos
```

Reemplaza los valores con los de tu base de datos PostgreSQL.

## Uso

1. Asegúrate de tener el archivo Excel llamado SKU_TOTALES.xlsx en el directorio correcto. (Puede ser proveido por el administrador del sistema, escribe a nicolaspicon98@gmail.com)

2. Ejecuta el script:

```bash
python index.py
```

Este script cargará los datos del archivo Excel, los transformará según sea necesario y los insertará en la base de datos PostgreSQL especificada.

## Licencia

Este proyecto está bajo la licencia MIT. Para más información, ver el archivo [LICENSE](LICENSE).

## Only For Geeks

You may go to the only-for-geeks folder to see the code that was used to create the script.
    - (The project Code description)[only-for-geeks/project-code-description.md]
    - (The project Code)[only-for-geeks/project-code.py]