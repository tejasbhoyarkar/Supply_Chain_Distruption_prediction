import mysql.connector

def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tejas@1234",
        database="supply_chain_db"
    )

    return connection   


    

    