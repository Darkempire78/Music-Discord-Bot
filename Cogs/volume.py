import discord
from discord.ext import commands

from Tools.Check import Check

class CogVolume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "volume",
                    usage="<0 to 200>",
                    description = "Change the bot's volume.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def volume(self, ctx, volume):

        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 

        if (
            (not volume.isdigit()) or 
            (int(volume)) < 0 or 
            (int(volume) > 200)
        ):
            return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The volume have to be a number between 0 and 200!")

        player = self.bot.wavelink.get_player(ctx.guild.id)

        volume = int(volume)
        await player.set_volume(volume)

        embed=discord.Embed(title="Volume changed :", description=f"The volumed was changed to : ``{volume} %``", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogVolume(bot))