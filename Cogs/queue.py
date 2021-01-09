import discord
from discord.ext import commands


class CogQueue(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "queue",
                    usage="",
                    description = "Display the queue.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def queue(self, ctx):

        if len(self.bot.music[ctx.guild.id]["musics"]) <= 0:
            return await ctx.channel.send(f"{ctx.author.mention} The queue is empty!")
            
        message = ""
        number = 0
        for i in self.bot.music[ctx.guild.id]["musics"]:
            musicDurationSeconds = i.duration % 60
            if musicDurationSeconds < 10:
                musicDurationSeconds = f"0{musicDurationSeconds}"
            i.title = i.title.replace("*", "\\*")

            number += 1
            i.title =i.title.replace("*", "\\*")
            message += f"**{number}) ["+ i.title + "](https://www.youtube.com"+ i.url + f"])** (" + str(i.duration//60) + f":{musicDurationSeconds})\n"
        embed=discord.Embed(title="Queue", description=message, color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(CogQueue(bot))