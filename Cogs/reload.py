import discord
from discord.ext import commands
from math import ceil


class CogReaload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "reload",
                    usage="",
                    description = "Reload the current music.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def skip(self, ctx):
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")

        # If user is not in the same voice channel that the bot
        if self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]: 
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")
            
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