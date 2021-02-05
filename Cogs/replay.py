import discord
from discord.ext import commands

from Tools.Check import Check

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
        
        if not await Check().userInVoiceChannel(ctx, self.bot): return 
        if not await Check().botInVoiceChannel(ctx, self.bot): return 
        if not await Check().userAndBotInSameVoiceChannel(ctx, self.bot): return 
        if not await Check().botIsPlaying(ctx, self.bot): return 
        
        music = self.bot.music[ctx.guild.id]["nowPlaying"]["music"]
        self.bot.music[ctx.guild.id]["musics"].insert(0, {"music": music, "requestedBy": ctx.author})
        music.title = music.title.replace("*", "\\*")
        if music.duration is None:
            duration = "Live"
        else:
            musicDurationSeconds = round(music.duration % 60)
            if musicDurationSeconds < 10:
                musicDurationSeconds = "0" + str(round(musicDurationSeconds))
            duration = f"{round(music.duration//60)}:{musicDurationSeconds}"
        embed=discord.Embed(title="Replay", description=f"New song added : **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
        embed.set_thumbnail(url=music.thumbnails)
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
        


def setup(bot):
    bot.add_cog(CogReplay(bot))