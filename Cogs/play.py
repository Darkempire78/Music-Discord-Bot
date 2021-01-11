import discord
import json
import aiohttp
import asyncio
import tekore # Spotify

from discord.ext import commands

from youtubesearchpython import VideosSearch

from sclib.asyncio import SoundcloudAPI, Track

from Tools.Music import Music
from Tools.playTrack import playTrack


async def searchSpotify(self, ctx, args):
    """Get a YouTube link from a Spotify link."""
    # Get track's id
    trackId = tekore.from_url(args)
    try:
        track = await self.bot.spotify.track(trackId[1])
    except:
        await ctx.send(f"{ctx.author.mention} The Spotify link is invalid!")
        return None
    title = track.name
    artist = track.artists[0].name
    # Search on youtube
    results = VideosSearch(f"{title} {artist}", limit = 1).result()["result"]
    if len(results) == 0:
        await noResultFound(self, ctx)
        return None
    return results[0]["link"]

async def searchDeezer(self, ctx, args):
    """Get a YouTube link from a Deezer link."""
    async with aiohttp.ClientSession() as session:
        async with session.get(args) as response:
            # Chack if it's a track
            if "track" not in response._real_url.path:
                await ctx.send(f"{ctx.author.mention} The Deezer link is not a track!")
                return None
            # Get the music ID
            trackId = response._real_url.name
        async with session.get(f"https://api.deezer.com/track/{trackId}") as response:
            response = await response.json()
            title = response["title_short"]
            artist = response["artist"]["name"]
            # Search on youtube
            results = VideosSearch(f"{title} {artist}", limit = 1).result()["result"]
            if len(results) == 0:
                await noResultFound(self, ctx)
                return None
            return results[0]["link"]

async def searchSoundcloud(self, ctx, args):
    """Get a YouTube link from a SoundCloud link."""
    soundcloud = SoundcloudAPI()
    try:
        track = await soundcloud.resolve(args)
        if not isinstance(track, Track):
            await ctx.send(f"{ctx.author.mention} The Soundcloud link is not a track!")
            return None
        # Search on youtube
        results = VideosSearch(track.title.replace("-", " ") + f" {track.artist}", limit = 1).result()["result"]
        if len(results) == 0:
            await noResultFound(self, ctx)
            return None
        return results[0]["link"]
            
    except:
        await ctx.send(f"{ctx.author.mention} The Soundcloud link is invalid!")
        return None

async def searchQuery(self, ctx, args):
    """Get a YouTube link from a query."""
    results = VideosSearch(args, limit = 5).result()["result"]
            
    message = ""
    number = 0
    if len(results) == 0:
        await noResultFound(self, ctx)
        return None
    for i in results:
        number += 1
        i["title"] =i["title"].replace("*", "\\*")
        message += f"**{number}) ["+ i["title"] + "](https://www.youtube.com"+ i["link"] + "])** ("+ str(i["duration"]) + ")\n"
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
            await ctx.send(f"{ctx.author.mention} Search exit!")
            return None
        return results[int(msg.content) -1]["link"]
    except asyncio.TimeoutError:
        embed = discord.Embed(title = f"**TIME IS OUT**", description = f"{ctx.author.mention} You exceeded the response time (15s)", color = discord.Colour.red())
        await ctx.channel.send(embed = embed)
        return None

async def noResultFound(self, ctx):
    """Send an embed with the error : no result found."""
    embed=discord.Embed(title="Search results :", description=f"No result found!", color=discord.Colour.random())
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

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
        await ctx.send("Searching...", delete_after=10)

        # Spotify
        if args.startswith("https://open.spotify.com/track"):
            args = await searchSpotify(self, ctx, args)
            if args is None: return
        
        # Deezer
        elif args.startswith("https://deezer.page.link") or args.startswith("https://www.deezer.com"): 
            args = await searchDeezer(self, ctx, args)
            if args is None: return
 
        # SoundCloud
        elif args.startswith("https://soundcloud.com"): 
            args = await searchSoundcloud(self, ctx, args)
            if args is None: return
            
        # Query
        elif not args.startswith("https://www.youtube.com"):
            args = await searchQuery(self, ctx, args)
            if args is None: return

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
            self.bot.music[ctx.guild.id]["volume"] = 0.5


def setup(bot):
    bot.add_cog(CogPlay(bot))