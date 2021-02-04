import discord
from discord.ext import commands


class CogPauseResume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "resume",
                    usage="",
                    description = "Resume the song.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def resume(self, ctx):
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if ctx.guild.voice_client is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm not connected in a voice channel!")
        if ctx.guild.voice_client and self.bot.user.id not in [
            i.id for i in ctx.author.voice.channel.members
        ]: 
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")

        client = ctx.guild.voice_client
        if client.is_paused():
            client.resume()
            return await ctx.channel.send(f"{ctx.author.mention} The song is resumed!")
        await ctx.channel.send(f"{ctx.author.mention} The song is already resumed!")
            


    @commands.command(name = "pause",
                    usage="",
                    description = "Pause the song.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def pause(self, ctx):
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if ctx.guild.voice_client is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm not connected in a voice channel!")
        if ctx.guild.voice_client and self.bot.user.id not in [
            i.id for i in ctx.author.voice.channel.members
        ]: 
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")

        client = ctx.guild.voice_client
        if not client.is_paused():
            client.pause()
            return await ctx.channel.send(f"{ctx.author.mention} The song is paused!")
        await ctx.channel.send(f"{ctx.author.mention} The song is already paused!")


def setup(bot):
    bot.add_cog(CogPauseResume(bot))