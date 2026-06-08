import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


def obtener_conexion():
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    database = os.getenv("DB_NAME", "cine_reservas")

    conexion = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl_disabled=False,
    )

    return conexion