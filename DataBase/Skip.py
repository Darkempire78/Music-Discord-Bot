import mysql.connector

from DataBase.Connection import DBConnection

class DBSkip:

    def __init__(self):
        self.connectionPool  = DBConnection().getConnection()

    def add(self, server, user):
        """Add a skip"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `skip` (`server`, `user`) VALUES (%s, %s);"
        val = (str(server), str(user))
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def clear(self, server):
        """clear the list of skip"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM `skip` WHERE `server`= %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        

    def displayUsers(self, server):
        """Return the list of each user"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT `user` FROM `skip` WHERE `server`= %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall() 
        return result

    