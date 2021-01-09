import discord
import json
import asyncio

from discord.ext import commands

from youtube_search import YoutubeSearch

from Tools.Music import Music
from Tools.playTrack import playTrack


class CogPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "play",
                    usage="<Link/Query>",
                    description = "The bot searches and plays the music.")
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def play(self, ctx, *args):

        args = " ".join(args)
        if not args.startswith("https://www.youtube.com"):
            results = YoutubeSearch(args, max_results=5).to_dict()
            message = ""
            number = 0
            if len(results) == 0:
                embed=discord.Embed(title="Search results :", description=f"No result found!", color=discord.Colour.random())
                embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                return await ctx.send(embed=embed)
            for i in results:
                number += 1
                i["title"] =i["title"].replace("*", "\\*")
                message += f"**{number}) ["+ i["title"] + "](https://www.youtube.com"+ i["url_suffix"] + "])** ("+ str(i["duration"]) + ")\n"
            embed=discord.Embed(title="Search results :", description=f"Choose your result.\nWrite ``0`` to pass the cooldown.\n\n{message}", color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

            def check(message):
                if message.content.isdigit():
                    message.content = int(message.content)
                    if ((message.content >= 0) and (message.content <= 5)):
                        message.content = str(message.content)
                        return message.content
            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
                if int(msg.content) == 0:
                    return await ctx.send(f"{ctx.author.mention} Search exit.")
                args = "https://www.youtube.com" + results[int(msg.content) -1]["url_suffix"]
            except asyncio.TimeoutError:
                embed = discord.Embed(title = f"**TIME IS OUT**", description = f"{ctx.author.mention} You exceeded the response time (15s)", color = discord.Colour.red())
                return await ctx.channel.send(embed = embed)
        
        link = args

        client = ctx.guild.voice_client

        if client and client.channel:
            if (self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]):
                return await ctx.channel.send(f"{ctx.author.mention} I'm already connected in a voice channel!")
            music = Music(self, link)
            self.bot.music[ctx.guild.id]["musics"].append(
                {
                "music": music,
                "requestedBy": ctx.author
                }
            )
            music.title = music.title.replace("*", "\\*")
            if music.isLive:
                duration = "Live"
            else:
                musicDurationSeconds = music.duration % 60
                if musicDurationSeconds < 10:
                    musicDurationSeconds = f"0{musicDurationSeconds}"
                duration = f"{music.duration//60}:{musicDurationSeconds}"
            embed=discord.Embed(title="Song added in the queue", description=f"New song added : **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
            embed.set_thumbnail(url=music.thumbnails)
            await ctx.channel.send(embed=embed)
        else:
            voice = ctx.author.voice
            if ctx.author.voice is None:
                return await ctx.channel.send(f"{ctx.author.mention} You are not connected in a voice channel!")
            client = await voice.channel.connect() # Connect the bot to the voice channel
            music = Music(self, link) # Get music data
            self.bot.music[ctx.guild.id]["musics"] = []
            playTrack(self, ctx, client, {"music": music, "requestedBy": ctx.author})


def setup(bot):
    bot.add_cog(CogPlay(bot))