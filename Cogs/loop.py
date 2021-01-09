import discord
from discord.ext import commands


class CogLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "loop",
                    usage="",
                    description = "Enable or disable the loop mode.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def loop(self, ctx):
        
        if ctx.author.voice is None:
            return await ctx.channel.send(f"{ctx.author.mention} You are not connected in a voice channel!")
        if self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]: 
            return await ctx.channel.send(f"{ctx.author.mention} You are not connected in the same voice channel that the bot!")

        if self.bot.music[ctx.guild.id]["loop"]:
            self.bot.music[ctx.guild.id]["loop"] = False
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was disabled!")
        else:
            self.bot.music[ctx.guild.id]["loop"] = True
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was enabled!")


def setup(bot):
    bot.add_cog(CogLoop(bot))