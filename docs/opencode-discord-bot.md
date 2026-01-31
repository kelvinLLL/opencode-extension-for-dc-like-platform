# Plan: Discord Bot for OpenCode CLI

## TL;DR

> **Quick Summary**: Create a local Discord Bot using `discord.py` and `opencode-sdk-python` that acts as a remote interface for the OpenCode CLI.
> 
> **Deliverables**:
> - `src/core/session_manager.py`: Manages OpenCode sessions.
> - `src/adapters/discord_adapter.py`: Discord bot implementation with command parsing.
> - `src/main.py`: Entry point.
> - `tests/`: Unit tests with mocks.
> 
> **Estimated Effort**: Medium
> **Parallel Execution**: YES - 2 waves
> **Critical Path**: Core Logic → Adapter Implementation → Integration

---

## Context

### Original Request
Build a Discord bot to interact with OpenCode CLI, using the official Python SDK. Must use an Adapter pattern for future platform support.

### Interview Summary
**Key Decisions**:
- **Deployment**: Local machine (Personal Assistant mode).
- **Session Strategy**: Stateful "CLI Mode" (User commands control active session).
- **Commands**: `@Bot switch <id>`, `@Bot new`, `@Bot chat <msg>`.
- **Testing**: Unit tests with mocks.
- **Style**: Standard Python (Black/Isort).

**Research Findings**:
- SDK (`AsyncOpencode`) supports async/await.
- Discord message limit (2000 chars) requires chunking.
- State persistence is in-memory for V1 (reset on restart).

---

## Work Objectives

### Core Objective
Enable users to interact with their local OpenCode CLI via Discord messages, maintaining conversation context and session state.

### Concrete Deliverables
- [ ] Working Discord Bot connected to local OpenCode instance
- [ ] Command system: `new`, `switch`, `list`, `model`
- [ ] Automatic message chunking for long responses
- [ ] Unit test suite for core logic

### Definition of Done
- [ ] Bot responds to `@Bot hello`
- [ ] Bot can create a new OpenCode session
- [ ] Bot splits >2000 char responses into multiple messages

### Must Have
- Adapter Pattern architecture
- AsyncIO throughout
- `.env` configuration for tokens

### Must NOT Have (Guardrails)
- Database persistence (In-memory only for V1)
- Multi-server support (Local usage only)
- TUI rendering (Text only)

---

## Verification Strategy

### Test Decision
- **Infrastructure exists**: NO (New project)
- **User wants tests**: YES (Unit Tests with Mocks)
- **Framework**: `pytest`

### Automated Verification Only
Each TODO includes `pytest` commands.

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1:
├── Task 1: Project Setup & Core Config
└── Task 2: Core SessionManager Logic

Wave 2:
├── Task 3: Base Adapter & Discord Implementation
└── Task 4: Unit Tests
```

---

## TODOs

- [x] 1. Project Setup & Configuration
  **What to do**:
  - Initialize poetry project.
  - Add dependencies: `discord.py`, `python-dotenv`, `pytest`, `pytest-asyncio`.
  - Add local SDK dependency: `poetry add ./opencode-sdk-python` (Ensure this path is correct relative to project root).
  - Create `.env.example` (Keys: `DISCORD_TOKEN`, `OPENCODE_BASE_URL`).
  - Create project structure: `src/core`, `src/adapters`.
  
  **References**:
  - `opencode-sdk-python/README.md` - SDK installation guide
  
  **Acceptance Criteria**:
  - [x] `poetry install` succeeds (Used pip/venv fallback)
  - [x] `src/` folder structure created
  - [x] `pytest` runs (0 tests -> 7 tests passed)

- [x] 2. Core SessionManager Implementation
  **What to do**:
  - Implement `src/core/session_manager.py`.
  - Class `SessionManager` wrapping `AsyncOpencode`.
  - Methods: `create_session`, `get_session`, `send_message`, `list_sessions`.
  - Manage in-memory state: `active_sessions: Dict[int, str]` (User ID -> Session ID).
  - Ensure `AsyncOpencode` is initialized inside an async context (or `__init__` if lazy).
  
  **References**:
  - `opencode-sdk-python/src/opencode_ai/resources/session.py` - For API method signatures (Reference ONLY, do not edit)
  
  **Acceptance Criteria**:
  - [x] Class `SessionManager` exists
  - [x] Can instantiate with `AsyncOpencode`
  - [x] State dictionary tracks active sessions

- [x] 3. Adapter Interface & Discord Implementation
  **What to do**:
  - Create `src/adapters/base.py`: Abstract Base Class `ChatAdapter`.
  - Implement `src/adapters/discord_adapter.py`:
    - Inherits `ChatAdapter`.
    - `on_message` handler.
    - Command parser: `switch`, `new`, `list`, `model`.
    - Message splitter (chunking at 1900 chars).
  
  **References**:
  - Discord.py docs: `https://discordpy.readthedocs.io/`
  
  **Acceptance Criteria**:
  - [x] `DiscordAdapter` class exists
  - [x] Regex for commands matches `@Bot command`
  - [x] Message splitter test: Input 2500 chars -> Returns 2 chunks (1900, 600)

- [x] 4. Main Entry Point & Integration
  **What to do**:
  - Create `src/main.py`.
  - Load `.env`.
  - Initialize `AsyncOpencode` and `DiscordAdapter`.
  - Start the bot.
  
  **Acceptance Criteria**:
  - [x] `python src/main.py` starts the bot (if token provided)

- [x] 5. Unit Tests
  **What to do**:
  - Create `tests/test_session_manager.py`.
  - Create `tests/test_discord_adapter.py`.
  - Mock `AsyncOpencode` responses.
  - Mock `discord.Message`.
  
  **Acceptance Criteria**:
  - [x] `pytest` passes with >80% coverage on logic
```
