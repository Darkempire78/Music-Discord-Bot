import discord
import psutil
import platform

import datetime

from discord.ext import commands

from DataBase.Queue import DBQueue


class CogStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "stats",
                    usage="",
                    description = "Display the bot's stats")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def stats(self, ctx):

        serverCount = len(self.bot.guilds)
        try:
            userCount = sum(i.member_count for i in self.bot.guilds)
        except:
            userCount = None
        playingServerCount = DBQueue(self.bot.dbConnection).countPlayingItems()
       
        embed=discord.Embed(title=f"{self.bot.user.name}'s stats", description="[**GitHub**](https://github.com/Darkempire78/Music-Discord-Bot)", color=discord.Colour.random())
        embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
        embed.add_field(name="Statistics :", value=f"`Servers : {serverCount}\nUsers : {userCount}`", inline=True)
        embed.add_field(name="Using :", value=f"`Python : v{platform.python_version()}\nDiscord.py : v{discord.__version__}`", inline=True)
        embed.add_field(name="RAM :", value=f"`Used : {psutil.virtual_memory().percent}%`", inline=True)
        embed.add_field(name="Music :", value=f"Playing music on `{playingServerCount}` servers", inline=False)
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogStats(bot))