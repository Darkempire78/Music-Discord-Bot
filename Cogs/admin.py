import discord
from discord.ext import commands
import asyncio

class CogAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "logout",
                    usage="",
                    description = "Stop the bot.")
    @commands.is_owner()
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def logout(self, ctx):

        await ctx.send(f"{self.bot.emojiList.alert} Stoping process...")
        for i in self.bot.voice_clients:
            try:
                await i.disconnect()
                await ctx.send(f"{self.bot.emojiList.true} Disconected from {i.channel.id} in {i.channel.guild.name}")
                print(f"Disconected from {i.channel.id} in {i.channel.guild.name}")
            except:
                await ctx.send(f"{self.bot.emojiList.false} **Error :** Can't disconect from {i.channel.id} in {i.channel.guild.name}")
                print(f"Error : Can't disconect from {i.channel.id} in {i.channel.guild.name}")
        await ctx.send(f"{self.bot.emojiList.alert} Stoped!")
        print(f"Stoping process... (by {ctx.author})")
        await self.bot.logout() # Stop the bot

        
        # def closeApp(self, ctx, voice_clients):
        #     if playingWarning[i.channel.id] is True:
        #         playingWarning[i.channel.id] = False
        #     else:
        #         asyncio.run_coroutine_threadsafe(voice_clients.disconnect(), self.bot.loop)
        #         asyncio.run_coroutine_threadsafe(ctx.send(f"{self.bot.emojiList.true} Disconected from {voice_clients.channel.id} in {voice_clients.channel.guild.name}"), self.bot.loop)
        #         print(f"Disconected from {voice_clients.channel.id} in {voice_clients.channel.guild.name}")

        #         if len(self.bot.voice_clients) == 0:
        #             asyncio.run_coroutine_threadsafe(ctx.send(f"{self.bot.emojiList.alert} Stoped!"), self.bot.loop)
        #             print(f"Stoping process... (by {ctx.author})")
        #             asyncio.run_coroutine_threadsafe(self.bot.logout(), self.bot.loop) # Stop the bot

        # await ctx.send(f"{self.bot.emojiList.alert} Stoping process...")
        
        # playingWarning = {}

        # for i in self.bot.voice_clients:
        #     # try:
        #     i.stop()
        #     audio_source = discord.FFmpegPCMAudio("RestartWarning.mp3", before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        #     if not i.is_playing():
        #         playingWarning[i.channel.id] = True
        #         i.play(audio_source, after=closeApp(self, ctx, i))
        # print('test')

        


def setup(bot):
    bot.add_cog(CogAdmin(bot))