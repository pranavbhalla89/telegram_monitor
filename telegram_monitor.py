# Telegram chat monitor
# 
# Requirements
#   Telegram app (API_ID and API_HASH) - https://my.telegram.org/apps
#   pip install telethon
#
# (Mac only) To keep running in background
# caffeinate -s python3 telegram_monitor.py

import logging
import time
from telethon import TelegramClient, events

# --- CONFIGURATION ---
API_ID = 1234  # Replace with your actual integer API ID
API_HASH = '<API_HASH>'  # Replace with your actual API hash string

NOTIFICATION_TARGET = 'me'  # 'me' sends it to your "Saved Messages"
COOLDOWN_SECONDS = 300      # 5 minutes * 60 seconds

# Leave empty [] to monitor ALL channels/groups you are in,
# or specify IDs/usernames like ['@channel1', -100123456789]
MONITORED_CHANNELS = []
# ---------------------

# Uncomment to see detailed logs
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Dictionary to store the last notification timestamp for each chat: { chat_id: timestamp }
last_notification_times = {}

async def main():
    # FIXED: Initialize the client INSIDE main() so it grabs the correct asyncio loop
    client = TelegramClient('session_monitor', API_ID, API_HASH)
    
    event_filter = events.NewMessage(chats=MONITORED_CHANNELS) if MONITORED_CHANNELS else events.NewMessage

    @client.on(event_filter)
    async def handle_new_message(event):
        if (event.is_channel or event.is_group) and event.message.photo:
            chat_id = event.chat_id
            current_time = time.time()
            
            if chat_id in last_notification_times:
                time_passed = current_time - last_notification_times[chat_id]
                if time_passed < COOLDOWN_SECONDS:
                    remaining_time = int(COOLDOWN_SECONDS - time_passed)
                    logging.info(f"Photo detected in chat {chat_id}, but skipped due to cooldown ({remaining_time}s remaining).")
                    return
            
            last_notification_times[chat_id] = current_time
            
            chat = await event.get_chat()
            chat_name = getattr(chat, 'title', 'Unknown Group/Channel')
            chat_username = getattr(chat, 'username', None)
            source = f"@{chat_username}" if chat_username else chat_name
            
            logging.info(f"Photo detected in {source}! Sending text-only alert.")
            
            alert_text = f"📸 **A photo was posted in:** {source}"
            await client.send_message(NOTIFICATION_TARGET, alert_text)

    print("⚡ Starting Telegram Channel Monitor (with 5-min cooldown)...")
    await client.start()
    print("✅ Monitor is running smoothly.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())