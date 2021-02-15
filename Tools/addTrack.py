import datetime
import discord
import wavelink
import json

from Tools.Check import Check
from Tools.Utils import Utils
from Tools.playTrack import playTrack

from DataBase.Queue import DBQueue
from DataBase.Server import DBServer


async def addTrack(self, ctx, tracks):

    if not await Check().userInVoiceChannel(ctx, self.bot): return 

    # If there is only one track
    if not isinstance(tracks, list):
        tracks = [tracks]

    player = self.bot.wavelink.get_player(ctx.guild.id)

    if not player.is_connected:
        # Clear all the queue
        DBQueue(self.bot.dbConnection).clear(ctx.guild.id)

        channel = ctx.author.voice.channel
        await player.connect(channel.id)
        await ctx.send(f"{ctx.author.mention} Connected in **`{channel.name}`**!")

    playlistMessage = None

    for track in tracks:
        
        tempLink = track
        if isinstance(track, str):
            # Convert the link in a track
            track = await self.bot.wavelink.get_tracks(track)
            track = track[0]
            if track is None:
                return await channel.send(f"{self.bot.emojiList.false} The link `{tempLink}` is invalid!")

        requester = f"{ctx.author.name}#{ctx.author.discriminator}"
        # Add the requester
        if player.is_playing:
            queueSize = DBQueue(self.bot.dbConnection).countQueueItems(ctx.guild.id)
            if queueSize >= 50:
                return await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} You are over the queue limit! The limit of the queue is 50 songs.")
            index = DBQueue(self.bot.dbConnection).getFutureIndex(ctx.guild.id)
            if index is not None:
                index += 1
            # Add to the queue
            DBQueue(self.bot.dbConnection).add(ctx.guild.id, False, requester, ctx.channel.id, track.uri, track.title, track.duration, index) 

            trackDuration = await Utils().durationFormat(track.duration)
            trackTitle = track.title.replace("*", "\\*")

            if len(tracks) == 1:

                # Queue size and duration
                queueSizeAndDuration = DBQueue(self.bot.dbConnection).queueSizeAndDuration(ctx.guild.id)
                if queueSizeAndDuration:
                    queueDuration = int(queueSizeAndDuration[0])
                    queueDuration = await Utils().durationFormat(queueDuration)
                    queueSize = queueSizeAndDuration[1]
                else:
                    queueSize = 0
                    queueDuration = "00:00"

                embed=discord.Embed(title="Song added in the queue", description=f"New song added : **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.random())
                embed.add_field(name="Place in the queue : ", value=f"`{queueSize}`", inline=True)
                embed.add_field(name="Estimated time before playing :", value=f"`{queueDuration}`", inline=True)
                embed.set_thumbnail(url=track.thumb)
                await ctx.channel.send(embed=embed)
            else:
                # If it's a playlist => Update the same message to do not spam the channel
                if playlistMessage is None:
                    embed=discord.Embed(title="Song added in the queue", description=f"- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.random())
                    embed.set_thumbnail(url=track.thumb)
                    playlistMessage = await ctx.channel.send(embed=embed)
                else:
                    # Update the message
                    embedEdited = discord.Embed(title="Songs added in the queue", description= playlistMessage.embeds[0].description + f"\n- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.random())
                    playlistMessage.embeds[0].description = embedEdited.description
                    if len(playlistMessage.embeds[0].description) > 1800:
                        embed=discord.Embed(title="Song added in the queue", description=f"- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.random())
                        embed.set_thumbnail(url=track.thumb)
                        playlistMessage = await ctx.channel.send(embed=embed)
                    else:
                        await playlistMessage.edit(embed=embedEdited)
        else:
            DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)

            DBQueue(self.bot.dbConnection).add(ctx.guild.id, True, requester, ctx.channel.id, track.uri, track.title, track.duration, 1) # Add to the DB
            # Play the track
            await playTrack(self, ctx, player, track, requester)