import discord
from discord.ext import commands

from Tools.Check import Check

from DataBase.Queue import DBQueue

class CogClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "clear",
                    usage="",
                    description = "Clear the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def clear(self, ctx):

        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        
        DBQueue(self.bot.dbConnection).clearFutureTracks(ctx.guild.id)

        await ctx.channel.send(f"{ctx.author.mention} The queue is cleared!")


def setup(bot):
    bot.add_cog(CogClear(bot))