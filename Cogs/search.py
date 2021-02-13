import discord
from discord.ext import commands

from Tools.Utils import Utils

from Cogs.play import noResultFound

class CogSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "search",
                    usage="<Query>",
                    description = "Search a song on youtube.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def search(self, ctx, args):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{args}')
   
        message = ""
        number = 0
        if tracks is None:
            await noResultFound(self, ctx)
            return None
        for i in tracks:
            if number >= 8:
                break
            number += 1
            duration = await Utils().durationFormat(i.duration)
            message += f"**{number}) [{i.title}]({i.uri}])** ({duration})\n"
        embed=discord.Embed(title="Search results :", description=f"choose the number that corresponds to the music.\nWrite `0` to pass the cooldown.\n\n{message}", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogSearch(bot))