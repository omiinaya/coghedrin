import random
import requests
import os
import discord
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
    async def pinghedrin(self, ctx):
        """This pongs when you ping"""
        await ctx.send("Pong!")

    @commands.command()
    async def roll(self, ctx):
        """This rolls from 1-100"""
        random_number = random.randint(1, 100)
        await ctx.send(f"{ctx.author.mention}, you rolled a {random_number}")
        
    @commands.command()
    async def dice(self, ctx):
        """This rolls from 1-6"""
        random_number = random.randint(1, 6)
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
                current_weather, time_until_next, next_weather = self.get_current_weather(eastern_america_data)
                message = f"Current weather is '{current_weather}'. Time until '{next_weather}' is {time_until_next}."
            else:
                message = "The API did not return JSON data."
            
            await ctx.send(message)
        else:
            await ctx.send("Failed to retrieve data from the API.")

    @commands.command()
    async def timeofday(self, ctx):
        """Returns the current time of day for Eastern Americas and time until the next one."""
        url = os.getenv('DAYNIGHT_API')
        response = requests.get(url)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            
            if 'application/json' in content_type:
                data = response.json()
                eastern_america_data = data[0]['data']['Eastern Americas']
                current_time_of_day, time_until_next, next_time_of_day = self.get_current_time_of_day(eastern_america_data)
                message = f"Current time of day is '{current_time_of_day}'. Time until '{next_time_of_day}' is {time_until_next}."
            else:
                message = "The API did not return JSON data."
            
            await ctx.send(message)
        else:
            await ctx.send("Failed to retrieve data from the API.")

    @commands.command()
    async def when(self, ctx, condition: str):
        """Tells how long until the specified condition (day, night, normal, rain) or if it's already that condition."""
        condition = condition.lower()
        if condition not in ["day", "night", "rain"]:
            await ctx.send("Invalid condition. Please choose from 'day', 'night', 'normal', or 'rain'.")
            return

        if condition in ["day", "night"]:
            url = os.getenv('DAYNIGHT_API')
            response = requests.get(url)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if 'application/json' in content_type:
                    data = response.json()
                    eastern_america_data = data[0]['data']['Eastern Americas']
                    current_time_of_day, time_until_next, next_time_of_day = self.get_current_time_of_day(eastern_america_data)
                    if current_time_of_day.lower() == condition:
                        message = f"It's currently '{condition}' already."
                    else:
                        message = f"Time until '{condition}' is {time_until_next}."
                else:
                    message = "The API did not return JSON data."
            else:
                message = "Failed to retrieve data from the API."
        else:
            url = os.getenv('WEATHER_API')
            response = requests.get(url)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if 'application/json' in content_type:
                    data = response.json()
                    eastern_america_data = data[0]['data']['Eastern Americas']
                    current_weather, time_until_next, next_weather = self.get_current_weather(eastern_america_data)
                    if current_weather.lower() == condition:
                        message = f"It's currently '{condition}'."
                    else:
                        message = f"Time until '{condition}' is {time_until_next}."
                else:
                    message = "The API did not return JSON data."
            else:
                message = "Failed to retrieve data from the API."

        await ctx.send(message)

    def get_current_weather(self, data):
        """Determines the current weather type and time until the next weather type based on the provided data."""
        current_time = datetime.now().timestamp()
        current_weather = "Unknown"
        time_until_next = "Unknown"
        next_weather = "Unknown"
        
        for i, forecast in enumerate(data):
            forecast_time = forecast['ts'] // 1000
            if forecast_time <= current_time:
                current_weather = forecast['condition'].replace("EWeatherType::", "")
                if i + 1 < len(data):
                    next_forecast_time = data[i + 1]['ts'] // 1000
                    next_weather = data[i + 1]['condition'].replace("EWeatherType::", "")
                    time_until_next_seconds = next_forecast_time - current_time
                    hours, remainder = divmod(time_until_next_seconds, 3600)
                    minutes = remainder // 60
                    if hours > 0:
                        time_until_next = f"{int(hours)} hours and {int(minutes)} minutes"
                    elif minutes > 0:
                        time_until_next = f"{int(minutes)} minutes"
                    else:
                        time_until_next = f"{int(time_until_next_seconds)} seconds"
                else:
                    time_until_next = "N/A"
            else:
                break
        
        return current_weather, time_until_next, next_weather

    def get_current_time_of_day(self, data):
        """Determines the current time of day and time until the next one based on the provided data."""
        current_time = datetime.now().timestamp()
        current_time_of_day = "Unknown"
        time_until_next = "Unknown"
        next_time_of_day = "Unknown"
        
        for i, forecast in enumerate(data):
            forecast_time = forecast['ts'] // 1000
            if forecast_time <= current_time:
                current_time_of_day = forecast['condition']
                if i + 1 < len(data):
                    next_forecast_time = data[i + 1]['ts'] // 1000
                    next_time_of_day = data[i + 1]['condition']
                    time_until_next_seconds = next_forecast_time - current_time
                    hours, remainder = divmod(time_until_next_seconds, 3600)
                    minutes = remainder // 60
                    if hours > 0:
                        time_until_next = f"{int(hours)} hours and {int(minutes)} minutes"
                    elif minutes > 0:
                        time_until_next = f"{int(minutes)} minutes"
                    else:
                        time_until_next = f"{int(time_until_next_seconds)} seconds"
                else:
                    time_until_next = "N/A"
            else:
                break
        
        return current_time_of_day, time_until_next, next_time_of_day
    
    @commands.command()
    async def measure(self, ctx):
        """Responds randomly with 1 - 14 inches."""
        measurement = random.randint(1, 14)
        await ctx.send(f"{ctx.author.mention}, you measured {measurement} inches.")
        
    @commands.command()
    async def secret(self, ctx):
        """Sends a secret message to the user who invoked the command."""
        try:
            await ctx.author.send("This is a secret message just for you!")
            await ctx.send(f"{ctx.author.mention}, check your DMs!")
        except discord.Forbidden:
            await ctx.send(f"{ctx.author.mention}, I couldn't send you a DM. Please check your privacy settings.")
            
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.mentioned_in(message) and not message.author.bot:
            if "ping" in message.content.lower():
                await message.channel.send("pong")
                
    @commands.command()
    async def roulette(self, ctx):
        """Play text-based Russian roulette where you have a 1/6 chance to die"""
        
        try:
            # Determine outcome based on fixed probability
            outcome = random.randint(1, 6)
            
            if outcome == 6:
                # 1/6 chance to die
                await ctx.send(f"There was a bullet in the chamber and you are now dead. ({outcome}.")
            else:
                # 5/6 chance to survive and show the roll number
                await ctx.send(f"There was no bullet in the chamnber and you have survived! ({outcome}).")
                
        except Exception as e:
            await ctx.send(f"Error in roulette command: {str(e)}")
            return


def setup(bot):
    bot.add_cog(MyCog(bot))