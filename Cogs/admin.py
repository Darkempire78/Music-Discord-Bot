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
        await ctx.send("<:Alert:804761370125402173> Stoping process...")
        for i in self.bot.voice_clients:
            try:
                await i.disconnect()
                await ctx.send(f"<:True:798596718349385799> Disconected from {i.channel.id} in {i.channel.guild.name}")
                print(f"Disconected from {i.channel.id} in {i.channel.guild.name}")
            except:
                await ctx.send(f"<:False:798596718563950653> **Error :** Can't disconect from {i.channel.id} in {i.channel.guild.name}")
                print(f"Error : Can't disconect from {i.channel.id} in {i.channel.guild.name}")
        await ctx.send(f"<:Alert:804761370125402173> Stoped!")
        print(f"Stoping process... (by {ctx.author})")
        await self.bot.logout() # Stop the bot


def setup(bot):
    bot.add_cog(CogAdmin(bot))