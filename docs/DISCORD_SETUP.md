# Discord Bot Configuration Guide

This guide will walk you through creating a Discord Application, creating a Bot User, and obtaining the necessary Token to run your OpenCode Discord Bot.

## Step 1: Create a Discord Application

1.  Go to the **[Discord Developer Portal](https://discord.com/developers/applications)**.
2.  Log in with your Discord account.
3.  Click the **"New Application"** button (top right).
4.  **Name** your application (e.g., "OpenCode Assistant").
5.  Click **Create**.

## Step 2: Create the Bot User

1.  In the left sidebar menu, click **Bot**.
2.  Click the **"Reset Token"** button (or "Add Bot" if it's a brand new app).
3.  **Confirm** the action.
4.  **COPY THIS TOKEN IMMEDIATELY**.
    *   This is your `DISCORD_TOKEN`.
    *   **Security Warning**: Never share this token. If leaked, anyone can control your bot.
    *   Paste this token into your `.env` file:
        ```ini
        DISCORD_TOKEN=your_copied_token_here
        ```

## Step 3: Configure Bot Privileges (Crucial!)

To allow the bot to read messages and command mentions, you must enable **Privileged Gateway Intents**.

1.  Still on the **Bot** page, scroll down to the **"Privileged Gateway Intents"** section.
2.  Toggle **ON** the following:
    *   ✅ **Message Content Intent** (Required to read commands like `@Bot new`)
    *   *(Optional)* **Server Members Intent** (Not strictly needed for this bot, but good for future features)
    *   *(Optional)* **Presence Intent**
3.  Click **Save Changes** (bottom of the page).

## Step 4: Invite the Bot to Your Server

1.  In the left sidebar menu, click **OAuth2**.
2.  Under OAuth2, click **URL Generator**.
3.  **Scopes**: Check the following box:
    *   ✅ `bot`
4.  **Bot Permissions**: Check the following boxes (at minimum):
    *   ✅ `Read Messages/View Channels`
    *   ✅ `Send Messages`
    *   ✅ `Read Message History`
5.  Scroll down to the **Generated URL**.
6.  **Copy** the URL and paste it into your browser.
7.  Select your Discord server and click **Authorize**.

## Step 5: Verify

1.  Go to your Discord server.
2.  You should see your bot in the member list (it will be offline until you run the python script).
3.  Once you run `python src/main.py`, the bot status should turn **Online**.
