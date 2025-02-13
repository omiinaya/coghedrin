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
    async def weather(self, ctx):
        """Fetch weather data from an API"""
        url = "https://throneandliberty.gameslantern.com/api/weather"
        headers = {
            "accept": "application/json, text/plain, */*",
            "x-requested-with": "XMLHttpRequest",
            "x-xsrf-token": "eyJpdiI6Ijl4YlFub0pZVUFzZFkzV1hpY1YvVmc9PSIsInZhbHVlIjoiZUlINVl3ektwSEFVQ3MxcU56YWJWUzZZTGJCVE5pb2JIbHBGOG9ZR2M3SE5OM2JUaVE4V1V4UXUxcm41M2I5OG5QODd5WEs0RlhnZUx5TldKQXpSWjlQUGtySlBKY1hwT1R6UjVDQTl5TnVSdUdmWXIvMzhuajV5aTB4TUZldHgiLCJtYWMiOiI0ZDdlNDQ5M2U3NzIxNTI1NGJhOTkyYzliMTFjNWZkNzc0OWUzYjdmYWE1NDZmY2E1NjYxMGQyODE4ZTBkNzIwIiwidGFnIjoiIn0="
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            await ctx.send(f"Weather data: {data}")
        except requests.RequestException as e:
            await ctx.send(f"Failed to fetch weather data: {e}")

def setup(bot):
    bot.add_cog(MyCog(bot))
