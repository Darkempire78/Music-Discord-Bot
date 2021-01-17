import discord
from discord.ext import commands

from random import shuffle


class CogClear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "clear",
                    usage="",
                    description = "Clear the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def clear(self, ctx):

        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if ctx.guild.voice_client and self.bot.user.id not in [
            i.id for i in ctx.author.voice.channel.members
        ]:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")
            
        if len(self.bot.music[ctx.guild.id]["musics"]) <= 0:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The queue is empty!")

        self.bot.music[ctx.guild.id]["musics"] = []

        await ctx.channel.send(f"{ctx.author.mention} The queue is cleared!")
       


def setup(bot):
    bot.add_cog(CogClear(bot))