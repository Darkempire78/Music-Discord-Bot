import discord
from discord.ext import commands


class CogRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "remove",
                    usage="<Index>",
                    description = "Remove the song with its index.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def remove(self, ctx, index):
        
        if ctx.author.voice is None:
            return await ctx.channel.send(f"{ctx.author.mention} You are not connected in a voice channel!")
        if self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]: 
            return await ctx.channel.send(f"{ctx.author.mention} You are not connected in the same voice channel that the bot!")
        if len(self.bot.music[ctx.guild.id]["musics"]) <= 0:
            return await ctx.channel.send(f"{ctx.author.mention} The queue is empty!")
        if not index.isdigit():
            return await ctx.channel.send(f"{ctx.author.mention} The index have to be a number!")
        if (int(index) -1) > len(self.bot.music[ctx.guild.id]["musics"]):
            return await ctx.channel.send(f"{ctx.author.mention} The index is invalid!")

        index = int(index) - 1
        music = self.bot.music[ctx.guild.id]["musics"][index]["music"]
        music.title = music.title.replace("*", "\\*")
        musicDurationSeconds = music.duration % 60
        if musicDurationSeconds < 10:
            musicDurationSeconds = f"0{musicDurationSeconds}"
        embed=discord.Embed(title="Song Remove in the queue", description=f"Song removed : **[{music.title}]({music.url})** ({music.duration//60}:{musicDurationSeconds})", color=discord.Colour.random())
        embed.set_thumbnail(url=music.thumbnails)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
        # Remove
        del self.bot.music[ctx.guild.id]["musics"][index]


def setup(bot):
    bot.add_cog(CogRemove(bot))