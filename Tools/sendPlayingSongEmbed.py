import discord

from Tools.Utils import Utils

from DataBase.Queue import DBQueue
from DataBase.Server import DBServer

async def sendPlayingSongEmbed(self, channel, track): 

    player = self.bot.wavelink.get_player(channel.guild.id)
    
    # Volume
    volume = player.volume
    
    # Track duration
    trackDuration = await Utils().durationFormat(track.duration)
    
    # Queue size and duration
    queueSizeAndDuration = DBQueue(self.bot.dbConnection).queueSizeAndDuration(channel.guild.id)
    if queueSizeAndDuration:
        queueDuration = int(queueSizeAndDuration[0])
        queueDuration = await Utils().durationFormat(queueDuration)
        queueSize = queueSizeAndDuration[1]
    else:
        queueSize = 0
        queueDuration = "00:00"
    
    # Title
    trackTitle = track.title.replace("*", "\\*")

    # Loop and LoopQueue
    isLoop = str(DBServer(self.bot.dbConnection).displayServer(channel.guild.id)[2])
    isLoopQueue = str(DBServer(self.bot.dbConnection).displayServer(channel.guild.id)[3])


    # Embed 
    embed=discord.Embed(title="Playing Song :", description=f"**[{trackTitle}]({track.uri})**", color=discord.Colour.random())
    if track.thumb:
        embed.set_thumbnail(url=track.thumb)
    embed.add_field(name="Requested by :", value=f"`{track.requester}`", inline=True)
    embed.add_field(name="Duration :", value=f"`{trackDuration}`", inline=True)
    embed.add_field(name="Volume :", value=f"`{volume} %`", inline=True)
    embed.add_field(name="Loop :", value=isLoop.replace("1", f"{self.bot.emojiList.true}").replace("0", f"{self.bot.emojiList.false}"), inline=True)
    embed.add_field(name="Loop queue :", value=isLoopQueue.replace("1", f"{self.bot.emojiList.true}").replace("0", f"{self.bot.emojiList.false}"), inline=True)
    embed.add_field(name="Lyrics :", value=f"`{self.bot.command_prefix}lyrics`", inline=True)
    embed.add_field(name="Queue :", value=f"`{queueSize} song(s) ({queueDuration})`", inline=True)
    embed.add_field(name="DJ Role :", value=f"`@role`", inline=True)
    await channel.send(embed=embed)