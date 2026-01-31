import asyncio
import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from opencode_ai import AsyncOpencode
from src.core.session_manager import SessionManager
from src.adapters.discord_adapter import DiscordAdapter

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def main():
    token = os.getenv("DISCORD_TOKEN")
    base_url = os.getenv("OPENCODE_BASE_URL", "http://localhost:54321")
    
    if not token or token == "your_token_here":
        logger.error("DISCORD_TOKEN not found or invalid in .env")
        return

    logger.info(f"Initializing OpenCode Client (Base URL: {base_url})...")
    client = AsyncOpencode(base_url=base_url)
    
    session_manager = SessionManager(client)
    
    try:
        logger.info("Checking connection to OpenCode Server...")
        await client.session.list()
        logger.info("✅ Connected to OpenCode Server successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to connect to OpenCode Server at {base_url}")
        logger.error(f"Details: {str(e)}")
        logger.error("Please make sure 'opencode serve' is running locally.")
        return

    adapter = DiscordAdapter(token, session_manager)
    
    logger.info("Starting Discord Bot...")
    try:
        await adapter.start()
    except KeyboardInterrupt:
        logger.info("Stopping bot...")
    finally:
        await adapter.stop()
        await client.close()
        logger.info("Bot stopped.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
