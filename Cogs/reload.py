import discord
from discord.ext import commands
from math import ceil

from Tools.Check import Check

class CogReaload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "reload",
                    usage="",
                    description = "Reload the current music.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def skip(self, ctx):

        if not await Check().userInVoiceChannel(ctx): return 
        if not await Check().botInVoiceChannel(ctx): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        
        self.bot.music[ctx.guild.id]["skip"] = {"count": 0, "users": []} # Clean the dict
        self.bot.music[ctx.guild.id]["musics"].insert(0,
            {
            "music": self.bot.music[ctx.guild.id]["nowPlaying"]["music"],
            "requestedBy": self.bot.music[ctx.guild.id]["nowPlaying"]["requestedBy"]
            }
        )
        await ctx.send(f"{ctx.author.mention} Current music reload!")
        client = ctx.guild.voice_client
        client.stop()


def setup(bot):
    bot.add_cog(CogReaload(bot))