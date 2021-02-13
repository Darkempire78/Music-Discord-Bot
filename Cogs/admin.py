import discord
from discord.ext import commands

import json

from DataBase.Queue import DBQueue

class CogAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name = "logout",
                    usage="",
                    description = "Stop the bot.")
    @commands.is_owner()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.member)
    async def logout(self, ctx):

        await ctx.send(f"{self.bot.emojiList.alert} Stoping process...")

        serversInQueue = DBQueue(self.bot.dbConnection).displayAllPlaying()

        if serversInQueue:
            for server in serversInQueue:
                textChannel = self.bot.get_channel(int(server[3]))
                await textChannel.send(f"{self.bot.emojiList.alert} **THE BOT WILL RESTART !**")

        with open("logoutData.json", "w+") as logoutData:
            data = {}
            for k, player in self.bot.wavelink.players.items():
                try:
                    # Write in logoutData.json
                    data[player.guild_id] = player.channel_id

                    if player.is_playing:
                        await player.destroy()
                    await player.disconnect()
                    await ctx.send(f"{self.bot.emojiList.true} Disconected from {player.guild_id}")
                    print(f"Disconected from {player.guild_id}")
                except:
                    await ctx.send(f"{self.bot.emojiList.false} **Error :** Can't disconect from {player.guild_id}")
                    print(f"Error : Can't disconect from {player.guild_id}")

            data = json.dumps(data, indent=4, ensure_ascii=False)
            logoutData.write(data)
        
        await ctx.send(f"{self.bot.emojiList.alert} Stoped!")
        print(f"\n⛔⛔⛔ Stoping process... (by {ctx.author})")
        await self.bot.logout() # Stop the bot    


def setup(bot):
    bot.add_cog(CogAdmin(bot))