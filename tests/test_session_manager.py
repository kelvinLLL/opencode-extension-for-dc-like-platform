import pytest
from unittest.mock import AsyncMock, MagicMock
from src.core.session_manager import SessionManager
from opencode_ai import AsyncOpencode
from opencode_ai.types import AssistantMessage, Session

@pytest.fixture
def mock_client():
    client = AsyncMock(spec=AsyncOpencode)
    client.session = AsyncMock()
    return client

@pytest.fixture
def manager(mock_client):
    return SessionManager(mock_client)

@pytest.mark.asyncio
async def test_get_or_create_session_creates_new(manager, mock_client):
    mock_session = MagicMock(spec=Session)
    mock_session.id = "ses_123"
    mock_client.session.create.return_value = mock_session
    
    session_id = await manager.get_or_create_session(user_id=1)
    
    assert session_id == "ses_123"
    assert manager.active_sessions[1] == "ses_123"
    mock_client.session.create.assert_called_once()

@pytest.mark.asyncio
async def test_get_or_create_session_uses_existing(manager):
    manager.active_sessions[1] = "ses_existing"
    
    session_id = await manager.get_or_create_session(user_id=1)
    
    assert session_id == "ses_existing"
    manager.client.session.create.assert_not_called()

@pytest.mark.asyncio
async def test_send_message_flow(manager, mock_client):
    manager.active_sessions[1] = "ses_123"
    
    # Mock chat response
    mock_assistant_msg = MagicMock(spec=AssistantMessage)
    mock_assistant_msg.id = "msg_abc"
    mock_client.session.chat.return_value = mock_assistant_msg
    
    # Mock history response
    mock_history_item = MagicMock()
    mock_history_item.info.id = "msg_abc"
    mock_history_item.parts = [MagicMock(type="text", text="Hello world")]
    
    mock_client.session.messages.return_value = [mock_history_item]
    
    response = await manager.send_message(1, "Hi")
    
    assert response == "Hello world"
    mock_client.session.chat.assert_called_with(
        id="ses_123",
        model_id="gemini-2.0-flash-exp",
        provider_id="google",
        parts=[{"type": "text", "text": "Hi"}]
    )
    mock_client.session.messages.assert_called_with("ses_123")
