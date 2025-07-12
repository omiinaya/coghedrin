import random
import requests
import os
import discord
from dotenv import load_dotenv
from redbot.core import commands
from datetime import datetime
import logging
from typing import Optional
from .utils import is_valid_member
from .api_helpers import fetch_json
from .localization import t

# Load environment variables from .env file
load_dotenv()
logger = logging.getLogger("red.coghedrin.mycog")

class MyCog(commands.Cog):
    """My custom cog with fun commands and best practices."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pinghedrin(self, ctx: commands.Context, lang: str = 'en') -> None:
        """Responds with Pong! for health check. (5s cooldown per user, supports localization)"""
        await ctx.send(t('pong', lang=lang))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def roll(self, ctx: commands.Context, lang: str = 'en') -> None:
        """Roll a random number from 1-100. (5s cooldown per user, supports localization)"""
        random_number = random.randint(1, 100)
        await ctx.send(t('roll', lang=lang, user=ctx.author.mention, number=random_number))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dice(self, ctx: commands.Context) -> None:
        """Roll a random number from 1-6. (5s cooldown per user)"""
        random_number = random.randint(1, 6)
        await ctx.send(f"{ctx.author.mention}, you rolled a {random_number}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rps(self, ctx: commands.Context, opponent: commands.MemberConverter) -> None:
        """Play Rock-Paper-Scissors against another player. (10s cooldown per user)"""
        try:
            valid, error = is_valid_member(ctx, opponent)
            if not valid:
                await ctx.send(error)
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
        except Exception as e:
            logger.error(f"Error in rps command: {e}")
            await ctx.send(f"Error: {e}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def apicall(self, ctx: commands.Context, url: Optional[str] = None) -> None:
        """Makes an API call and returns the response. Optionally takes a URL argument. (10s cooldown per user)"""
        api_url = url or os.getenv('SAMPLE_API')
        if not api_url or not api_url.startswith(('http://', 'https://')):
            await ctx.send("API URL not configured or invalid. Please set SAMPLE_API in your .env file or provide a valid URL.")
            return
        try:
            response = requests.get(api_url, timeout=10)
            logger.info(f"API call to {api_url} returned status {response.status_code}")
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    data = response.json()
                    message = f"API Response: {data}"
                else:
                    data = response.text
                    message = f"API Response: {data}"
                if len(message) > 1800:
                    message = message[:1800] + '... (truncated)'
                await ctx.send(message)
            else:
                await ctx.send(f"Failed to retrieve data from the API. Status: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"API call failed: {e}")
            await ctx.send(f"API call failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in apicall: {e}")
            await ctx.send(f"Unexpected error: {e}")
    
    @commands.command()
    async def weather(self, ctx):
        """Returns the current weather type for Eastern Americas and time until the next weather type."""
        url = os.getenv('WEATHER_API')
        data = fetch_json(url)
        if data:
            eastern_america_data = data[0]['data']['Eastern Americas']
            current_weather, time_until_next, next_weather = self.get_current_weather(eastern_america_data)
            message = f"Current weather is '{current_weather}'. Time until '{next_weather}' is {time_until_next}."
        else:
            message = "Failed to retrieve data from the API."
        await ctx.send(message)

    @commands.command()
    async def timeofday(self, ctx):
        """Returns the current time of day for Eastern Americas and time until the next one."""
        url = os.getenv('DAYNIGHT_API')
        data = fetch_json(url)
        if data:
            eastern_america_data = data[0]['data']['Eastern Americas']
            current_time_of_day, time_until_next, next_time_of_day = self.get_current_time_of_day(eastern_america_data)
            message = f"Current time of day is '{current_time_of_day}'. Time until '{next_time_of_day}' is {time_until_next}."
        else:
            message = "Failed to retrieve data from the API."
        await ctx.send(message)

    @commands.command()
    async def when(self, ctx, condition: str, lang: str = 'en'):
        """Tells how long until the specified condition (day, night, normal, rain) or if it's already that condition. (supports localization)"""
        condition = condition.lower()
        if condition not in ["day", "night", "rain"]:
            await ctx.send(t('invalid_condition', lang=lang))
            return
        if condition in ["day", "night"]:
            url = os.getenv('DAYNIGHT_API')
            data = fetch_json(url)
            if data:
                eastern_america_data = data[0]['data']['Eastern Americas']
                current_time_of_day, time_until_next, next_time_of_day = self.get_current_time_of_day(eastern_america_data)
                if current_time_of_day.lower() == condition:
                    message = f"It's currently '{condition}' already."
                else:
                    message = f"Time until '{condition}' is {time_until_next}."
            else:
                message = "Failed to retrieve data from the API."
        else:
            url = os.getenv('WEATHER_API')
            data = fetch_json(url)
            if data:
                eastern_america_data = data[0]['data']['Eastern Americas']
                current_weather, time_until_next, next_weather = self.get_current_weather(eastern_america_data)
                if current_weather.lower() == condition:
                    message = f"It's currently '{condition}'."
                else:
                    message = f"Time until '{condition}' is {time_until_next}."
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
                await ctx.send(f"You are dead. ({outcome})")
            else:
                # 5/6 chance to survive and show the roll number
                await ctx.send(f"You have survived! ({outcome})")
                
        except Exception as e:
            await ctx.send(f"Error in roulette command: {str(e)}")
            return

    @commands.command()
    async def slots(self, ctx):
        """Play a slot machine game with Discord emojis"""
        # Define the slot machine emojis
        emojis = [":cherries:", ":lemon:", ":strawberry:", ":grapes:", ":seven:", ":bell:"]
        
        # Spin the slots
        slot1 = random.choice(emojis)
        slot2 = random.choice(emojis)
        slot3 = random.choice(emojis)
        
        # Display the result
        result = f"{slot1} | {slot2} | {slot3}"
        
        # Check for a win (all three slots are the same)
        if slot1 == slot2 == slot3:
            message = f"{ctx.author.mention}, Jackpot! You won!"
        else:
            message = f"{ctx.author.mention}, Better luck next time!"
        
        await ctx.send(f"{result}\n{message}")

    @commands.command()
    async def coinflip(self, ctx, bet_on: str = None):
        """Play text-based coin flip game"""
        
        if not bet_on:
            await ctx.send("Please specify either 'even' or 'odd'.")
            return
        
        try:
            outcome = random.randint(1, 2)
            if outcome == 1:
                result = "odd"
            else:
                result = "even"

            # Determine outcome based on user's bet
            if bet_on.lower() == result:
                await ctx.send(f"You won! ({result})")
            else:
                await ctx.send(f"You lost. ({result})")
                return
                
        except Exception as e:
            await ctx.send(f"Error in coinflip command: {str(e)}")
            return

    @commands.command()
    async def decide(self, ctx):
        if random.random() < 0.5:
            await ctx.send("yes")
        else:
            await ctx.send("no")

    @commands.command()
    async def balding(self, ctx):
        """Returns a random balding percentage."""
        percent = random.randint(0, 100)
        if percent == 0:
            await ctx.send("Congratz! You're not balding.")
        else:
            await ctx.send(f"{ctx.author.mention} is {percent}% balding. o7")

def setup(bot):
    bot.add_cog(MyCog(bot))