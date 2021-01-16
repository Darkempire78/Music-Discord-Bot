import discord
import asyncio
from discord.ext import commands

from youtubesearchpython import VideosSearch


class CogSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "search",
                    usage="<Query>",
                    description = "Search a song on youtube.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def search(self, ctx, args):
        results = VideosSearch(args, limit = 10).result()["result"]
        message = ""
        if len(results) == 0:
            embed=discord.Embed(title="Search results :", description=f"No result found!", color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
            return await ctx.send(embed=embed)
        for number, i in enumerate(results, start=1):
            i["title"] =i["title"].replace("*", "\\*")
            message += f"**{number}) ["+ i["title"] + "]("+ i["link"] + "])** ("+ str(i["duration"]) + ")\n"
        embed=discord.Embed(title="Search results :", description=f"{message}", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogSearch(bot))