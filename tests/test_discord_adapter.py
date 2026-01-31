import pytest
from unittest.mock import AsyncMock, MagicMock
from src.adapters.discord_adapter import DiscordAdapter
from src.core.session_manager import SessionManager

@pytest.fixture
def mock_session_manager():
    return AsyncMock(spec=SessionManager)

@pytest.fixture
def adapter(mock_session_manager):
    return DiscordAdapter("fake_token", mock_session_manager)

@pytest.mark.asyncio
async def test_on_message_ignores_self(adapter):
    # Mock client user
    adapter.client = MagicMock()
    adapter.client.user = MagicMock()
    adapter.client.user.id = 999
    
    msg = AsyncMock()
    msg.author = adapter.client.user # Same user
    
    await adapter.on_message(msg)
    
    # handle_command should not be called
    # We can check if reply was called (it shouldn't)
    msg.reply.assert_not_called()

@pytest.mark.asyncio
async def test_handle_command_new(adapter, mock_session_manager):
    msg = AsyncMock()
    msg.author.id = 123
    mock_session_manager.create_session.return_value = "ses_new"
    
    await adapter.handle_command(msg, "new")
    
    mock_session_manager.create_session.assert_called_with(123, "gemini-2.0-flash-exp")
    msg.reply.assert_called()

@pytest.mark.asyncio
async def test_send_chunked(adapter):
    channel = AsyncMock()
    long_text = "a" * 2000
    
    await adapter.send_chunked(channel, long_text)
    
    # Should be sent in 2 chunks (1900 + 100)
    assert channel.send.call_count == 2
    channel.send.assert_any_call("a" * 1900)
    channel.send.assert_any_call("a" * 100)

@pytest.mark.asyncio
async def test_handle_command_list(adapter, mock_session_manager):
    msg = AsyncMock()
    msg.author.id = 123
    
    cm = AsyncMock()
    msg.channel.typing = MagicMock(return_value=cm)
    
    mock_session_manager.client = MagicMock()
    
    session1 = MagicMock()
    session1.id = "ses_1"
    session2 = MagicMock()
    session2.id = "ses_2"
    
    mock_session_manager.client.session.list = AsyncMock(return_value=[session1, session2])
    
    mock_session_manager.active_sessions = {123: "ses_1"}
    
    await adapter.handle_command(msg, "list")
    
    mock_session_manager.client.session.list.assert_called_once()
