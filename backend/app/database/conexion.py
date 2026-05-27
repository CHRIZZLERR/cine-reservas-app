import mysql.connector

def obtener_conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="chris123",
        database="cine_reservas"
    )
    return conexion