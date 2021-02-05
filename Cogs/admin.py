import discord
from discord.ext import commands


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


def setup(bot):
    bot.add_cog(CogAdmin(bot))