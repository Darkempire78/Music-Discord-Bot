import discord
from discord.ext import commands

from Tools.Check import Check

from DataBase.Queue import DBQueue

class CogMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "move",
                    usage="<IndexFrom> <IndexTo>",
                    description = "Move a song in the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def move(self, ctx, indexFrom, indexTo):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        
        tracks = DBQueue(self.bot.dbConnection).display(ctx.guild.id)
        tracksCount = len(tracks)

        if len(tracks) == 0:
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The queue is empty!")

        if not indexFrom.isdigit() or not indexTo.isdigit():
            return await ctx.channel.send(f"{self.bot.emojiList.false}{ctx.author.mention} Index have to be a number!")
        if ((int(indexFrom)) > tracksCount) or ((int(indexTo)) > tracksCount):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} Index is invalid!")
        if (int(indexFrom) == int(indexTo)):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} Indexes cannot be the same!")

        indexFromFake = int(indexFrom)
        indexToFake = int(indexTo)

        # Get real index 
        indexFrom = DBQueue(self.bot.dbConnection).getIndexFromFakeIndex(ctx.guild.id, indexFromFake -1)
        indexTo = DBQueue(self.bot.dbConnection).getIndexFromFakeIndex(ctx.guild.id, indexToFake -1)

        # Get the track to move
        trackToMove = DBQueue(self.bot.dbConnection).displaySpecific(ctx.guild.id, indexFrom)
        indexFrom = trackToMove[7]

        # Delete the track to move
        DBQueue(self.bot.dbConnection).remove(ctx.guild.id, indexFrom)

        if indexFrom < indexTo:
            # -1 to each track between trackToMove index and 
            DBQueue(self.bot.dbConnection).updateRemoveOneToEach(ctx.guild.id, indexFrom, indexTo)
        else:
            # +1 to each track between trackToMove index and 
            DBQueue(self.bot.dbConnection).updateAddOneToEach(ctx.guild.id, indexFrom, indexTo)
    
        # Re-create the track
        DBQueue(self.bot.dbConnection).add(trackToMove[0], trackToMove[1], trackToMove[2], trackToMove[3], trackToMove[4], trackToMove[5], trackToMove[6], indexTo) 

        embed = discord.Embed(title="Song moved", description=f"- [**{trackToMove[5]}**]({trackToMove[4]}) was moved from `{indexFromFake}` to `{indexToFake}`.", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(CogMove(bot))
