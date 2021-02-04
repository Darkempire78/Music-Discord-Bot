import discord
from discord.ext import commands

from Tools.Check import Check


class CogClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "clear",
                    usage="",
                    description = "Clear the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def clear(self, ctx):

        if not await Check().userInVoiceChannel(ctx): return 
        if not await Check().botInVoiceChannel(ctx): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        if not await Check().queueEmpty(ctx, self.bot): return 

        self.bot.music[ctx.guild.id]["musics"] = []

        await ctx.channel.send(f"{ctx.author.mention} The queue is cleared!")
       


def setup(bot):
    bot.add_cog(CogClear(bot))