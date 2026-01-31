import asyncio
import os
import logging
from opencode_ai import AsyncOpencode

# Basic logging to see what happens
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    base_url = "http://localhost:4096"
    logger.info(f"Connecting to {base_url}...")
    
    client = AsyncOpencode(base_url=base_url)
    
    try:
        logger.info("Creating session...")
        session = await client.session.create(extra_body={})
        logger.info(f"Session created: {session.id}")
        
        logger.info("Sending 'hello'...")
        
        # Send message
        await client.session.with_raw_response.chat(
            id=session.id,
            model_id="gemini-3-flash",
            provider_id="google",
            parts=[{"type": "text", "text": "hello"}]
        )
        
        logger.info("Message sent. Listening for events...")
        
        # Try to listen to events stream? 
        # The docs mention client.event.list()
        
        # But wait, does 'chat' itself return a stream if we ask for it?
        # The SDK docs say: 
        # "To stream the response body, use .with_streaming_response instead"
        
        # Let's try calling chat WITH streaming response wrapper
        # Maybe that triggers the generation?
        
        logger.info("Sending 'hello' AGAIN with streaming...")
        
        async with client.session.with_streaming_response.chat(
            id=session.id,
            model_id="gemini-3-flash",
            provider_id="google",
            parts=[{"type": "text", "text": "hello again"}]
        ) as response:
            logger.info(f"Stream response status: {response.status_code}")
            async for line in response.iter_lines():
                print(f"Stream line: {line}")
            
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
