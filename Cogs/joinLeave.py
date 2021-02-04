import discord
from discord.ext import commands

from Tools.Check import Check


class CogJoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "join",
                    usage="",
                    description = "Add the bot in your voice channel")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def join(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx): return 
        if not await Check().botInVoiceChannel(ctx): return 

        voice = ctx.author.voice
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
        
        if not await Check().userInVoiceChannel(ctx): return 
        if not await Check().botInVoiceChannel(ctx): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        client = ctx.guild.voice_client
        await client.disconnect()
        self.bot.music[ctx.guild.id]["musics"] = []
        self.bot.music[ctx.guild.id]["skip"] = {"count": 0, "users": []}
        self.bot.music[ctx.guild.id]["nowPlaying"] = None
        self.bot.music[ctx.guild.id]["volume"] = 0.5
        await ctx.channel.send(f"{ctx.author.mention} Disconnected!")
        


def setup(bot):
    bot.add_cog(CogJoinLeave(bot))