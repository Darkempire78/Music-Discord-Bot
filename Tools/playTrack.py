import discord
import asyncio

from Tools.sendPlayingSongEmbed import sendPlayingSongEmbed

def playTrack(self, ctx, client, music):
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music["music"].streamUrl, 
            before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), self.bot.music[ctx.guild.id]["volume"])

    def nextSong(_):
        if self.bot.music[ctx.guild.id]["loop"] and self.bot.music[ctx.guild.id]["nowPlaying"]:
            asyncio.run_coroutine_threadsafe(ctx.channel.send(f"🔄 Looped!"), self.bot.loop)
            playTrack(self, ctx, client, self.bot.music[ctx.guild.id]["nowPlaying"])
            
        else:
            queue = self.bot.music[ctx.guild.id]["musics"]
            if len(queue) > 0:
                new_music = queue[0]
                del queue[0]
                playTrack(self, ctx, client, new_music)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)
                self.bot.music[ctx.guild.id]["nowPlaying"] = None
                self.bot.music[ctx.guild.id]["skip"] = {"count": 0, "users": []}
                self.bot.music[ctx.guild.id]["volume"] = 0.5
                asyncio.run_coroutine_threadsafe(ctx.channel.send(f"Disconnected because the queue is empty!"), self.bot.loop)

    client.play(source, after=nextSong)
    sendPlayingSongEmbed(self, ctx, music) # Send message
    self.bot.music[ctx.guild.id]["nowPlaying"] = {
        "music": music["music"],
        "requestedBy": music["requestedBy"]
    } # Update nowPlawing