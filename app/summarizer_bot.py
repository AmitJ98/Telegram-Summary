import summarizer
from pyrogram import Client
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_ID = int(os.getenv("MY_TELEGRAM_API_ID"))
API_HASH = os.getenv("MY_TELEGRAM_API_HASH")
user_bot = Client("my_account", api_id=API_ID, api_hash=API_HASH)


GROUP_NAME = "Abu Ali Express in English"



def save_messages_to_json(messages, file_name):
    """Save messages to a JSON file for testing or debugging."""
    processed_messages = [
        {
            'message_id': msg.id,
            'content': msg.caption or msg.text,
            'timestamp': msg.date.isoformat(),
            'sender_id': msg.from_user.id if msg.from_user else None,
            'sender_username': msg.from_user.username if msg.from_user else None,
            'media': bool(msg.media),
            'media_caption': msg.caption if msg.media else None,
        }
        for msg in messages
    ]
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(processed_messages, f, ensure_ascii=False, indent=4)
    print(f"Messages saved to '{file_name}'.")


def fetch_unread_messages(bot:Client, group_name:str):
    """Fetch unread messages from a specific group."""

    target_dialog = None
    for dialog in bot.get_dialogs():
        if dialog.chat.title == group_name:
            target_dialog = dialog
            break

    if not target_dialog:
        print(f"Could not find the group '{group_name}'.")
        return None, None

    dialog_id = target_dialog.chat.id
    unread_count = target_dialog.unread_messages_count
    print(f"Fetching unread messages from '{group_name}' (Unread Count: {unread_count}) ---->")

    unread_messages = []
    if unread_count != 0:
        for message in bot.get_chat_history(dialog_id, limit=unread_count):
            if not message.caption and not message.text:
                continue
            unread_messages.append(message)

        # bot.read_chat_history(dialog_id) # need to add option for mark or no
        # print(f"Marked all messages as read in '{group_name}'.") 
    else:
        print(f"No unread messages in '{group_name}'.")

    return dialog_id, unread_messages    


def main():
    with user_bot:
        print("Successfully connected to Telegram!")
        print("Start session ---->>>")
        
        dialog_id, unread_messages = fetch_unread_messages(user_bot, GROUP_NAME)

        if unread_messages:
            print(f"Total of valid unread messages in '{GROUP_NAME}': {len(unread_messages)}")

            # Save messages for testing/debugging
            # save_messages_to_json(unread_messages, 'unread_messages.json')

            # Summarize the messages
            summary = summarizer.summarize_group(unread_messages)


if __name__ == "__main__":
    main()