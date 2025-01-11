import summarizer
from pyrogram import Client
from database_management.users_data_table import fetch_user_data
import json
import re
import os
from summarizer import summarize_chat


####################   TESTING  ###############################################
################################################################################

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
        session_folder = "sessions"
        os.makedirs(session_folder, exist_ok=True) 
        str_user_id = str(user_id)
        user_bot = Client(name = str_user_id, api_id=user["api_id"], api_hash=user["api_hash"], workdir=session_folder)

        if user_bot:
            print(f"[USER BOT SUCCESS] User bot created successfully for user ID {user_id}.")
            return user_bot
        
        else:
            print(f"[USER BOT ERROR] Failed to create user bot for user ID {user_id}.")
            return None
    else:
        return None


def check_valid_chat_name(group_name:str) -> bool:
    """Check if the group name is valid for summarization.
        Matches only English letters (uppercase and lowercase), digits, and common symbols."""

    pattern = r'^[a-zA-Z0-9!@#$%^&*()_\-+=\[\]|\\:"\'<>,.?/~` ]*$'
    return bool(re.match(pattern, group_name))


async def scan_chats(user_id: int) -> list[tuple[str, int]]:
    """Scan all chats/groups of the user and return only those with valid names."""

    user_bot = create_user_bot(user_id)
    if not user_bot:
        return []

    valid_chats = []
    try:
        await user_bot.start()  
        async for dialog in user_bot.get_dialogs():
            if dialog.chat.title and check_valid_chat_name(dialog.chat.title):
                valid_chats.append((dialog.chat.title, dialog.chat.id))
        
        return valid_chats

    except Exception as e:
        print(f"[USER BOT ERROR] Failed to scan chats for user ID {user_id}. Reason: {e}")
        return []

    finally:
        await user_bot.stop() 


async def fetch_unread_messages_from_spesific_chat(user_bot: Client, chat_id: int, unread_count: int) -> list: #list of messages
    """Fetch unread messages from a specific chat."""

    unread_messages = []
    try:
        async for message in user_bot.get_chat_history(chat_id, limit=unread_count):
            if not message.caption and not message.text:
                continue
            unread_messages.append(message) 
        await user_bot.read_chat_history(chat_id)

    except Exception as e:
        print(f"[USER BOT ERROR] Failed to fetch messages from chat ID {chat_id}. Reason: {e}")

    return unread_messages


async def fetch_messages_from_all_chats(user_bot: Client, chats_list: list[tuple[str, int]]) -> list[tuple[str,list,bool]]:
    """Fetch messages from all chats and groups that the user selected."""
    
    unread_list = []

    for chat_name, chat_id in chats_list:
        try:
            chat = await user_bot.get_chat(chat_id)  
            unread_count = chat.unread_messages

            if unread_count == 0:
                unread_list.append((chat_name, [f"{chat_name}\nNo unread messages found in the chat."], False))
                continue
            else:
                unread_messages = await fetch_unread_messages_from_spesific_chat(user_bot, chat_id, unread_count)
                unread_list.append((chat_name, unread_messages,True))

        except Exception as e:
            print(f"[USER BOT ERROR] Failed to fetch messages from chat: {chat_name} (ID: {chat_id}). Reason: {e}")
            unread_list.append((chat_name, [f"{chat_name}\nError fetching messages."], False))

    return unread_list


async def summarize_all_chats(user_id: int) -> list[str]:
    """
    Fetch unread messages from selected chats and summarize them.

    Args:
        user_id (int): The user ID for which chats need to be summarized.
    Returns:
        list[str]: A list of summaries for the selected chats.
    """

    user_bot = create_user_bot(user_id)

    try:
        await user_bot.start()
        chats_list = []   # Replace this placeholder with a database call or user input fetching chats_list
        
        summaries = [] 
        unread_list = await fetch_messages_from_all_chats(user_bot, chats_list)

        for chat_name, unread_messages, summary_bool in unread_list:
            if summary_bool:
                try:
                    summary = summarize_chat(chat_name, unread_messages) 
                    if summary:
                        summaries.append(summary)
                except Exception as e:
                    print(f"USER BOT ERROR] Failed to summarize chat: {chat_name}. Reason: {e}")
            
            else:
                summaries.append(f"{chat_name}\nNo messages to summarize.")

        return summaries

    except Exception as e:
        print(f"[USER BOT ERROR] Failed to process chats for user ID {user_id}. Reason: {e}")
        return []
    
    finally:
        await user_bot.stop()  
