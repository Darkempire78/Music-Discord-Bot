import discord
from discord.ext import commands

import wavelink

class CogLavalink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host= self.bot.lavalink.host,
                                              port= self.bot.lavalink.port,
                                              rest_uri= self.bot.lavalink.restUri,
                                              password= self.bot.lavalink.password,
                                              identifier= self.bot.lavalink.identifier,
                                              region= self.bot.lavalink.region)


def setup(bot):
    bot.add_cog(CogLavalink(bot))