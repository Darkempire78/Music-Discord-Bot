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
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The queue is empty!")

        message = ""
        for number, i in enumerate(self.bot.music[ctx.guild.id]["musics"], start=1):
            musicDurationSeconds = i["music"].duration % 60
            if musicDurationSeconds < 10:
                musicDurationSeconds = f"0{musicDurationSeconds}"
            i["music"].title = i["music"].title.replace("*", "\\*")

            i["music"].title =i["music"].title.replace("*", "\\*")
            
            message += f"**{number}) ["+ i["music"].title + "](https://www.youtube.com"+ i["music"].url + f"])** (" + str(i["music"].duration//60) + f":{musicDurationSeconds})\n"
            if len(message) > 1800:
                embed=discord.Embed(title="Queue", description=message, color=discord.Colour.random())
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                message = ""
        if len(message) > 0:
            embed=discord.Embed(title="Queue", description=message, color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(CogQueue(bot))