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

        player = self.bot.wavelink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.channel.send(f"{ctx.author.mention} There is currently no song!")
        
        await sendPlayingSongEmbed(self, ctx.channel, player.current)



def setup(bot):
    bot.add_cog(CogNowPlaying(bot))