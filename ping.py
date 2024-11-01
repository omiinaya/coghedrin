from redbot.core import commands

class MyCog(commands.Cog):
    """My ping pong cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("pong")