import summarizer
from pyrogram import Client
from database_management.users_data_table import fetch_user_data
import json
import re


####################   TESTING  ###############################################
################################################################################
GROUP_NAME = "Abu Ali Express in English"

def save_messages_to_json_for_testing(messages, file_name):
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

################################################################################

def create_user_bot(user_id:int) -> Client:
    """Create a user bot and return it."""

    user = fetch_user_data(user_id)
    if user:
        user_bot = Client(name = "test", api_id=user["api_id"], api_hash=user["api_hash"])

        if user_bot:
            print(f"[USER BOT SUCCESS] User bot created successfully for user ID {user_id}.")
            return user_bot
        
        else:
            print(f"[USER BOT ERROR] Failed to create user bot for user ID {user_id}.")
            return None
    else:
        return None


def check_valid_chat_name_for_summarization(group_name:str) -> bool:
    """Check if the group name is valid for summarization.
        Matches only English letters (uppercase and lowercase), digits, and common symbols."""

    pattern = r'^[a-zA-Z0-9!@#$%^&*()_\-+=\[\]|\\:"\'<>,.?/~` ]*$'
    return bool(re.match(pattern, group_name))


async def scan_chats_for_summarization(user_id: int) -> list[str]:
    """Scan all chats/groups of the user and return only those with valid names."""

    user_bot = create_user_bot(user_id)
    if not user_bot:
        return []

    valid_chats = []
    try:
        await user_bot.start()  
        async for dialog in user_bot.get_dialogs():
            if dialog.chat.title and check_valid_chat_name_for_summarization(dialog.chat.title):
                valid_chats.append(dialog.chat.title)
        
        print(valid_chats)
        return valid_chats

    except Exception as e:
        print(f"[USER BOT ERROR] Failed to scan chats for user ID {user_id}. Reason: {e}")
        return []

    finally:
        await user_bot.stop() 


def fetch_unread_messages_from_chat(bot:Client, group_name:str):
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


