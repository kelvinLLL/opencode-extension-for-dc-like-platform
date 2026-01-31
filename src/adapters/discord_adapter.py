import discord
import asyncio
import logging
from typing import List
from src.core.session_manager import SessionManager
from .base import ChatAdapter

logger = logging.getLogger(__name__)

class DiscordAdapter(ChatAdapter):
    def __init__(self, token: str, session_manager: SessionManager):
        self.token = token
        self.session_manager = session_manager
        
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        
        self.client = discord.Client(intents=intents)
        
        self.client.on_ready = self.on_ready
        self.client.on_message = self.on_message

    async def start(self):
        await self.client.start(self.token)

    async def stop(self):
        await self.client.close()

    async def on_ready(self):
        logger.info(f'Logged in as {self.client.user} (ID: {self.client.user.id})')

    async def on_message(self, message: discord.Message):
        if message.author == self.client.user:
            return

        if self.client.user in message.mentions:
            logger.info(f"Received mention from {message.author}: {message.content}")
            content = message.content.replace(f'<@{self.client.user.id}>', '').strip()
            content = content.replace(f'<@!{self.client.user.id}>', '').strip()
            
            if not content:
                content = "hello" 

            await self.handle_command(message, content)

    async def handle_command(self, message: discord.Message, content: str):
        user_id = message.author.id
        
        try:
            if content.startswith('help'):
                help_text = """
**OpenCode Bot Commands:**
- `@Bot new [model_id]` - Start a new session. 
  - Default model: `antigravity-gemini-3-pro`
  - Example: `@Bot new google/gemini-pro`
- `@Bot switch <session_id>` - Switch to an existing session.
- `@Bot list` - List all available sessions.
- `@Bot <message>` - Chat with the current session.
                """
                await message.reply(help_text)
                return

            if content.startswith('new'):
                parts = content.split()
                model_id = "antigravity-gemini-3-pro"
                if len(parts) > 1:
                    model_id = parts[1]
                
                logger.info(f"User {user_id} creating new session with model {model_id}")
                session_id = await self.session_manager.create_session(user_id, model_id)
                await message.reply(f"✅ Started new session: `{session_id}`\nModel: `{model_id}`")
                
            elif content.startswith('switch'):
                parts = content.split()
                if len(parts) < 2:
                    await message.reply("Usage: `@Bot switch <session_id>`")
                    return
                session_id = parts[1]
                logger.info(f"User {user_id} switching to session {session_id}")
                self.session_manager.active_sessions[user_id] = session_id
                await message.reply(f"🔄 Switched to session: `{session_id}`")
                
            elif content.startswith('list'):
                 async with message.channel.typing():
                     logger.info(f"User {user_id} listing sessions")
                     sessions = await self.session_manager.client.session.list()
                     
                     response_lines = ["**Available Sessions:**"]
                     for s in sessions:
                         marker = ""
                         if user_id in self.session_manager.active_sessions:
                             if self.session_manager.active_sessions[user_id] == s.id:
                                 marker = " (Active)"
                         response_lines.append(f"- `{s.id}`{marker}")
                     
                     if len(response_lines) == 1:
                         response_lines.append("No sessions found.")
                         
                     await self.send_chunked(message.channel, "\n".join(response_lines))

            else:
                async with message.channel.typing():
                    logger.info(f"Sending message to OpenCode for user {user_id}...")
                    response = await self.session_manager.send_message(user_id, content)
                    logger.info(f"Received response from OpenCode (Length: {len(response)})")
                    await self.send_chunked(message.channel, response)
                    
        except Exception as e:
            logger.error(f"Error handling command: {str(e)}", exc_info=True)
            await message.reply(f"⚠️ Error: {str(e)}\n(Check bot logs for details)")

    async def send_chunked(self, channel, text: str):
        chunk_size = 1900
        if not text:
             await channel.send("<Empty Response>")
             return

        for i in range(0, len(text), chunk_size):
            await channel.send(text[i:i+chunk_size])
