import discord

from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, MissingPermissions, CommandNotFound, MissingRequiredArgument, ExpectedClosingQuoteError, BotMissingPermissions

import traceback
import sys
import datetime

from Tools.Utils import Utils

from DataBase.Server import DBServer
from DataBase.Queue import DBQueue

# ------------------------ COGS ------------------------ #  

class EventsCog(commands.Cog, name="EventsCog"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------- #

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return
        if isinstance(error, CommandOnCooldown):
            jour = round(error.retry_after/86400)
            heure = round(error.retry_after/3600)
            minute = round(error.retry_after/60)
            if jour > 0:
                return await ctx.send(f'{ctx.author.mention} This command has a cooldown, be sure to wait for '+str(jour)+ "day(s)")
            if heure > 0:
                return await ctx.send(f'{ctx.author.mention} This command has a cooldown, be sure to wait for '+str(heure)+ " hour(s)")
            if minute > 0:
                return await ctx.send(f'{ctx.author.mention} This command has a cooldown, be sure to wait for '+ str(minute)+" minute(s)")
            return await ctx.send(f'{ctx.author.mention} This command has a cooldown, be sure to wait for {error.retry_after:.2f} second(s)')
        if isinstance(error, BotMissingPermissions):
            missing = ", ".join(error.missing_perms)
            return await ctx.send(f"{ctx.author.mention} I need the `{missing}` permission(s) to run this command.")
        if isinstance(error, MissingPermissions):
            missing = ", ".join(error.missing_perms)
            return await ctx.send(f"{ctx.author.mention} You need the `{missing}` permission(s) to run this command.")
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(f"{ctx.author.mention} Required argument is missed!\nUse this model : `{self.bot.command_prefix}{ctx.command.name} {ctx.command.usage}`")
        if isinstance(error, ExpectedClosingQuoteError):
            return await ctx.send(f"{ctx.author.mention} Your request cannot only contain `{error.close_quote}`")
        
        embed = discord.Embed(title=f"__**COMMAND ERROR**__", description=f"[**GitHub**](https://github.com/Darkempire78/Music-Discord-Bot)\n\n**You may report this issue on the [GitHub repository](https://github.com/Darkempire78/Music-Discord-Bot)**\n```{error}```", color=discord.Colour.red())
        embed.set_footer(text="Bot Created by Darkempire#8245")
        try:
            await ctx.channel.send(embed=embed)
        except:
            pass

        # Send the error on the support server 
        channel = self.bot.get_channel(800839028659453952)
        if channel is not None:
            try:
                invite = await ctx.guild.channels[0].create_invite()
            except:
                invite = None
            embed = discord.Embed(title=f"**ERROR :**", description=f"**Date :** " + datetime.datetime.now().strftime("%x at %X") + f"\n**Command name :** {ctx.command.name}\n**Server link :** <{invite}>\n\n```{error}```", color=discord.Colour.red())
            embed.set_footer(text=f"Server : {ctx.guild.name} - {ctx.guild.id} | Author : {ctx.author} - {ctx.author.id}")
            await channel.send(embed=embed)

            print("\n\n⚠️⚠️⚠️ " + datetime.datetime.now().strftime("%x at %X") + " Ignoring exception in command {}\n:".format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        
        # If the bot leave a voice channel
        if (before.channel is not None) and (after.channel is None):
            if member == self.bot.user:

                player = self.bot.wavelink.get_player(before.channel.guild.id)
                if player.is_playing:
                    await player.destroy()
                DBQueue(self.bot.dbConnection).clear(before.channel.guild.id)
                DBServer(self.bot.dbConnection).clearMusicParameters(before.channel.guild.id, False, False)

        if (before.channel is not None) and (after.channel is not before.channel):
            if (
                (self.bot.user.id in before.channel.voice_states.keys() and 
                len(before.channel.voice_states) == 1) 
                or 
                (member == self.bot.user)
            ):
                if member != self.bot.user:
                    player = self.bot.wavelink.get_player(before.channel.guild.id)
                    await player.disconnect()
                
                DBServer(self.bot.dbConnection).clearMusicParameters(before.channel.guild.id, False, False)

        # If the bot join a voice channel
        elif (before.channel is None) and (after.channel is not None):
            if member == self.bot.user:

                DBServer(self.bot.dbConnection).clearMusicParameters(after.channel.guild.id, False, False)


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        
        DBServer(self.bot.dbConnection).add(guild.id, "?", False, False, "")

        # Print the log on the support server
        channel = self.bot.get_channel(799998669926563860)
        if channel is not None:
            await channel.send(f":green_circle: Joined a server: {guild.name} ({guild.id})")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        DBServer(self.bot.dbConnection).remove(guild.id)

        # Print the log on the support server
        channel = self.bot.get_channel(799998669926563860)
        if channel is not None:
            await channel.send(f":red_circle: Left a server: {guild.name} ({guild.id})")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        # If the bot is mentioned
        if self.bot.user in message.mentions:
            await message.channel.send(f"{message.author.mention} My prefix on this server is : `{self.bot.command_prefix}`", delete_after=10)


# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.add_cog(EventsCog(bot))