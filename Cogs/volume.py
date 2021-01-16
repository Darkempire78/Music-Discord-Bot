import discord
from discord.ext import commands


class CogVolume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "volume",
                    usage="<0 to 100>",
                    description = "Change the bot's volume.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def volume(self, ctx, volume):

        if not ctx.guild.voice_client:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm not connected in a voice channel!")

        if (
            (not volume.isdigit()) or 
            (int(volume)) < 0 or 
            (int(volume) > 100)
        ):
            return await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The volume have to be a number between 0 and 100 !")

        self.bot.music[ctx.guild.id]["volume"] = int(volume)/100
        ctx.guild.voice_client.source.volume = self.bot.music[ctx.guild.id]["volume"]
        
        embed=discord.Embed(title="Volume changed :", description=f"The volumed was changed to : ``{volume}%``", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogVolume(bot))