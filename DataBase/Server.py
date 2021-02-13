import mysql.connector

from DataBase.Connection import DBConnection

class DBServer:

    def __init__(self):
        self.connectionPool  = DBConnection().getConnection()

    def add(self, server, prefix, loop, loopQueue, djRole):
        """Add a server"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `server` (`server`, `prefix`, `loop`, `loopQueue`, `djRole`) VALUES (%s, %s, %s, %s, %s);"
        val = (str(server), prefix, loop, loopQueue, djRole)
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def remove(self, server):
        """Remove a server"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM `server` WHERE `server`= %s LIMIT 1;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        

    def clearMusicParameters(self, server, loop, loopQueue):
        """Set the track to isPLaying"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"UPDATE `server` SET `loop`= %s, loopQueue= %s WHERE `server` = %s;"
        val = (loop, loopQueue, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def display(self):
        """Return the content of servers"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM `server`;"
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result
    
    def displayServer(self, server):
        """Return the content of servers"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM `server` WHERE `server`= %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result[0]
    
    def updateLoop(self, server, loop):
        """Set the track to isPLaying"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"UPDATE `server` SET `loop`= %s WHERE `server` = %s;"
        val = (loop, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def updateLoopQueue(self, server, loopQueue):
        """Set the track to isPLaying"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"UPDATE `server` SET `loopQueue`= %s WHERE `server` = %s;"
        val = (loopQueue, str(server))
        mycursor.execute(query, val)
        mydb.commit()
        