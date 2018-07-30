import pyodbc

serverName = "ee6ncfdxy8.database.windows.net"
userId = "azuredbfordapper"
password = "qrGejCjw7JJZkJ"
database = "Dapper"

conn = pyodbc.connect(DRIVER="{SQL Server}", SERVER=serverName,DATABASE=database,UID=userId,PWD=password)

cursor = conn.cursor()
cursor.execute("SELECT * FROM PRICE")


for row in cursor:
    print(row)

