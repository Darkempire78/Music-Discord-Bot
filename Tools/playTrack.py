import discord
import wavelink

from Tools.sendPlayingSongEmbed import sendPlayingSongEmbed

from DataBase.Queue import DBQueue

class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get('requester')


async def playTrack(self, channel, player, track, requester):
    if player.is_playing:
        return

    if isinstance(track, str):
        # Convert the link in a track
        track = await self.bot.wavelink.get_tracks(track)
        track = track[0]
        if track is None:
            return await channel.send(f"{self.bot.emojiList.false} The song link is invalid!")

    # Add the requester
    track = Track(track.id, track.info, requester=requester)

    await player.play(track)
    
    # Send the embed
    await sendPlayingSongEmbed(self, channel, track)