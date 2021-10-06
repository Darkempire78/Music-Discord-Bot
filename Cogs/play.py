import discord
import json
import aiohttp
import asyncio
import tekore # Spotify

import wavelink

from discord.ext import commands

from youtubesearchpython import PlaylistsSearch

from Tools.Utils import Utils

from Tools.addTrack import addTrack
from Tools.Check import Check


async def searchSpotifyTrack(self, ctx, args):
    """Get a YouTube link from a Spotify link."""
    await ctx.send(f"{self.bot.emojiList.spotifyLogo} Searching...", delete_after=10)
    # Get track's id
    trackId = tekore.from_url(args)
    try:
        track = await self.bot.spotify.track(trackId[1])
    except:
        await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The Spotify link is invalid!")
        return None
    title = track.name
    artist = track.artists[0].name
    # Search on youtube
    track = await self.bot.wavelink.get_tracks(f'ytsearch:{title} {artist}')
    if len(track) == 0:
        await noResultFound(self, ctx)
        return None
    return track[0]

async def searchSpotifyPlaylist(self, ctx, args):
    """Get Spotify links from a playlist link."""
    await ctx.send(f"{self.bot.emojiList.spotifyLogo} Searching...", delete_after=10)
    # Get palylist's id
    playlistId = tekore.from_url(args)
    try:
        playlist = await self.bot.spotify.playlist(playlistId[1])
    except:
        await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The Spotify playlist is invalid!")
        return None

    trackLinks = []
    if self.playlistLimit != 0 and playlist.tracks.total > self.playlistLimit:
        await playlistTooLarge(self, ctx)
        return None
    await ctx.send(f"{self.bot.emojiList.spotifyLogo} Loading... (This process can take several seconds)", delete_after=60)
    for i in playlist.tracks.items:
        title = i.track.name
        artist = i.track.artists[0].name
        # Search on youtube
        track = await self.bot.wavelink.get_tracks(f'ytsearch:{title} {artist}')
        if track is None:
            await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} No song found to : `{title} - {artist}` !")
        else:
            trackLinks.append(track[0])
    if not trackLinks: # if len(trackLinks) == 0:
        return None
    return trackLinks


async def searchDeezer(self, ctx, args):
    """Get a YouTube link from a Deezer link."""
    await ctx.send(f"{self.bot.emojiList.deezerLogo} Searching...", delete_after=10)
    async with aiohttp.ClientSession() as session:
        async with session.get(args) as response:
            # Chack if it's a track
            if "track" in response._real_url.path:
                link = await searchDeezerTrack(self, ctx, session, response)
                if link is None: 
                    return None
                return link
            if "playlist" in response._real_url.path:
                links = await searchDeezerPlaylist(self, ctx, session, response)
                if links is None: 
                    return None
                return links
            await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The Deezer link is not a track!")
            return None
            
async def searchDeezerTrack(self, ctx, session, response):
    # Get the music ID
    trackId = response._real_url.name
    async with session.get(f"https://api.deezer.com/track/{trackId}") as response:
        response = await response.json()
        title = response["title_short"]
        artist = response["artist"]["name"]
        # Search on youtube
        track = await self.bot.wavelink.get_tracks(f'ytsearch:{title} {artist}')
        if len(track) == 0:
            await noResultFound(self, ctx)
            return None
        return track[0]

async def searchDeezerPlaylist(self, ctx, session, response):
    #Get the playlist ID
    playlistId = response._real_url.name
    async with session.get(f"https://api.deezer.com/playlist/{playlistId}") as response:
        response = await response.json()
        if self.playlistLimit != 0 and response["nb_tracks"] > self.playlistLimit:
            await playlistTooLarge(self, ctx)
            return None
        await ctx.send(f"{self.bot.emojiList.deezerLogo} Loading... (This process can take several seconds)", delete_after=60)
        trackLinks = []
        for i in response["tracks"]["data"]:
            title = i["title_short"]
            artist = i["artist"]["name"]
            # Search on youtube
            track = await self.bot.wavelink.get_tracks(f'ytsearch:{title} {artist}')
            if len(track) == 0:
                await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} No song found to : `{title} - {artist}` !")
            else:
                trackLinks.append(track[0])
        if not trackLinks:
            return None
        return trackLinks


async def searchSoundcloud(self, ctx, args):
    """Get a YouTube link from a SoundCloud link."""
    await ctx.send(f"{self.bot.emojiList.soundcloudLogo} Searching...", delete_after=10)

    track = await self.bot.wavelink.get_tracks(args)

    if len(track) == 0:
        await noResultFound(self, ctx)
        return None
    
    elif len(track) > 1:
        if self.playlistLimit != 0 and len(track) > self.playlistLimit:
            await playlistTooLarge(self, ctx)
            return None
        return track.tracks

    return track


async def searchQuery(self, ctx, args):
    """Get a YouTube link from a query."""
    await ctx.send(f"{self.bot.emojiList.youtubeLogo} Searching...", delete_after=10)

    tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{args}')

    message = ""
    number = 0
    if tracks is None:
        await noResultFound(self, ctx)
        return None
    for i in tracks[:5]:
        number += 1
        duration = await Utils().durationFormat(i.duration)
        message += f"**{number}) [{i.title}]({i.uri}])** ({duration})\n"
    embed=discord.Embed(title="Search results :", description=f"choose the number that corresponds to the music.\nWrite `0` to pass the cooldown.\n\n{message}", color=discord.Colour.random())
    embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

    def check(message):
        if message.content.isdigit():
            messageContent = int(message.content)
            if ((messageContent >= 0) and (messageContent <= 5)):
                return message.content
    try:
        msg = await self.bot.wait_for('message', timeout=15.0, check=check)
        if int(msg.content) == 0:
            await ctx.send(f"{ctx.author.mention} Search exit!")
            return None
        return tracks[int(msg.content) -1]
    except asyncio.TimeoutError:
        embed = discord.Embed(title = f"**TIME IS OUT**", description = f"{self.bot.emojiList.false} {ctx.author.mention} You exceeded the response time (15s)", color = discord.Colour.red())
        await ctx.channel.send(embed = embed)
        return None

async def searchPlaylist(self, ctx, args):
    """Get YouTube links from a playlist link."""
    await ctx.send("<:YouTubeLogo:798492404587954176> Searching...", delete_after=10)
    videoCount = int(PlaylistsSearch(args, limit = 1).result()["result"][0]["videoCount"])
    if videoCount == 0:
        await noResultFound(self, ctx)
        return None
    if self.playlistLimit != 0 and videoCount > self.playlistLimit:
        await playlistTooLarge(self, ctx)
        return None
    await ctx.send("<:YouTubeLogo:798492404587954176> Loading... (This process can take several seconds)", delete_after=60)
    
    tracks = await self.bot.wavelink.get_tracks(args)
    return tracks.tracks


async def playlistTooLarge(self, ctx):
    """Send an embed with the error : playlist is too big."""
    embed=discord.Embed(title="Search results :", description=f"{self.bot.emojiList.false} The playlist is too big! (max : {self.playlistLimit} tracks)", color=discord.Colour.random())
    embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

async def noResultFound(self, ctx):
    """Send an embed with the error : no result found."""
    embed=discord.Embed(title="Search results :", description=f"{self.bot.emojiList.false} No result found!", color=discord.Colour.random())
    embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

class CogPlay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("configuration.json", "r") as config:
            data = json.load(config)
            self.playlistLimit = int(data.get("playlistLimit", 15))
            # 0 is nolimit
            print(f"Playlist limit set to {self.playlistLimit}")

    @commands.command(name = "play",
                    aliases=["p"],
                    usage="<Link/Query>",
                    description = "The bot searches and plays the music.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def play(self, ctx, *args):

        if not await Check().userInVoiceChannel(ctx, self.bot): return 

        args = " ".join(args)

        # Spotify
        if args.startswith("https://open.spotify.com"):
            if args.startswith("https://open.spotify.com/track"):
                args = await searchSpotifyTrack(self, ctx, args)
            elif args.startswith("https://open.spotify.com/playlist"):
                args = await searchSpotifyPlaylist(self, ctx, args)
            else:
                return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} Only Spotify playlist and Spotify track are available!")
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

        # YouTube video
        elif args.startswith("https://www.youtube.com/watch"):
            await ctx.send("<:YouTubeLogo:798492404587954176> Searching...", delete_after=10)
            # Check if the link exists
            track = await self.bot.wavelink.get_tracks(args)
            args = track[0]
            if track is None:
                return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")
        
        # Query
        else:
            args = await searchQuery(self, ctx, args)
            if args is None: return

        tracks = args

        await addTrack(self, ctx, tracks) 
            

def setup(bot):
    bot.add_cog(CogPlay(bot))
