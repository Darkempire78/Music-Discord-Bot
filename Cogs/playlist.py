import discord
from discord.ext import commands

import json
from youtubesearchpython import Video, ResultMode

from DataBase.Playlist import DBPlaylist

from Tools.addTrack import addTrack

class CogPlaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(name="playlist", invoke_without_command=True)
    async def playlist(self, ctx):
        pass


    @playlist.command(name = "add",
                    aliases=[],
                    usage="<YouTubeLink>",
                    description = "Add a song to your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_add(self, ctx, link):
        if not link.startswith("https://www.youtube.com/watch"):
            return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")
        # Check if the link exists
        track = await self.bot.wavelink.get_tracks(link)
        track = track[0]
        if track is None:
            return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} The YouTube link is invalid!")
        
        playlistSize = DBPlaylist(self.bot.dbConnection).countPlaylistItems(ctx.author.id, "liked") # Request
        if playlistSize >= 25:
            return await ctx.send(f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist (liked) is full (25 songs)!")
        DBPlaylist(self.bot.dbConnection).add(ctx.author.id, "liked", track.title, track.uri) # Request

        embed=discord.Embed(title="Song added in your playlist", description=f"- **[{track.title}]({track.uri})**", color=discord.Colour.random())
        embed.add_field(name="playlist name :", value=f"`liked`", inline=True)
        embed.add_field(name="playlist size :", value=f"`{playlistSize+1}/25`", inline=True)
        embed.set_thumbnail(url=track.thumb)
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    
    @playlist.command(name = "show",
                    aliases=["display"],
                    usage="",
                    description = "Show your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_show(self, ctx):
        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, "liked") # Request

        if len(playlistContent) <= 0:
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist (liked) is empty!")

        isFirstMessage = True
        message = ""
        for number, i in enumerate(playlistContent, start=1):
            message += f"**{number}) [{i[2]}]({i[3]})**\n"
            if len(message) > 1800:

                if isFirstMessage:
                    embedTitle = "Liked Playlist :"
                    isFirstMessage = False
                else:
                    embedTitle = ""

                embed=discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
                embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                message = ""
        if len(message) > 0:
            embedTitle = "Liked Playlist :" if isFirstMessage else ""

            embed=discord.Embed(title=embedTitle, description=message, color=discord.Colour.random())
            embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


    @playlist.command(name = "remove",
                    aliases=["delete"],
                    usage="<Index>",
                    description = "Remove a song of your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def playlist_remove(self, ctx, index):
        
        index = int(index) -1
        
        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, "liked") # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist (liked) is empty!")

        if index < 0 or index > (len(playlistContent ) -1):
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} The index is available!")
        DBPlaylist(self.bot.dbConnection).remove(ctx.author.id, "liked", playlistContent[index][3]) # Request

        embed=discord.Embed(title="Song removed from your playlist (liked)", description=f"- **[" + playlistContent[index][2] + "](" + playlistContent[index][3] + ")**", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)


    @playlist.command(name = "load",
                    aliases=[],
                    usage="",
                    description = "Load all songs of your playlist in the queue")
    @commands.guild_only()
    @commands.cooldown(1, 30, commands.BucketType.member)
    async def playlist_load(self, ctx):
        
        playlistContent = DBPlaylist(self.bot.dbConnection).display(ctx.author.id, "liked") # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} Your playlist (liked) is empty!")

        links = [i[3] for i in playlistContent]
        await addTrack(self, ctx, links)


def setup(bot):
    bot.add_cog(CogPlaylist(bot))