from abc import ABC, abstractmethod

class ChatAdapter(ABC):
    @abstractmethod
    async def start(self):
        """Start the adapter (e.g. connect to Discord)"""
        pass
    
    @abstractmethod
    async def stop(self):
        """Stop the adapter"""
        pass
