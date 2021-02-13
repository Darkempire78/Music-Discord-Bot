import discord

from discord.ext import commands

# ------------------------ COGS ------------------------ #  

class HelpCog(commands.Cog, name="help command"):
    def __init__(self, bot):
        self.bot = bot

# ------------------------------------------------------ #  

    @commands.command(name = 'help',
                        usage="(commandName)",
                        description = "Display the help message.")
    @commands.cooldown(1, 3, commands.BucketType.member)
    async def help(self, ctx, commandName=None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    commandName2 = i
                    break 
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            commandName2 = i
                            stop = True
                            break
                if stop:
                    break 

            if commandName2 is None:
                await ctx.channel.send(f"{self.bot.emojiList.false} {ctx.author.mention} No command found!")   
            else:
                embed = discord.Embed(title=f"**{commandName2.name.upper()} COMMAND :**", description="[**GitHub**](https://github.com/Darkempire78/Raid-Protect-Discord-Bot)", color=discord.Colour.random())
                embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                embed.add_field(name=f"**NAME :**", value=f"{commandName2.name}", inline=False)
                aliases = ""
                if len(commandName2.aliases) > 0:
                    for aliase in commandName2.aliases:
                        aliases = aliase
                else:
                    commandName2.aliases = None
                    aliases = None
                embed.add_field(name=f"**ALIASES :**", value=f"{aliases}", inline=False)
                if commandName2.usage is None:
                    commandName2.usage = ""
                embed.add_field(name=f"**USAGE :**", value=f"{self.bot.command_prefix}{commandName2.name} {commandName2.usage}", inline=False)
                embed.add_field(name=f"**DESCRIPTION :**", value=f"{commandName2.description}", inline=False)
                embed.set_footer(text="Bot Created by Darkempire#8245")
                await ctx.channel.send(embed=embed)
        else:
            message1 = (f"""
            **{self.bot.command_prefix}help (command) :** Display the help list or the help data for a specific command.\n
            **{self.bot.command_prefix}support :** Give a link to join the support server.
            **{self.bot.command_prefix}invite :** Give a link to invite the bot.
            **{self.bot.command_prefix}github :** Give the github link of the bot (source code).
            **{self.bot.command_prefix}vote :** Give the Top.gg link to vote for the bot.

            **{self.bot.command_prefix}play <Url/Query> :** Search on youtube and play the music.
            **{self.bot.command_prefix}search <Query> :** Search a song on youtube.
            **{self.bot.command_prefix}nowplaying :** Display data about the current song.
            **{self.bot.command_prefix}join :** Add the bot to your voice channel.
            **{self.bot.command_prefix}leave :** Remove the bot of your voice channel.
            **{self.bot.command_prefix}pause :** Pause the current song.
            **{self.bot.command_prefix}resume :** Resume the current song.
            **{self.bot.command_prefix}volume <0-100> :** Change the bot's volume.
            **{self.bot.command_prefix}queue :** Display the queue.
            **{self.bot.command_prefix}move <IndexFrom> <IndexTo> :** Move a song in the queue.   
            """)

            message2 = (f"""
            **{self.bot.command_prefix}remove <Index> :** Remove the song with its index.
            **{self.bot.command_prefix}clear :** Clear the queue.
            **{self.bot.command_prefix}replay :** Replay the current song.
            **{self.bot.command_prefix}reload :** Reload the current song.
            **{self.bot.command_prefix}loop :** Enable or disable the loop mode.
            **{self.bot.command_prefix}loopqueue :** Enable or disable the loop queue mode.

            **{self.bot.command_prefix}playlist add <Url> :** Add a track to your playlist.
            **{self.bot.command_prefix}playlist remove <Index> :** Remove a track to your playlist.
            **{self.bot.command_prefix}playlist display :** Display playlist's songs.
            **{self.bot.command_prefix}playlist load :** Add the whole playlist to the queue.

            **{self.bot.command_prefix}stats :** Display the bot's stats.
            """)

            # **{self.bot.command_prefix}shuffle :** Shuffle the queue.
            # **{self.bot.command_prefix}removedupes :** Remove all duplicates song from the queue.
            # **{self.bot.command_prefix}leavecleanup :** Remove absent user's songs from the queue.

            embed = discord.Embed(title=f"__**Help page of {self.bot.user.name.upper()}**__", description="[**GitHub**](https://github.com/Darkempire78/Music-Discord-Bot)", color=discord.Colour.random())
            embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            embed.add_field(name=f"__COMMANDS :__", value=message1, inline=False)
            embed.set_footer(text="Bot Created by Darkempire#8245")
            await ctx.channel.send(embed=embed)

            embed = discord.Embed(title=f"", description=f"{message2}", color=discord.Colour.random())
            embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            embed.set_footer(text="Bot Created by Darkempire#8245")
            await ctx.channel.send(embed=embed)

# ------------------------ BOT ------------------------ #  

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))