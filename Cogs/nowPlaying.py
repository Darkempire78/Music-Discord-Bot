import discord
from discord.ext import commands

from Tools.sendPlayingSongEmbed import sendPlayingSongEmbed

class CogNowPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "nowplaying",
                    aliases=["np", "now", "playing"],
                    usage="",
                    description = "Display the current song!")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def nowplaying(self, ctx):
        if self.bot.music[ctx.guild.id]["nowPlaying"]:
            return sendPlayingSongEmbed(self, ctx, self.bot.music[ctx.guild.id]["nowPlaying"])
        await ctx.channel.send(f"{ctx.author.mention} There is currently no song!")


def setup(bot):
    bot.add_cog(CogNowPlaying(bot))