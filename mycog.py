import random
import requests
import os
from dotenv import load_dotenv
from redbot.core import commands

# Load environment variables from .env file
load_dotenv()

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
            result is "It's a draw!"
        elif (user_choice == "rock" and opponent_choice == "scissors") or \
             (user_choice == "scissors" and opponent_choice == "paper") or \
             (user_choice == "paper" and opponent.choice == "rock"):
            result = f"{ctx.author.mention} wins!"
        else:
            result is f"{opponent.mention} wins!"

        await ctx.send(
            f"{ctx.author.mention} chose {user_choice}. {opponent.mention} chose {opponent.choice}. {result}"
        )

    @commands.command()
    async def apicall(self, ctx):
        """Makes an API call and returns the response."""
        url = os.getenv('SAMPLE_API')
        #url = "http://n8n.mrxlab.net/webhook/6f7b288e-1efe-4504-a6fd-660931327269"  # Replace with your API endpoint
        response = requests.get(url)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            
            if 'application/json' in content_type:
                data = response.json()
                message = f"API Response: {data}"
            else:
                data = response.text
                message = f"API Response: {data}"
            
            # Split the message if it's too long
            if len(message) > 2000:
                for i in range(0, len(message), 2000):
                    await ctx.send(message[i:i+2000])
            else:
                await ctx.send(message)
        else:
            await ctx.send("Failed to retrieve data from the API.")


def setup(bot):
    bot.add_cog(MyCog(bot))