import discord
from discord.ext import commands

from Tools.Check import Check


class CogMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "move",
                    usage="<IndexFrom> <IndexTo>",
                    description = "Move a song in the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def move(self, ctx, indexFrom, indexTo):
        
        if not await Check().userInVoiceChannel(ctx): return 
        if not await Check().botInVoiceChannel(ctx): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        if not await Check().queueEmpty(ctx, self.bot): return 

        if not indexFrom.isdigit() or not indexTo.isdigit():
            return await ctx.channel.send(f"{self.bot.emojiList.false}{ctx.author.mention} The index have to be a number!")
        if (int(indexFrom) -1) > len(self.bot.music[ctx.guild.id]["musics"]) or (int(indexTo) -1) > len(self.bot.music[ctx.guild.id]["musics"]):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The index is invalid!")

        former = self.bot.music[ctx.guild.id]["musics"][int(indexFrom) -1]
        self.bot.music[ctx.guild.id]["musics"].insert(int(indexTo), former.copy())
        self.bot.music[ctx.guild.id]["musics"].remove(former)
        
        embed=discord.Embed(title="Song moved", description="- [**" + former["music"].title + f"**](" + former["music"].url + f") was moved from `{indexFrom}` to `{indexTo}`.", color=discord.Colour.random())
        embed.set_thumbnail(url=former["music"].thumbnails)
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

        


def setup(bot):
    bot.add_cog(CogMove(bot))