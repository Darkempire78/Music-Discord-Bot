import discord
from discord.ext import commands


class CogJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "join",
                    usage="",
                    description = "Add the bot in your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def join(self, ctx):
        voice = ctx.author.voice
        if ctx.guild.voice_client:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm already connected in a voice channel!")
        if voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        await voice.channel.connect()
        self.bot.music[ctx.guild.id]["musics"] = []
        self.bot.music[ctx.guild.id]["skip"] = {"count": 0, "users": []}
        self.bot.music[ctx.guild.id]["nowPlaying"] = None
        self.bot.music[ctx.guild.id]["volume"] = 0.5
        await ctx.channel.send(f"{ctx.author.mention} Connected!")

    @commands.command(name = "leave",
                    usage="",
                    description = "Leave the bot of your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def leave(self, ctx):
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if ctx.guild.voice_client is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm not connected in a voice channel!")

        # If user is not in the same voice channel that the bot
        if ctx.guild.voice_client and self.bot.user.id not in [
            i.id for i in ctx.author.voice.channel.members
        ]:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")
        
        client = ctx.guild.voice_client
        await client.disconnect()
        self.bot.music[ctx.guild.id]["musics"] = []
        self.bot.music[ctx.guild.id]["skip"] = {"count": 0, "users": []}
        self.bot.music[ctx.guild.id]["nowPlaying"] = None
        self.bot.music[ctx.guild.id]["volume"] = 0.5
        await ctx.channel.send(f"{ctx.author.mention} Disconnected!")
        


def setup(bot):
    bot.add_cog(CogJoinLeave(bot))