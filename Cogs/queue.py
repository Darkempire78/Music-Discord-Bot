import discord
from discord.ext import commands

from Tools.Check import Check
from Tools.Utils import Utils

from DataBase.Queue import DBQueue

class CogQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "queue",
                    usage="",
                    description = "Display the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def queue(self, ctx):

        isFirstMessage = True
        message = ""

        tracks = DBQueue(self.bot.dbConnection).display(ctx.guild.id)

        if len(tracks) == 0:
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The queue is empty!")
        
        for number, track in enumerate(tracks, start=1):
            
            trackDuration = await Utils().durationFormat(track[6])
            trackTitle = track[5].replace("*", "\\*")
            trackUrl = track[4]

            message += f"**{number}) [{trackTitle}]({trackUrl})** ({trackDuration})\n"
            if len(message) > 1800:
                
                if isFirstMessage:
                    embedTitle = "Queue"
                    isFirstMessage = False
                else:
                    embedTitle = ""

                embed=discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
                embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                message = ""
        if len(message) > 0:
            embed=discord.Embed(title="", description=message, color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(CogQueue(bot))