import asyncio
import logging
from typing import Dict, List, Optional
from opencode_ai import AsyncOpencode
from opencode_ai.types import AssistantMessage

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, client: AsyncOpencode):
        self.client = client
        # Mapping from User ID (Discord ID) to Session ID
        self.active_sessions: Dict[int, str] = {}

    async def get_or_create_session(self, user_id: int, model_id: str = "gemini-2.0-flash-exp") -> str:
        """
        Get the active session for a user, or create a new one if none exists.
        """
        if user_id in self.active_sessions:
            return self.active_sessions[user_id]
        
        return await self.create_session(user_id, model_id)

    async def create_session(self, user_id: int, model_id: str = "gemini-2.0-flash-exp") -> str:
        """
        Force create a new session for the user, overwriting the previous one.
        """
        # Create session via SDK
        # Try passing an empty dict to ensure valid JSON body is sent
        session = await self.client.session.create(extra_body={})
        self.active_sessions[user_id] = session.id
        return session.id

    async def send_message(self, user_id: int, content: str, model_id: str = "gemini-2.0-flash-exp") -> str:
        """
        Send a message to the user's active session.
        Returns the text response.
        """
        session_id = await self.get_or_create_session(user_id, model_id)
        
        provider_id = "google"
        
        if "/" in model_id:
            parts = model_id.split("/", 1)
            provider_id = parts[0]
            model_id = parts[1] 
        
        # Force double check: If it's a known model from config, ensure provider is google
        if "gemini" in model_id or "claude" in model_id:
            provider_id = "google"

        try:
            # We pass params both normally AND in extra_body to ensure they are received
            # regardless of SDK/Server field naming mismatches (providerID vs provider_id)
            await self.client.session.with_raw_response.chat(
                id=session_id,
                model_id=model_id,
                provider_id=provider_id,
                extra_body={
                    "providerID": provider_id, # Server likely expects camelCase
                    "modelID": model_id,
                    "provider_id": provider_id, # Backup
                    "model_id": model_id
                },
                parts=[{"type": "text", "text": content}] 
            )
            
            for attempt in range(20):

                history = await self.client.session.messages(session_id)
                
                if not history:
                    logger.info(f"Polling attempt {attempt+1}: History is empty")
                    await asyncio.sleep(0.5)
                    continue

                debug_info = []
                for msg in history[-3:]: 
                    debug_info.append(f"[ID={msg.info.id}, Role={msg.info.role}, Parts={len(msg.parts) if msg.parts else 0}]")
                logger.info(f"Polling attempt {attempt+1}: {', '.join(debug_info)}")

                found_msg = None
                for msg in reversed(history):
                    if msg.info.role == 'assistant':
                        has_text = False
                        if msg.parts:
                            for part in msg.parts:
                                if part.type == 'text' and part.text:
                                    has_text = True
                                    break
                        if has_text:
                            found_msg = msg
                            break
                
                if found_msg:
                    text_response = ""
                    for part in found_msg.parts:
                        if part.type == 'text':
                            text_response += part.text
                    
                    return text_response
                
                await asyncio.sleep(0.5)
            
            return "<No text response (Timeout waiting for assistant)>"

        except Exception as e:
            if "404" in str(e):
                if user_id in self.active_sessions:
                    del self.active_sessions[user_id]
                raise Exception("Session expired or not found. Please try again.") from e
            raise e

    async def list_active_sessions(self) -> Dict[int, str]:
        return self.active_sessions

