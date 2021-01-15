import discord
import json
import aiohttp
import asyncio
import tekore # Spotify

from discord.ext import commands

from youtubesearchpython import VideosSearch, PlaylistsSearch, Video, ResultMode

from sclib.asyncio import SoundcloudAPI, Track, Playlist

from Tools.Music import Music
from Tools.playTrack import playTrack


async def searchSpotifyTrack(self, ctx, args):
    """Get a YouTube link from a Spotify link."""
    await ctx.send("<:SpotifyLogo:798492403882262569> Searching...", delete_after=10)
    # Get track's id
    trackId = tekore.from_url(args)
    try:
        track = await self.bot.spotify.track(trackId[1])
    except:
        await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The Spotify link is invalid!")
        return None
    title = track.name
    artist = track.artists[0].name
    # Search on youtube
    results = VideosSearch(f"{title} {artist}", limit = 1).result()["result"]
    if len(results) == 0:
        await noResultFound(self, ctx)
        return None
    return results[0]["link"]

async def searchSpotifyPlaylist(self, ctx, args):
    """Get Spotify links from a playlist link."""
    await ctx.send("<:SpotifyLogo:798492403882262569> Searching...", delete_after=10)
    # Get palylist's id
    playlistId = tekore.from_url(args)
    try:
        playlist = await self.bot.spotify.playlist(playlistId[1])
    except:
        await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The Spotify playlist is invalid!")
        return None

    trackLinks = []
    if playlist.tracks.total > 25:
        await playlistTooLarge(self, ctx)
        return None
    await ctx.send("<:SpotifyLogo:798492403882262569> Loading... (This process can takes several seconds)", delete_after=60)
    for i in playlist.tracks.items:
        title = i.track.name
        artist = i.track.artists[0].name
        # Search on youtube
        results = VideosSearch(f"{title} {artist}", limit = 1).result()["result"]
        if len(results) == 0:
            await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} No song found to : `{title} - {artist}` !")
        else:
            trackLinks.append(results[0]["link"])
    if not trackLinks: # if len(trackLinks) == 0:
        return None
    return trackLinks


async def searchDeezer(self, ctx, args):
    """Get a YouTube link from a Deezer link."""
    await ctx.send("<:DeezerLogo:798492403048644628> Searching...", delete_after=10)
    async with aiohttp.ClientSession() as session:
        async with session.get(args) as response:
            # Chack if it's a track
            if "track" in response._real_url.path:
                link = await searchDeezerTrack(self, ctx, session, response)
                if link is None: 
                    return None
                return link
            elif "playlist" in response._real_url.path:
                links = await searchDeezerPlaylist(self, ctx, session, response)
                if links is None: 
                    return None
                return links
            else:
                await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The Deezer link is not a track!")
                return None
            
async def searchDeezerTrack(self, ctx, session, response):
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

async def searchDeezerPlaylist(self, ctx, session, response):
    #Get the playlist ID
    playlistId = response._real_url.name
    async with session.get(f"https://api.deezer.com/playlist/{playlistId}") as response:
        response = await response.json()
        if response["nb_tracks"] > 25:
            await playlistTooLarge(self, ctx)
            return None
        await ctx.send("<:DeezerLogo:798492403048644628> Loading... (This process can takes several seconds)", delete_after=60)
        trackLinks = []
        for i in response["tracks"]["data"]:
            title = i["title_short"]
            artist = i["artist"]["name"]
            # Search on youtube
            results = VideosSearch(f"{title} {artist}", limit = 1).result()["result"]
            if len(results) == 0:
                await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} No song found to : `{title} - {artist}` !")
            else:
                trackLinks.append(results[0]["link"])
        if not trackLinks:
            return None
        return trackLinks

async def searchSoundcloud(self, ctx, args):
    """Get a YouTube link from a SoundCloud link."""
    await ctx.send("<:SoundCloudLogo:798492403459424256> Searching...", delete_after=10)
    soundcloud = SoundcloudAPI()
    try:
        trackOrPlaylist = await soundcloud.resolve(args)
        if isinstance(trackOrPlaylist, Track):
            link = await searchSoundcloudTrack(self, ctx, trackOrPlaylist)
            if link is None: 
                return None
            return link
        elif isinstance(trackOrPlaylist, Playlist):
            links = await searchSoundcloudPlaylist(self, ctx, trackOrPlaylist)
            if links is None: 
                return None
            return links
        else:
            await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The Soundcloud link is not a track or a playlist!")
            return None
    except:
        await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The Soundcloud link is invalid!")
        return None

async def searchSoundcloudTrack(self, ctx, track):
    # Search on youtube
    results = VideosSearch(track.title.replace("-", " ") + f" {track.artist}", limit = 1).result()["result"]
    if len(results) == 0:
        await noResultFound(self, ctx)
        return None
    return results[0]["link"] 

async def searchSoundcloudPlaylist(self, ctx, playlist):
    if playlist.track_count > 25:
        await playlistTooLarge(self, ctx)
        return None
    await ctx.send("<:SoundCloudLogo:798492403459424256> Loading... (This process can takes several seconds)", delete_after=60)
    trackLinks = []
    for i in playlist.tracks:
        results = VideosSearch(i.title.replace("-", " ") + f" {i.artist}", limit = 1).result()["result"]
        if len(results) == 0:
            await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} No song found to : `{i.title} - {i.artist}` !")
        else:
            trackLinks.append(results[0]["link"])
    return trackLinks

async def searchQuery(self, ctx, args):
    """Get a YouTube link from a query."""
    await ctx.send("<:YouTubeLogo:798492404587954176> Searching...", delete_after=10)
    results = VideosSearch(args, limit = 5).result()["result"]
            
    message = ""
    number = 0
    if len(results) == 0:
        await noResultFound(self, ctx)
        return None
    for i in results:
        number += 1
        i["title"] =i["title"].replace("*", "\\*")
        message += f"**{number}) ["+ i["title"] + "]("+ i["link"] + "])** ("+ str(i["duration"]) + ")\n"
    embed=discord.Embed(title="Search results :", description=f"Choose your result.\nWrite `0` to pass the cooldown.\n\n{message}", color=discord.Colour.random())
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
        embed = discord.Embed(title = f"**TIME IS OUT**", description = f"<:False:798596718563950653> {ctx.author.mention} You exceeded the response time (15s)", color = discord.Colour.red())
        await ctx.channel.send(embed = embed)
        return None

async def searchPlaylist(self, ctx, args):
    """Get YouTube links from a playlist link."""
    await ctx.send("<:YouTubeLogo:798492404587954176> Searching...", delete_after=10)
    videoCount = int(PlaylistsSearch(args, limit = 1).result()["result"][0]["videoCount"])
    if videoCount == 0:
        await noResultFound(self, ctx)
        return None
    if videoCount > 25:
        await playlistTooLarge(self, ctx)
        return None
    await ctx.send("<:YouTubeLogo:798492404587954176> Loading... (This process can takes several seconds)", delete_after=60)
    with self.bot.ytdl:
        result = self.bot.ytdl.extract_info(args, download=False)
        videos = result['entries']
        return [i["webpage_url"] for i in videos]


async def playlistTooLarge(self, ctx):
    """Send an embed with the error : playlist is too big."""
    embed=discord.Embed(title="Search results :", description=f"<:False:798596718563950653> The playlist is too big! (max : 25 tracks)", color=discord.Colour.random())
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

async def noResultFound(self, ctx):
    """Send an embed with the error : no result found."""
    embed=discord.Embed(title="Search results :", description=f"<:False:798596718563950653> No result found!", color=discord.Colour.random())
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

class CogPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "play",
                    aliases=["p"],
                    usage="<Link/Query>",
                    description = "The bot searches and plays the music.")
    @commands.guild_only()
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def play(self, ctx, *args):

        args = " ".join(args)

        # Spotify
        if args.startswith("https://open.spotify.com"):
            if args.startswith("https://open.spotify.com/track"):
                args = await searchSpotifyTrack(self, ctx, args)
            elif args.startswith("https://open.spotify.com/playlist"):
                args = await searchSpotifyPlaylist(self, ctx, args)
            if args is None: return
        
        # Deezer
        elif args.startswith("https://deezer.page.link") or args.startswith("https://www.deezer.com"): 
            args = await searchDeezer(self, ctx, args)
            if args is None:
                return
 
        # SoundCloud
        elif args.startswith("https://soundcloud.com"): 
            args = await searchSoundcloud(self, ctx, args)
            if args is None: return
        
        # Youtube Playlist
        elif args.startswith("https://www.youtube.com/playlist"): 
            args = await searchPlaylist(self, ctx, args)
            if args is None: return

        # Query
        elif not args.startswith("https://www.youtube.com/watch"):
            args = await searchQuery(self, ctx, args)
            if args is None: return

        # YouTube video
        else:
            await ctx.send("<:YouTubeLogo:798492404587954176> Searching...", delete_after=10)
            try:
                # Check if the link exist
                Video.get(args, mode = ResultMode.json)
            except:
                return await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The YouTube link is invalid!")

        links = args
        client = ctx.guild.voice_client

        if not isinstance(links, list):
            links = [links]

        playlistMessage = None
        isPlaylist = False
        if len(links) > 1:
            isPlaylist = True

        for link in links:
            if client and client.channel:
                if (self.bot.user.id not in [i.id for i in ctx.author.voice.channel.members]):
                    return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} I'm already connected in a voice channel!")
                if self.bot.music[ctx.guild.id]["nowPlaying"] is None:
                    await ctx.send("Loading...", delete_after=10)
                music = Music(self, link)
                music.title = music.title.replace("*", "\\*")
                if music.isLive:
                    duration = "Live"
                else:
                    musicDurationSeconds = music.duration % 60
                    if musicDurationSeconds < 10:
                        musicDurationSeconds = f"0{musicDurationSeconds}"
                    duration = f"{music.duration//60}:{musicDurationSeconds}"
                
                if self.bot.music[ctx.guild.id]["nowPlaying"] is None:
                    self.bot.music[ctx.guild.id]["musics"] = []
                    self.bot.music[ctx.guild.id]["volume"] = 0.5
                    return playTrack(self, ctx, client, {"music": music, "requestedBy": ctx.author})

                self.bot.music[ctx.guild.id]["musics"].append(
                    {
                    "music": music,
                    "requestedBy": ctx.author
                    }
                )
                if not isPlaylist:
                    embed=discord.Embed(title="Songs added in the queue", description=f"New songs added : **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                    embed.set_thumbnail(url=music.thumbnails)
                    await ctx.channel.send(embed=embed)
                else:
                    # If it's a plylist => Update the same message to do not spam the channel
                    if playlistMessage is None:
                        embed=discord.Embed(title="Song added in the queue", description=f"- **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                        embed.set_thumbnail(url=music.thumbnails)
                        playlistMessage = await ctx.channel.send(embed=embed)
                    else:
                        # Update the message
                        embedEdited = discord.Embed(title="Songs added in the queue", description= playlistMessage.embeds[0].description + f"\n- **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                        playlistMessage.embeds[0].description = embedEdited.description
                        if len(playlistMessage.embeds[0].description) > 1800:
                            embed=discord.Embed(title="Song added in the queue", description=f"- **[{music.title}]({music.url})** ({duration})", color=discord.Colour.random())
                            embed.set_thumbnail(url=music.thumbnails)
                            playlistMessage = await ctx.channel.send(embed=embed)
                        else:
                            await playlistMessage.edit(embed=embedEdited)
                        
                
            else:
                voice = ctx.author.voice
                if ctx.author.voice is None:
                    return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} You are not connected in a voice channel!")
                await ctx.send("Loading...", delete_after=10)
                client = await voice.channel.connect() # Connect the bot to the voice channel
                music = Music(self, link) # Get music data
                self.bot.music[ctx.guild.id]["musics"] = []
                self.bot.music[ctx.guild.id]["volume"] = 0.5
                playTrack(self, ctx, client, {"music": music, "requestedBy": ctx.author})
            


def setup(bot):
    bot.add_cog(CogPlay(bot))