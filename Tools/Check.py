import discord
import wavelink

class Check:

    async def userInVoiceChannel(self, ctx, bot):
        """Check if the user is in a voice channel"""
        if ctx.author.voice:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} You are not connected in a voice channel!")
        return False
        
    
    async def botInVoiceChannel(self, ctx, bot):
        """Check if the bot is in a voice channel"""
        player = bot.wavelink.get_player(ctx.guild.id)

        if player.is_connected:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} I'm not connected in a voice channel!")
        return False

    async def botNotInVoiceChannel(self, ctx, bot):
        """Check if the bot is not in a voice channel"""
        player = bot.wavelink.get_player(ctx.guild.id)

        if not player.is_connected:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} I'm already connected in a voice channel!")
        return False
        

    async def userAndBotInSameVoiceChannel(self, ctx, bot):
        """Check if the user and the bot are in the same voice channel"""
        player = bot.wavelink.get_player(ctx.guild.id)

        if (
            (bot.user.id in ctx.author.voice.channel.voice_states) and
            (ctx.author.id in ctx.author.voice.channel.voice_states)
        ):
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} You are not connected in the same voice channel that the bot!")
        return False
    
    async def botIsPlaying(self, ctx, bot):
        """Check if the bot is playing"""
        player = bot.wavelink.get_player(ctx.guild.id)

        if player.is_playing:
            return True
        await ctx.channel.send(f"{bot.emojiList.false} {ctx.author.mention} There is currently no song to replay!")
        return False
        