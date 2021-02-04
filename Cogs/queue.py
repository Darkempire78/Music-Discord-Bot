import discord
from discord.ext import commands

from Tools.Check import Check

class CogQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "queue",
                    usage="",
                    description = "Display the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def queue(self, ctx):

        if not await Check().queueEmpty(ctx, self.bot): return 

        isFirstMessage = True
        message = ""
        for number, i in enumerate(self.bot.music[ctx.guild.id]["musics"], start=1):
            if i["music"].duration is None:
                duration = "Live"
            else:
                musicDurationSeconds = round(i["music"].duration % 60)
                if musicDurationSeconds < 10:
                    musicDurationSeconds = "0" + str(round(musicDurationSeconds))
                duration = str(round(i["music"].duration//60)) + f":{round(int(musicDurationSeconds))}"
            i["music"].title = i["music"].title.replace("*", "\\*")

            i["music"].title =i["music"].title.replace("*", "\\*")

            message += f"**{number}) ["+ i["music"].title + "](https://www.youtube.com"+ i["music"].url + f"])** ({duration})\n"
            if len(message) > 1800:
                
                if isFirstMessage:
                    embedTitle = "Queue"
                    isFirstMessage = False
                else:
                    embedTitle = ""

                embed=discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
                embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                message = ""
        if len(message) > 0:
            embed=discord.Embed(title="", description=message, color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(CogQueue(bot))