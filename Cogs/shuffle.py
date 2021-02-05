import discord
from discord.ext import commands

from random import shuffle

from Tools.Check import Check

class CogShuffle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "shuffle",
                    usage="",
                    description = "Shuffle the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def shuffle(self, ctx):

        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        if not await Check().queueEmpty(ctx, self.bot): return 

        shuffle(self.bot.music[ctx.guild.id]["musics"])

        await ctx.channel.send(f"{ctx.author.mention} The queue is shuffled!")
       


def setup(bot):
    bot.add_cog(CogShuffle(bot))