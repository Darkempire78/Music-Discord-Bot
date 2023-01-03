import datetime
import discord
import wavelink
import json

from Tools.Check import Check
from Tools.Utils import Utils
from Tools.playTrack import playTrack

from DataBase.Queue import DBQueue
from DataBase.Server import DBServer


async def addTrack(self, ctx, playlistLimit, tracks):
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
    embeds = []
    index = None
    queueLengthToAdd = len(tracks)

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
        queueSize = DBQueue(self.bot.dbConnection).countQueueItems(ctx.guild.id)
        if playlistLimit != 0 and queueSize >= playlistLimit:
            await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} You are over the queue limit! The limit of the queue is {playlistLimit} songs.")
            break
        index = DBQueue(self.bot.dbConnection).getFutureIndex(ctx.guild.id)

        if index is None:
            index = 0

        index += 1
        # Add to the queue
        if not player.is_playing:
            DBServer(self.bot.dbConnection).clearMusicParameters(ctx.guild.id, False, False)
            await playTrack(self, ctx, player, track, requester)
        else:
            DBQueue(self.bot.dbConnection).add(ctx.guild.id, False, requester, ctx.channel.id, track.uri, track.title, track.duration, index) 

        trackDuration = await Utils().durationFormat(track.duration)
        trackTitle = track.title.replace("*", "\\*")

        if len(tracks) == 1:
            if queueSizeAndDuration := DBQueue(
                self.bot.dbConnection
            ).queueSizeAndDuration(ctx.guild.id):
                queueDuration = int(queueSizeAndDuration[0])
                queueDuration = await Utils().durationFormat(queueDuration)
                queueSize = queueSizeAndDuration[1]
            else:
                queueSize = 0
                queueDuration = "00:00"

            playlistMessage=discord.Embed(title="Song added in the queue", description=f"New song added : **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.random())
            playlistMessage.add_field(name="Place in the queue : ", value=f"`{queueSize}`", inline=True)
            playlistMessage.add_field(name="Estimated time before playing :", value=f"`{queueDuration}`", inline=True)
            playlistMessage.set_thumbnail(url=track.thumb)
        elif playlistMessage is None:
            playlistMessage = discord.Embed(title="Song added in the queue", description=f"- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.random())
            playlistMessage.set_thumbnail(url=track.thumb)
        elif (
            len(
                f"{playlistMessage.description}\n- **[{trackTitle}]({track.uri})** ({trackDuration})"
            )
            > 4096
        ):
            embeds.append(playlistMessage)
            playlistMessage = discord.Embed(title="Song added in the queue", description=f"- **[{trackTitle}]({track.uri})** ({trackDuration})", color=discord.Colour.random())
            playlistMessage.set_thumbnail(url=track.thumb)
        else:
            playlistMessage = discord.Embed(
                title="Songs added in the queue",
                description=f"{playlistMessage.description}\n- **[{trackTitle}]({track.uri})** ({trackDuration})",
                color=discord.Colour.random(),
            )

    embeds.append(playlistMessage)

    if queueSizeAndDuration := DBQueue(
        self.bot.dbConnection
    ).queueSizeAndDuration(ctx.guild.id):
        queueSize = queueSizeAndDuration[1]
    else:
        queueSize = 0

    if (queueLengthToAdd> 1):
        total=discord.Embed(title=f"{queueLengthToAdd} added, {queueSize} in queue")
    else:
        total = discord.Embed(title="No Songs added to the queue")

    await ctx.channel.send(embed=total)

    for embedMessage in embeds:
        await ctx.channel.send(embed=embedMessage)

