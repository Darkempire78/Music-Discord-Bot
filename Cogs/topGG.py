from discord.ext import commands

import dbl


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = self.bot.dblToken
        self.dblpy = dbl.DBLClient(
            self.bot, self.token, autopost=True # Autopost will post your guild count every 30 minutes
            # webhook_path=bot.dblWebhookPath, webhook_auth=bot.dblWebhookAuth
        )  

    # @commands.Cog.listener()
    # async def on_guild_post(self):
    #     print("Server count posted successfully")

    @commands.Cog.listener()
    async def on_dbl_vote(data):
        print("New vote", data)


def setup(bot):
    bot.add_cog(TopGG(bot))