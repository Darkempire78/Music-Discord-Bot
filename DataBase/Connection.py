import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

import json


class DBConnection:
    def __init__(self):
        with open("configuration.json", "r") as config:
            data = json.load(config)

        self.MySQLHost = data["MySQLHost"]
        self.MySQLLogin = data["MySQLLogin"]
        self.MySQLPasword = data["MySQLPasword"]
        self.MySQLDatabase = data["MySQLDatabase"]
    
    def getConnection(self):
        # https://pynative.com/python-database-connection-pooling-with-mysql/
        return mysql.connector.pooling.MySQLConnectionPool(
            pool_name= "betterMusic_pool",
            pool_size= 10,
            pool_reset_session= True,
            host= self.MySQLHost,
            database= self.MySQLDatabase,
            user= self.MySQLLogin,
            password= self.MySQLPasword
        )

        # return mysql.connector.connect(
        #     host=self.MySQLHost,
        #     user=self.MySQLLogin,
        #     passwd=self.MySQLPasword,
        #     database=self.MySQLDatabase,
        # )