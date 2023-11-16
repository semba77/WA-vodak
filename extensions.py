import pymysql

def connect():
    return pymysql.connect(**{
        "host": 'localhost', 
        "port": 3306,
        "user": 'db_user',  
        "password": "heslo", 
        "db":'lodicky', 
        "autocommit": True
        }) 
