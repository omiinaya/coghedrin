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

def setup(bot):
    bot.add_cog(MyCog(bot))