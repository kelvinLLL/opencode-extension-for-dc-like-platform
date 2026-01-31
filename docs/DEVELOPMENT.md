# OpenCode Discord Bot Development Guide

## Overview

This project implements a Discord Bot that acts as a remote interface for a local OpenCode CLI instance. It allows you to interact with your AI coding assistant directly from Discord, maintaining session context and supporting standard OpenCode operations.

## Architecture

The project follows a modular **Adapter Pattern** to decouple the core OpenCode logic from specific chat platforms.

```
src/
├── core/
│   └── session_manager.py    # Wraps the OpenCode Python SDK, manages user sessions
├── adapters/
│   ├── base.py               # Abstract Base Class for chat adapters
│   └── discord_adapter.py    # Discord implementation (using discord.py)
└── main.py                   # Entry point, wires Core and Adapter together
```

- **Core**: Handles communication with `localhost:54321` via `opencode-sdk-python`.
- **Adapters**: Handle platform-specific events (messages, commands) and format responses (chunking).

## Prerequisites

- **Python 3.9+**
- **OpenCode CLI**: Must be installed and running locally (`opencode serve` or just running the app).
- **Discord Bot Token**: You need a bot created in the [Discord Developer Portal](https://discord.com/developers/applications).

## Installation

1.  **Clone the repository** (if you haven't already).

2.  **Set up a virtual environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This project depends on a local copy of `opencode-sdk-python` located in the root directory.*

## Configuration

1.  Copy the example configuration:
    ```bash
    cp .env.example .env
    ```

2.  Edit `.env` and fill in your details:
    ```ini
    DISCORD_TOKEN=your_discord_bot_token_here
    OPENCODE_BASE_URL=http://localhost:54321
    ```

## Usage

### Starting the Bot

Ensure your OpenCode instance is running, then start the bot:

```bash
python src/main.py
```

### Commands

The bot listens for mentions (`@BotName`).

-   **Start a new session**:
    ```text
    @Bot new [model_id]
    # Example: @Bot new gemini-2.0-flash-exp
    ```

-   **Chat**:
    ```text
    @Bot How do I write a binary search in Python?
    ```

-   **List active sessions**:
    ```text
    @Bot list
    ```

-   **Switch to an existing session**:
    ```text
    @Bot switch <session_id>
    ```

## Development

### Running Tests

We use `pytest` for unit testing. The tests mock the Discord API and OpenCode SDK to ensure logic correctness without needing a live server.

```bash
# Run all tests
pytest tests/
```

### Adding a New Adapter

To add support for a new platform (e.g., Slack, Telegram):

1.  Create a new file in `src/adapters/`, e.g., `slack_adapter.py`.
2.  Inherit from `ChatAdapter` (defined in `src/adapters/base.py`).
3.  Implement `start()` and `stop()`.
4.  Inject `SessionManager` into your adapter to handle OpenCode interactions.
5.  Update `src/main.py` to initialize your new adapter based on configuration.

## Troubleshooting

-   **Bot fails to connect to OpenCode**: Ensure `OPENCODE_BASE_URL` is correct and the server is running. Default is `http://localhost:54321`.
-   **Discord API Errors**: Check your `DISCORD_TOKEN` and ensure the bot has `Message Content Intent` enabled in the Discord Developer Portal.
