import discord
from discord.ext import commands
import os
import asyncio
import logging
import sys

# Add project root to path to allow imports if running directly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.config import DISCORD_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Myria")

intents = discord.Intents.default()
intents.message_content = True

class MyriaBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Load Cogs
        extensions = [
            "src.bot.cogs.voice_chat",
            "src.bot.cogs.text_chat",
            "src.bot.cogs.system"
        ]
        
        for ext in extensions:
            try:
                await self.load_extension(ext)
                logger.info(f"Loaded extension: {ext}")
            except Exception as e:
                logger.error(f"Failed to load extension {ext}: {e}")

        # Start WebSocket Server
        from ..services.websocket_server import app, WS_HOST, WS_PORT
        import uvicorn
        
        config = uvicorn.Config(app, host=WS_HOST, port=WS_PORT, log_level="info")
        server = uvicorn.Server(config)
        
        # Run uvicorn in the loop
        # Run uvicorn in the loop
        self.loop.create_task(server.serve())
        logger.info("WebSocket server started in background task.")

        # Attach WS Server helper to bot
        from ..services.websocket_server import WebSocketServer
        self.ws_server = WebSocketServer()

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN not found. Please set it in .env")
        sys.exit(1)
        
    bot = MyriaBot()
    bot.run(DISCORD_TOKEN)
