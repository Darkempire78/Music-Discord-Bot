import discord
from discord.ext import commands


class CogMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "move",
                    usage="<IndexFrom> <IndexTo>",
                    description = "Move a song in the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def move(self, ctx, indexFrom, indexTo):
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]: 
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")
        if len(self.bot.music[ctx.guild.id]["musics"]) <= 0:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The queue is empty!")
        if not indexFrom.isdigit() or not indexTo.isdigit():
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The index have to be a number!")
        if (int(indexFrom) -1) > len(self.bot.music[ctx.guild.id]["musics"]) or (int(indexTo) -1) > len(self.bot.music[ctx.guild.id]["musics"]):
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The index is invalid!")

        former = self.bot.music[ctx.guild.id]["musics"][int(indexFrom) -1]
        self.bot.music[ctx.guild.id]["musics"].insert(int(indexTo), former.copy())
        self.bot.music[ctx.guild.id]["musics"].remove(former)
        await ctx.channel.send(f"{ctx.author.mention} " + former["music"] + f"was moved from `{indexFrom}` to `{indexTo}`.")


        


def setup(bot):
    bot.add_cog(CogMove(bot))