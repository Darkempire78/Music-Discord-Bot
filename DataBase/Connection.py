import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

import json


class DBConnection:
    # poolConnection = None

    def __init__(self):
        # if self.poolConnection is None:
        with open("configuration.json", "r") as config:
            data = json.load(config)

        self.MySQLHost = data["MySQLHost"]
        self.MySQLLogin = data["MySQLLogin"]
        self.MySQLPassword = data["MySQLPasword"]
        self.MySQLDatabase = data["MySQLDatabase"]

            # self.poolConnection =  mysql.connector.pooling.MySQLConnectionPool(
            #         pool_name= "betterMusic_pool",
            #         pool_size= 10,
            #         pool_reset_session= False,
            #         host= self.MySQLHost,
            #         database= self.MySQLDatabase,
            #         user= self.MySQLLogin,
            #         password= self.MySQLPassword
            #     )


            # self.poolConnection = mysql.connector.connect(
            #         host=self.MySQLHost,
            #         user=self.MySQLLogin,
            #         passwd=self.MySQLPassword,
            #         database=self.MySQLDatabase,
            #     )

    def getConnection(self):
        # https://pynative.com/python-database-connection-pooling-with-mysql/
        # return self.poolConnection
        return mysql.connector.connect(
                    host=self.MySQLHost,
                    user=self.MySQLLogin,
                    passwd=self.MySQLPassword,
                    database=self.MySQLDatabase,
                )
        # return self.poolConnection.get_connection()