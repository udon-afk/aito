import discord
from discord.ext import commands
import logging
from ...config import SCORE_CHANNEL_ID

logger = logging.getLogger(__name__)

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("System Cog loaded.")
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Handle scoring via reactions in SCORE_CHANNEL_ID
        """
        if payload.channel_id != SCORE_CHANNEL_ID:
            return
            
        if payload.user_id == self.bot.user.id:
            return

        # Fetch the message
        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return
            
        try:
            message = await channel.fetch_message(payload.message_id)
        except discord.NotFound:
            return

        # Only process Embeds (which are sent by the bot for scoring)
        # or Bot messages if we change the design.
        # Assuming we are reacting to the Bot's log in SCORE_CHANNEL.
        
        # Emoji to Score Mapping
        emoji_str = str(payload.emoji)
        score = 0
        
        # Simple mapping
        if "👍" in emoji_str: score = 5
        elif "👎" in emoji_str: score = 1
        elif "😄" in emoji_str: score = 4
        elif "😐" in emoji_str: score = 3
        elif "😕" in emoji_str: score = 2
        # Add Number emojis if needed: '1️⃣', '2️⃣'...
        elif "1️⃣" in emoji_str: score = 1
        elif "2️⃣" in emoji_str: score = 2
        elif "3️⃣" in emoji_str: score = 3
        elif "4️⃣" in emoji_str: score = 4
        elif "5️⃣" in emoji_str: score = 5
        
        if score == 0:
            return

        # Extract Input/Output from Embed or Message
        # Assuming the Score Channel Log format:
        # Embed Title: Input / Output
        # Embed Description: ...
        # Or fields.
        
        input_text = ""
        output_text = ""
        
        if message.embeds:
            embed = message.embeds[0]
            # Heuristic extraction based on typical logging format
            # Let's assume Field 0 is Input, Field 1 is Output
            for field in embed.fields:
                if field.name in ["Input", "入力", "User"]:
                    input_text = field.value
                elif field.name in ["Output", "出力", "Bot", "AI"]:
                    output_text = field.value
        else:
            # Fallback if just text
            content = message.content
            # Try to split? Too ambiguous.
            pass

        if input_text and output_text:
            logger.info(f"LEARNING DATA CAPTURED | Score: {score} | In: {input_text[:20]}... | Out: {output_text[:20]}...")
            # TODO: Call RAG engine to save
            # self.bot.rag_engine.add_memory(input_text, output_text, score) 
            # (Assuming rag_engine is attached to bot or imported)
        else:
            logger.debug("Could not extract input/output from scored message.")

async def setup(bot):
    await bot.add_cog(System(bot))
