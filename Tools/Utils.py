import discord

class Utils:

    async def generateGuildDictionnary(self, bot, guilds):
        for i in guilds:
            bot.music[i.id] = {
                "volume": 0.5,
                "musics": [],
                "skip": {
                    "count": 0,
                    "users": []
                },
                "nowPlaying": None,
                "loop": False,
                "loopQueue": False
            }