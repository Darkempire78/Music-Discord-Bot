import discord
from discord.ext import commands


class CogLoopLoopQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "loop",
                    usage="",
                    description = "Enable or disable the loop mode.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def loop(self, ctx):
        
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if ctx.guild.voice_client and self.bot.user.id not in [
            i.id for i in ctx.author.voice.channel.members
        ]: 
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")

        if self.bot.music[ctx.guild.id]["loop"]:
            self.bot.music[ctx.guild.id]["loop"] = False
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was disabled!")
        else:
            self.bot.music[ctx.guild.id]["loop"] = True
            await ctx.channel.send(f"{ctx.author.mention} The loop mode was enabled!")

    @commands.command(name = "loopqueue",
                    aliases=["lq"],
                    usage="",
                    description = "Enable or disable the loop queue mode.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def loopqueue(self, ctx):
        
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if ctx.guild.voice_client and self.bot.user.id not in [
            i.id for i in ctx.author.voice.channel.members
        ]: 
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")

        if self.bot.music[ctx.guild.id]["loopQueue"]:
            self.bot.music[ctx.guild.id]["loopQueue"] = False
            await ctx.channel.send(f"{ctx.author.mention} The loop queue mode was disabled!")
        else:
            self.bot.music[ctx.guild.id]["loopQueue"] = True
            await ctx.channel.send(f"{ctx.author.mention} The loop queue mode was enabled!")


def setup(bot):
    bot.add_cog(CogLoopLoopQueue(bot))