import discord
from discord.ext import commands

from Tools.Check import Check

from DataBase.Server import DBServer

class CogLoopLoopQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "loop",
                    usage="",
                    description = "Enable or disable the loop mode.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def loop(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        isLoop = DBServer(self.bot.dbConnection).displayServer(ctx.guild.id)[2]

        if isLoop == 1:
            DBServer(self.bot.dbConnection).updateLoop(ctx.guild.id, False)
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was disabled!")
        else:
            DBServer(self.bot.dbConnection).updateLoop(ctx.guild.id, True)
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was enabled!")


    @commands.command(name = "loopqueue",
                    aliases=["lq"],
                    usage="",
                    description = "Enable or disable the loop queue mode.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def loopqueue(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        
        isLoopQueue = DBServer(self.bot.dbConnection).displayServer(ctx.guild.id)[3]

        if isLoopQueue == 1:
            DBServer(self.bot.dbConnection).updateLoopQueue(ctx.guild.id, False)
            await ctx.channel.send(f"{ctx.author.mention} The loop queue mode was disabled!")
        else:
            DBServer(self.bot.dbConnection).updateLoopQueue(ctx.guild.id, True)
            await ctx.channel.send(f"{ctx.author.mention} The loop queue mode was enabled!")


def setup(bot):
    bot.add_cog(CogLoopLoopQueue(bot))