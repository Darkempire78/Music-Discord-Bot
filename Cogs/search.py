import discord
import asyncio
from discord.ext import commands

from youtube_search import YoutubeSearch


class CogSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "search",
                    usage="<Query>",
                    description = "Search a song on youtube.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def search(self, ctx, args):
        results = YoutubeSearch(args, max_results=8).to_dict()
        message = ""
        number = 0
        if len(results) == 0:
            embed=discord.Embed(title="Search results :", description=f"No result found!", color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        for i in results:
            number += 1
            i["title"] =i["title"].replace("*", "\\*")
            message += f"**{number}) ["+ i["title"] + "](https://www.youtube.com"+ i["url_suffix"] + "])** ("+ str(i["duration"]) + ")\n"
        embed=discord.Embed(title="Search results :", description=f"{message}", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogSearch(bot))