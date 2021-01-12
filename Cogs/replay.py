import discord
from discord.ext import commands


class CogReplay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "replay",
                    aliases=["repeat"],
                    usage="",
                    description = "Replay the current song")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def replay(self, ctx):
        if ctx.author.voice is None:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
        if self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]: 
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in the same voice channel that the bot!")
        if not self.bot.music[ctx.guild.id]["nowPlaying"]:
            await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} There is currently no song to replay!")
        
        music = self.bot.music[ctx.guild.id]["nowPlaying"]["music"]
        self.bot.music[ctx.guild.id]["musics"].insert(0, {"music": music, "requestedBy": ctx.author})
        music.title = music.title.replace("*", "\\*")
        musicDurationSeconds = music.duration % 60
        if musicDurationSeconds < 10:
            musicDurationSeconds = f"0{musicDurationSeconds}"
        embed=discord.Embed(title="Replay", description=f"New song added : **[{music.title}]({music.url})** ({music.duration//60}:{musicDurationSeconds})", color=discord.Colour.random())
        embed.set_thumbnail(url=music.thumbnails)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
        


def setup(bot):
    bot.add_cog(CogReplay(bot))