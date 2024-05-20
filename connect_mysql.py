import mysql.connector
from mysql.connector import Error

def connect_database():
  """ Connect to MySQL database """
  try:
    conn = mysql.connector.connect(
      database = "library_management_system",
      user = "root",
      password = "f1360114408",
      host = "localhost"
    )
    
    if conn.is_connected():
      print('\33[32m', "Connection to MySQL is successful", "\033[0m")
      return conn
    
    
  except Error as e:
    print("Error while connecting to MySQL", e)
    
