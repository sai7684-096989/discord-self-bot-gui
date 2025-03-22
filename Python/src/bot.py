import discord
from discord.ext import commands
import asyncio

class DiscordSelfBot:
    def __init__(self, token):
        self.token = token
        self.bot = commands.Bot(command_prefix="!", self_bot=True)
        self.is_ready = False  # Flag to check if the bot is ready

        @self.bot.event
        async def on_ready():
            print(f"Logged in as {self.bot.user.name}, ready to fuck shit up!")
            self.is_ready = True

    def run(self):
        try:
            # Create a new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.bot.start(self.token))
        except Exception as e:
            print(f"Failed to login, dipshit: {e}")
            self.is_ready = False

    def is_connected(self):
        return self.is_ready