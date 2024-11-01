from redbot.core import commands

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!")

    async def ping(self, ctx):
        """This pongs when you ping"""
        await ctx.send("Pong!")

    async def rain(self, ctx):
        """This shows when it will rain next"""
        await ctx.send("Soon!")