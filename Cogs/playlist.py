import discord
from discord.ext import commands

import json
from youtubesearchpython import Video, ResultMode

from DataBase.playlist import DBPlaylist

class CogPlaylist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(name="playlist", invoke_without_command=True)
    async def playlist(self, ctx):
        await ctx.send("playlist")


    @playlist.command(name = "add",
                    aliases=[],
                    usage="<YouTubeLink>",
                    description = "Add a song to your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.member)
    async def playlist_add(self, ctx, link):
        if not link.startswith("https://www.youtube.com/watch"):
            return await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The YouTube link is invalid!")
        # Check if the link exists
        song = Video.get(link, mode = ResultMode.json)
        if not song:
            return await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} The YouTube link is invalid!")
        song = json.loads(song)
        
        playlistSize = DBPlaylist().countPlaylistItems(ctx.author.id, "liked") # Request
        if playlistSize >= 25:
            return await ctx.send(f"<:False:798596718563950653> {ctx.author.mention} Your playlist (liked) is full (25 songs)!")
        DBPlaylist().add(ctx.author.id, "liked", song["title"], link) # Request

        embed=discord.Embed(title="Song added in your playlist", description=f"- **[" + song["title"] + "](" + song["link"] + ")**", color=discord.Colour.random())
        embed.add_field(name="playlist name :", value=f"`liked`", inline=True)
        embed.add_field(name="playlist size :", value=f"`{playlistSize+1}/25`", inline=True)
        embed.set_thumbnail(url=song["thumbnails"][len(song["thumbnails"] )-1]["url"])
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)

    
    @playlist.command(name = "show",
                    aliases=["display"],
                    usage="",
                    description = "Show your playlist")
    @commands.guild_only()
    @commands.cooldown(1, 4, commands.BucketType.member)
    async def playlist_show(self, ctx):
        playlistContent = DBPlaylist().display(ctx.author.id, "liked") # Request

        if len(playlistContent) <= 0:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} Your playlist (liked) is empty!")

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
    @commands.cooldown(1, 4, commands.BucketType.member)
    async def playlist_remove(self, ctx, index):
        
        index = int(index) -1
        
        playlistContent = DBPlaylist().display(ctx.author.id, "liked") # Request
        if len(playlistContent) <= 0:
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} Your playlist (liked) is empty!")

        if index < 0 or index > (len(playlistContent ) -1):
            return await ctx.channel.send(f"<:False:798596718563950653> {ctx.author.mention} The index is available!")
        DBPlaylist().remove(ctx.author.id, "liked", playlistContent[index][3]) # Request

        embed=discord.Embed(title="Song removed from your playlist (liked)", description=f"- **[" + playlistContent[index][2] + "](" + playlistContent[index][3] + ")**", color=discord.Colour.random())
        embed.set_footer(text=f"Requested by {ctx.author} | Open source", icon_url=ctx.author.avatar_url)
        await ctx.channel.send(embed=embed)
        


def setup(bot):
    bot.add_cog(CogPlaylist(bot))