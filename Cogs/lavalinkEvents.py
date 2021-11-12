from discord.ext import commands
import wavelink
import sponsorblock as sb
import asyncio
import json

from Tools.playTrack import playTrack

from DataBase.Queue import DBQueue
from DataBase.Server import DBServer
from DataBase.Skip import DBSkip


class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get('requester')


class CogLavalinkEvents(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot

    @wavelink.WavelinkMixin.listener('on_track_start')
    async def on_track_start(self, node: wavelink.Node, payload):

        with open("configuration.json", "r") as config:
            data = json.load(config)
            sponsorblock = data["sponsorblock"]
            
        # Sponsorblock
        if sponsorblock:
            currentTrack = DBQueue(self.bot.dbConnection).getCurrentSong(payload.player.guild_id)[4]
            sbClient = sb.Client()
            segments = None

            try:
                segments = sbClient.get_skip_segments(currentTrack, category="music_offtopic")
            except:
                pass

            while True:
                # Stop if it's another track
                track = DBQueue(self.bot.dbConnection).getCurrentSong(payload.player.guild_id)[4]
                if track != currentTrack:
                    break
                
                currentPosition = payload.player.position
                if segments:
                    for segment in segments:
                        if currentPosition >= segment.start*1000 and currentPosition <= segment.end*1000:
                            await payload.player.seek(segment.end*1000)
                await asyncio.sleep(0.5)

    @wavelink.WavelinkMixin.listener('on_track_stuck')
    @wavelink.WavelinkMixin.listener('on_track_end')
    @wavelink.WavelinkMixin.listener('on_track_exception')
    async def on_player_stop(self, node: wavelink.Node, payload):
           
        serverParameters = DBServer(self.bot.dbConnection).displayServer(payload.player.guild_id)
        isLoop = serverParameters[2]
        isLoopQueue = serverParameters[3]

        # Clear the skip DB
        DBSkip(self.bot.dbConnection).clear(payload.player.guild_id)

        if isLoop == 1:
            currentTrack = DBQueue(self.bot.dbConnection).getCurrentSong(payload.player.guild_id)
            requester = currentTrack[2]
            channelID = currentTrack[3]
            channel = self.bot.get_channel(int(channelID))
            track = await self.bot.wavelink.get_tracks(currentTrack[4])
            track = track[0]
            await channel.send(f"🔄 Looped!")
            return await playTrack(self, channel, payload.player, track, requester)
        
        # If not looped
        track = DBQueue(self.bot.dbConnection).getNextSong(payload.player.guild_id)
        if track is None:
            currentTrack = DBQueue(self.bot.dbConnection).getCurrentSong(payload.player.guild_id)
            if currentTrack:
                channelID = currentTrack[3]
                channel = self.bot.get_channel(int(channelID))
                if channel:
                    await channel.send(f"{self.bot.emojiList.false} Disconnected because the queue is empty!")
                    await payload.player.disconnect()
            return 

        channelID = track[3]
        channel = self.bot.get_channel(int(channelID))
        requester = track[2]
        track = track[4]

        # Remove the former track
        DBQueue(self.bot.dbConnection).removeFormer(payload.player.guild_id)
        # update playing track to former track (index = 0)
        DBQueue(self.bot.dbConnection).updatePlayingToFormer(payload.player.guild_id)
        # Change the new track to isPlaying
        trackIndex = DBQueue(self.bot.dbConnection).getNextIndex(payload.player.guild_id)
        DBQueue(self.bot.dbConnection).setIsPlaying(payload.player.guild_id, trackIndex)

        await playTrack(self, channel, payload.player, track, requester)

        if isLoopQueue == 1:
            formerTrack = DBQueue(self.bot.dbConnection).displayFormer(payload.player.guild_id)

            if len(formerTrack) > 0:
                futureIndex = DBQueue(self.bot.dbConnection).getFutureIndex(payload.player.guild_id)
                futureIndex += 1

                title = formerTrack[5]
                duration = formerTrack[6]

                # Add the former track at the end of the queue
                DBQueue(self.bot.dbConnection).add(payload.player.guild_id, False, requester, channel.id, track, title, duration, futureIndex)


    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node: wavelink.Node):
        print(f'Lavalink node {node.identifier} is ready!')

        # Restart the queue and playing music
        # with open("logoutData.json", "r") as logoutData:
        #     logoutData = json.load(logoutData)

        # serversInQueue = DBQueue(self.bot.dbConnection).displayAllPlaying()

        # if serversInQueue:
        #     for server in serversInQueue:
        #         serverID = int(server[0])
        #         if str(serverID) in logoutData:
        #             voiceChannelID = logoutData[str(serverID)]
        #             voiceChannel = self.bot.get_channel(int(voiceChannelID))
        #             if voiceChannel:
        #                 # Get the track
        #                 track = await node.get_tracks(server[4])
        #                 if track:
        #                     track = track[0]
        #                     track = Track(track.id, track.info, requester=server[2])
                            
        #                     # Play the track
        #                     player = node.get_player(serverID)
        #                     if player:
        #                         await player.play(track)

    
def setup(bot):
    bot.add_cog(CogLavalinkEvents(bot))