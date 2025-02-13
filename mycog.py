import requests
from redbot.core import commands

class MyCog(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycom(self, ctx):
        """This does stuff!"""
        await ctx.send("I can do stuff!")

    @commands.command()
    async def pinghedrin(self, ctx):
        """This pongs when you ping"""
        await ctx.send("Pong!")

    @commands.command()
    async def rain(self, ctx):
        """This shows when it will rain next"""
        await ctx.send("Soon!")

    @commands.command()
    async def dice(self, ctx):
        """This rolls from 1-100"""
        random_number = random.randint(1, 100)
        await ctx.send(f"{ctx.author.mention}, you rolled a {random_number}")

    @commands.command()
    async def rps(self, ctx, opponent: commands.MemberConverter):
        """Play Rock-Paper-Scissors against another player"""
        if opponent == ctx.author:
            await ctx.send("You can't play against yourself!")
            return

        choices = ["rock", "paper", "scissors"]
        user_choice = random.choice(choices)
        opponent_choice = random.choice(choices)

        result = None
        if user_choice == opponent_choice:
            result = "It's a draw!"
        elif (user_choice == "rock" and opponent_choice == "scissors") or \
             (user_choice == "scissors" and opponent_choice == "paper") or \
             (user_choice == "paper" and opponent_choice == "rock"):
            result = f"{ctx.author.mention} wins!"
        else:
            result = f"{opponent.mention} wins!"

        await ctx.send(
            f"{ctx.author.mention} chose {user_choice}. {opponent.mention} chose {opponent_choice}. {result}"
        )

    @commands.command()
    async def api_request(self, ctx):
        """Makes an API request to the specified address"""
        url = "http://n8n.mrxlab.net/webhook/396e8d5d-80c3-4dfc-8760-7963eb2d9d6b"
        response = requests.get(url)
        
        if response.status_code == 200:
            await ctx.send("API request successful!")
        else:
            await ctx.send("Failed to make API request.")

def setup(bot):
    bot.add_cog(MyCog(bot))
