import discord
import asyncio

from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound

# ------------------------ COGS ------------------------ #  

class EventsCog(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            jour = round(error.retry_after/86400)
            heure = round(error.retry_after/3600)
            minute = round(error.retry_after/60)
            if jour > 0:
                await ctx.send('This command has a cooldown, be sure to wait for '+str(jour)+ "day(s)")
            elif heure > 0:
                await ctx.send('This command has a cooldown, be sure to wait for '+str(heure)+ " hour(s)")
            elif minute > 0:
                await ctx.send('This command has a cooldown, be sure to wait for '+ str(minute)+" minute(s)")
            else:
                await ctx.send(f'This command has a cooldown, be sure to wait for {error.retry_after:.2f} second(s)')
        elif isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingPermissions):
            await ctx.send(error.text)
        elif isinstance(error, CheckFailure):
            await ctx.send(error.original.text)
        else:
            embed = discord.Embed(title=f"__**COMMAND ERROR**__", description=f"[**GitHub**](https://github.com/Darkempire78/Music-Discord-Bot)\n\n**You may repport this issue on the [GitHub repository](https://github.com/Darkempire78/Music-Discord-Bot)**\n```{error}```", color=discord.Colour.red())
            embed.set_footer(text="Bot Created by Darkempire#8245")
            await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member != self.bot.user:
            return

        # If the bot is disconnected
        if (before.channel is not None) and (after.channel is None):
            self.bot.music[before.channel.guild.id]["musics"] = []
            self.bot.music[before.channel.guild.id]["volume"] = 0.5
            self.bot.music[before.channel.guild.id]["skip"] = {"count": 0, "users": []}
            self.bot.music[before.channel.guild.id]["nowPlaying"] = None
            self.bot.music[before.channel.guild.id]["loop"] = None
        elif (before.channel is  None) and (after.channel is not None):
            self.bot.music[after.channel.guild.id]["musics"] = []
            self.bot.music[after.channel.guild.id]["volume"] = 0.5
            self.bot.music[after.channel.guild.id]["skip"] = {"count": 0, "users": []}
            self.bot.music[after.channel.guild.id]["nowPlaying"] = None
            self.bot.music[after.channel.guild.id]["loop"] = None

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(EventsCog(bot))