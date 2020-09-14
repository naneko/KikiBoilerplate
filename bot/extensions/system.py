import logging

from discord.ext import commands

log = logging.getLogger(__name__)


class System(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def upgrade(self, ctx: commands.context):
        from git import Repo

        with ctx.channel.typing():
            log.warning("Upgrading bot from git repo")
            repo = Repo("..")
            o = repo.remotes.origin
            o.pull()

        log.info(f"Pulled update successfully ({repo.heads[0].commit})")

        await ctx.send(
            f"Pulled `{repo.heads[0].commit}` from master branch. Run `;;reload` to complete upgrade."
        )


def setup(bot: commands.bot):
    log.debug("System module loaded")
    bot.add_cog(System(bot))


def teardown(bot):
    log.debug("System module unloaded")
