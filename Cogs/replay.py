import discord
from discord.ext import commands

from Tools.Check import Check
from Tools.Utils import Utils

from DataBase.Queue import DBQueue

class CogReplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "replay",
                    aliases=["repeat"],
                    usage="",
                    description = "Replay the current song")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def replay(self, ctx):
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return
        if not await Check().botInVoiceChannel(ctx, self.bot): return
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return
        if not await Check().botIsPlaying(ctx, self.bot): return 

        formerTrack = DBQueue(self.bot.dbConnection).displayFormer(ctx.guild.id)

        if formerTrack is None:
            return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} There is no former track to replay!")

        futureIndex = DBQueue(self.bot.dbConnection).getFutureIndex(ctx.guild.id)
        futureIndex += 1

        trackUri = formerTrack[4]
        trackTitle = formerTrack[5].replace("*", "\\*")
        durationInMs = formerTrack[6]
        trackDuration = await Utils().durationFormat(durationInMs)
        requester = f"{ctx.author.name}#{ctx.author.discriminator}"

        # Add the former track at the end of the queue
        DBQueue(self.bot.dbConnection).add(ctx.guild.id, False, requester, ctx.channel.id, trackUri, trackTitle, durationInMs, futureIndex)

        embed=discord.Embed(title="Replay", description=f"New song added : **[{trackTitle}]({trackUri})** ({trackDuration})", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
        


def setup(bot):
    bot.add_cog(CogReplay(bot))