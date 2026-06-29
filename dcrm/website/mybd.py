import mysql.connector # type: ignore
dataBase =mysql.connector.connect(
    host='localhost',
    user='root',
    passwd=''
)
# preparacion de un cursor  object

cursorObject =dataBase.cursor()
#crear la base de datos 
cursorObject.execute("CREATE DATABASE clientes")

print("todo esta bien ya emigro")