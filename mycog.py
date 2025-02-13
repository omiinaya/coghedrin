import random
import requests
import os
from dotenv import load_dotenv
from redbot.core import commands
from datetime import datetime

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
    
    @commands.command()
    async def weather(self, ctx):
        """Returns the current weather type for Eastern Americas and time until the next weather type."""
        url = os.getenv('WEATHER_API')
        response = requests.get(url)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            
            if 'application/json' in content_type:
                data = response.json()
                eastern_america_data = data[0]['data']['Eastern Americas']
                current_weather, time_until_next = self.get_current_weather(eastern_america_data)
                message = f"Current weather is '{current_weather}'. Time until next weather type: {time_until_next}."
            else:
                message = "The API did not return JSON data."
            
            await ctx.send(message)
        else:
            await ctx.send("Failed to retrieve data from the API.")

    def format_eastern_america_data(self, data):
        """Formats the Eastern Americas data with readable timestamps."""
        formatted_message = "**Eastern Americas Weather Data**\n"
        for forecast in data:
            timestamp = forecast['ts']
            condition = forecast['condition']
            readable_time = datetime.fromtimestamp(timestamp // 1000).strftime('%I:%M %p')
            formatted_message += f"- {readable_time}: {condition}\n"
        return formatted_message

    def get_current_weather(self, data):
        """Determines the current weather type and time until the next weather type based on the provided data."""
        current_time = datetime.now().timestamp()
        current_weather = "Unknown"
        time_until_next = "Unknown"
        
        for i, forecast in enumerate(data):
            forecast_time = forecast['ts'] // 1000
            if forecast_time <= current_time:
                current_weather = forecast['condition'].replace("EWeatherType::", "")
                if i + 1 < len(data):
                    next_forecast_time = data[i + 1]['ts'] // 1000
                    time_until_next_seconds = next_forecast_time - current_time
                    hours, remainder = divmod(time_until_next_seconds, 3600)
                    minutes = remainder // 60
                    if hours > 0:
                        time_until_next = f"{int(hours)} hours and {int(minutes)} minutes"
                    else:
                        time_until_next = f"{int(minutes)} minutes"
                else:
                    time_until_next = "N/A"
            else:
                break
        
        return current_weather, time_until_next

def setup(bot):
    bot.add_cog(MyCog(bot))