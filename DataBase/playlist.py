import mysql.connector

from DataBase.Connection import DBConnection

import datetime

class DBPlaylist:

    def __init__(self):
        self.connectionPool  = DBConnection().getConnection()

    def add(self, user, name, title, link):
        """Add a song in a playlist"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `playlist` (`user`, `name`, `title`, `link`) VALUES (%s, %s, %s, %s);"
        val = (str(user), name, title, link)
        mycursor.execute(query, val)
        mydb.commit()
        

    def countPlaylistItems(self, user, name):
        """Return the size of a user's playlist"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT COUNT(*) FROM playlist WHERE user = %s AND name = %s;"
        val = (str(user), name)
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result[0][0]
    
    def display(self, user, name):
        """Return the content of a user's playlist"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM playlist WHERE user = %s AND name = %s;"
        val = (str(user), name)
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result
    
    def remove(self, user, name, link):
        """Remove a song in a playlist"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM playlist WHERE user=%s AND name=%s AND link=%s LIMIT 1;"
        val = (str(user), name, link)
        mycursor.execute(query, val)
        mydb.commit()
        