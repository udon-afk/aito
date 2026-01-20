import discord
from discord.ext import commands
import logging
import asyncio
import os
from ...config import CHAT_CHANNEL_ID
from ...services.ollama_client import OllamaClient
from ...services.sbv2_client import SBV2Client

logger = logging.getLogger(__name__)

class TextChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ollama = OllamaClient()
        self.sbv2 = SBV2Client()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("TextChat Cog loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id != CHAT_CHANNEL_ID:
            return

        # 1. Process Text
        user_text = message.content
        logger.info(f"Text Message from {message.author}: {user_text}")

        async with message.channel.typing():
            # 2. Ollama Generation (Async wrapper)
            loop = asyncio.get_event_loop()
            try:
                # TODO: Add context/RAG here
                ai_text = await loop.run_in_executor(
                    None, 
                    lambda: self.ollama.generate(user_text, user_id=message.author.id)
                )
            except Exception as e:
                logger.error(f"Generate error: {e}")
                ai_text = "エラーが発生しました。"

            # 3. Send Text Reply
            await message.reply(ai_text)
            
            # 4. Voice Reply (if user is in VC and bot is capable)
            if message.guild.voice_client and message.guild.voice_client.is_connected():
                
                # Notify Frontend
                if hasattr(self.bot, "ws_server"):
                    await self.bot.ws_server.broadcast({
                        "type": "speaking", 
                        "text": ai_text,
                        "source": "text_chat"
                    })

                # Generate Audio (Async wrapper)
                try:
                    wav_path = await loop.run_in_executor(
                        None,
                        lambda: self.sbv2.tts(ai_text)
                    )
                except Exception as e:
                    logger.error(f"TTS error: {e}")
                    wav_path = None
                
                if wav_path and os.path.exists(wav_path):
                     # Play Audio
                     def after_play(error):
                         if error:
                             logger.error(f"Player error: {error}")
                         try:
                             os.remove(wav_path)
                             logger.info(f"Removed temp file: {wav_path}")
                         except Exception as e:
                             logger.error(f"Failed to remove temp file: {e}")

                     source = discord.FFmpegPCMAudio(wav_path)
                     message.guild.voice_client.play(source, after=after_play)
                else:
                    logger.warning("Failed to generate TTS audio.")

async def setup(bot):
    await bot.add_cog(TextChat(bot))
