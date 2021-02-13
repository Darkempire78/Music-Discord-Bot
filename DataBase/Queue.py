import mysql.connector

from DataBase.Connection import DBConnection

class DBQueue:

    def __init__(self):
        self.connectionPool  = DBConnection().getConnection()

    def add(self, server, isPlaying, requester, textChannel, track, title, duration, index):
        """Add a song in the queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"INSERT INTO `queue` (`server`, `isPlaying`, `requester`, `textChannel`, `track`, `title`, `duration`, `index`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
        val = (str(server), isPlaying, requester, str(textChannel), track, title, duration, index)
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def remove(self, server, index):
        """Remove the song from the queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM queue WHERE `server`= %s AND `index`= %s;"
        val = (str(server), index)
        mycursor.execute(query, val)
        mydb.commit()
        

    def removeFormer(self, server):
        """Remove the former song (index = 0) from the queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM queue WHERE `server`= %s AND `index`= 0;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        

    def updatePlayingToFormer(self, server):
        """update the playing track to former track"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"UPDATE queue SET isPlaying= false, `index`= 0 WHERE `server` = %s AND `isPlaying`= true LIMIT 1;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def updateRemoveOneToEach(self, server, indexFrom, indexTo):
        """remove 1 to each track between 2 indexes"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"UPDATE queue SET `index`= `index`-1 WHERE `server` = %s AND `index`> %s AND `index`<= %s;"
        val = (str(server), indexFrom, indexTo)
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def updateAddOneToEach(self, server, indexFrom, indexTo):
        """add 1 to each track between 2 indexes"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"UPDATE queue SET `index`= `index`+1 WHERE `server` = %s AND `index`>= %s AND `index`< %s;"
        val = (str(server), indexTo, indexFrom)
        mycursor.execute(query, val)
        mydb.commit()
        
    
    def getFutureIndex(self, server):
        """Return the max index of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT MAX(`index`) FROM queue WHERE `server`= %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result[0][0]

    def getNextIndex(self, server):
        """Return the next index of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT MIN(`index`) FROM queue WHERE `server`= %s AND isPlaying= false AND `index`!= 0;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result[0][0]
    
    def getIndexFromFakeIndex(self, server, index):
        """Return the real index from a fake index (1 to x)"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT `index` FROM queue WHERE `server`= %s AND isPlaying= false AND `index`!= 0 ORDER BY `index` ASC LIMIT 1 OFFSET %s;"
        val = (str(server), index)
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result[0][0]
    
    def getCurrentSong(self, server):
        """Return the playing song of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE `server`= %s AND isPlaying= true;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result[0]

    def getNextSong(self, server):
        """Return the next song of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE `server`= %s AND isPlaying= false AND `index`!= 0 ORDER BY `index` ASC LIMIT 1;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        if len(result) == 0:
            return None
        return result[0]

    def countQueueItems(self, server):
        """Return the size of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT COUNT(*) FROM queue WHERE `server` = %s AND `index`!= 0;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result[0][0]
    
    def countPlayingItems(self):
        """Return the size of a server's queue playing track"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT COUNT(*) FROM queue WHERE isPlaying= true;"
        mycursor.execute(query)
        result = mycursor.fetchall()
        return result[0][0]
    
    def queueSizeAndDuration(self, server):
        """Return the queue duration of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT SUM(duration), COUNT(*) FROM queue WHERE `server` = %s AND isPlaying= false AND `index`!= 0;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        if result[0][0] is None:
            return None
        return result[0]
    
    def setIsPlaying(self, server, index):
        """Set the track to isPLaying"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"UPDATE queue SET isPlaying= true WHERE `server` = %s AND `index`= %s LIMIT 1;"
        val = (str(server), index)
        mycursor.execute(query, val)
        mydb.commit()
        

    def clear(self, server):
        """Clear all the queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM queue WHERE `server` = %s;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        

    def clearFutureTracks(self, server):
        """Clear all the queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"DELETE FROM queue WHERE `server` = %s AND `isPlaying`= false AND `index`!= 0;"
        val = (str(server), )
        mycursor.execute(query, val)
        mydb.commit()
        

    def display(self, server):
        """Return the content of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE `server` = %s AND isPlaying = false AND `index`!= 0 ORDER BY `index` ASC;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        return result
    
    def displayFormer(self, server):
        """Return the content of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE `server`= %s AND `index`= 0 LIMIT 1;"
        val = (str(server), )
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        if len(result) == 0:
            return None
        return result[0]
    
    def displaySpecific(self, server, index):
        """Return the content of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE `server`= %s AND `index`= %s LIMIT 1;"
        val = (str(server), index)
        mycursor.execute(query, val)
        result = mycursor.fetchall()
        if len(result) == 0:
            return None
        return result[0]

    def displayAllPlaying(self):
        """Return the content of a server's queue"""
        mydb = self.connectionPool.get_connection()
        mycursor = mydb.cursor()
        query = f"SELECT * FROM queue WHERE `isPlaying`= true;"
        mycursor.execute(query)
        result = mycursor.fetchall()
        if len(result) == 0:
            return None
        return result