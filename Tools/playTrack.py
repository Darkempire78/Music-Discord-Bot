import discord
import asyncio

from Tools.sendPlayingSongEmbed import sendPlayingSongEmbed

def playTrack(self, ctx, client, queue, music):
    self.bot.music[ctx.guild.id]["source"] = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(music.streamUrl, 
            before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

    def next(_):
        if self.bot.music[ctx.guild.id]["loop"] and self.bot.music[ctx.guild.id]["nowPlaying"]:
            asyncio.run_coroutine_threadsafe(ctx.channel.send(f"🔄 Looped!"), self.bot.loop)
            playTrack(self, ctx, client, queue, self.bot.music[ctx.guild.id]["nowPlaying"])
            
        else:
            if len(queue) > 0:
                new_music = queue[0]
                del queue[0]
                playTrack(self, ctx, client, queue, new_music)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(), self.bot.loop)
                self.bot.music[ctx.guild.id]["nowPlaying"] = None
                self.bot.music[ctx.guild.id]["skip"] = {"count": 0, "users": []}
                asyncio.run_coroutine_threadsafe(ctx.channel.send(f"Disconnected!"), self.bot.loop)

    client.play(self.bot.music[ctx.guild.id]["source"], after=next)
    sendPlayingSongEmbed(self, ctx, music) # Send message
    self.bot.music[ctx.guild.id]["nowPlaying"] = music # Update nowPlawing