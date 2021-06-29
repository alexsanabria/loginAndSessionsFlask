import mysql.connector
from mysql.connector import Error

class Conexion:

    def __init__(self):
        pass

    def conectar():
        conexion=None #Inicializar la conexion como valor vacio
        try:          # Intentar realizar la conexión 
            conexion = mysql.connector.connect(

                host='localhost',
                user='root',
                passwd='',
                database='Login')
            print('Conexión satisfactoria')
        except Error as e: 
            print("Error en la conexion")
        return conexion
    

    #   LEER INFORMACION DE LA BASE DE DATOS
    def leer_datos(conexion, query): #Recibe los datos de Conexion y la consulta sql
        cursor=conexion.cursor(dictionary=True) # Crear el cursor
        result=None # inicializar la variable para guardar el resultado de la consulta
        try: # Ejecutar la consulta
            cursor.execute(query)
            result=cursor.fetchall()# Guardar los datos recibidos de la DB en la variable result
            return result # Devuelve el valor de la  consulta a la instanciadonde se invocó esta función
        except Error as e: # Mostrar errores en caso que se presenten
            print("Se Presentó un error", e)

    # ESCRIBIR INFORMACION EN LA BASE DE DATOS
    def escribir_datos(conexion, query): #Recibe los datos de Conexion y la consulta sql
        cursor=conexion.cursor() # Crear el cursor
        cursor.execute(query)   # Ejecutar la consulta
        conexion.commit()   # Confirmar la consulta
        conexion.close()    # Cerrar la conexion

    # BORRAR INFORMACION DE LA BASE DE DATOS
    def borrar(conexion, query): #Recibe los datos de Conexion y la consulta sql
        cursor=conexion.cursor() # Crear el cursor
        cursor.execute(query)  # Ejecutar la consulta
        conexion.commit() # Confirmar la consulta
        conexion.close()  # Cerrar la conexion


