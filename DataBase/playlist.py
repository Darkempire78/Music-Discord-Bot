import mysql.connector
import json

class DBPlaylist:

    def __init__(self):
        with open("configuration.json", "r") as config:
            data = json.load(config)

        self.MySQLHost = data["MySQLHost"]
        self.MySQLLogin = data["MySQLLogin"]
        self.MySQLPasword = data["MySQLPasword"]
        self.MySQLDatabase = data["MySQLDatabase"]

    def getConnection(self):
        return mysql.connector.connect(
            host=self.MySQLHost,
            user=self.MySQLLogin,
            passwd=self.MySQLPasword,
            database=self.MySQLDatabase,
        ) 

    def add(self, user, name, title, link):
        """Add a song in a playlist"""
        mydb = self.getConnection()
        mycursor = mydb.cursor()
        mycursor.execute(f"INSERT INTO `playlist` (`user`, `name`, `title`, `link`) VALUES ('{user}', '{name}', '{title}', '{link}');")
        mydb.commit()
        mydb.close()

    def countPlaylistItems(self, user, name):
        """Return the size of a user's playlist"""
        mydb = self.getConnection()
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT COUNT(*) FROM playlist WHERE user = '{user}' AND name = '{name}';")
        result = mycursor.fetchall()
        mydb.close()
        return result[0][0]
    
    def display(self, user, name):
        """Return the content of a user's playlist"""
        mydb = self.getConnection()
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM playlist WHERE user = '{user}' AND name = '{name}';")
        result = mycursor.fetchall()
        mydb.close()
        return result
    
    def remove(self, user, name, link):
        """Remove a song in a playlist"""
        mydb = self.getConnection()
        mycursor = mydb.cursor()
        mycursor.execute(f"DELETE FROM playlist WHERE user='{user}' AND name='{name}' AND link='{link}' LIMIT 1;")
        mydb.commit()
        mydb.close()