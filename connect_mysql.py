import mysql.connector
from mysql.connector import Error
import variables

def connect_database():
    try:
        conn = mysql.connector.connect(
            database = "library_management_system",
            user = "root",
            password = variables.password,
            host = "localhost"
          )
        
        if conn.is_connected():
          print('\33[96m', "Connection to MySQL is successful", "\033[0m")
          return conn
    
    except Error as e:
        print("Error while connecting to MySQL", e)
