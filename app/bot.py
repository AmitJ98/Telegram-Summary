import summarizer
from pyrogram import Client
from dotenv import load_dotenv
import os


load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

bot = Client("my_account", api_id=API_ID, api_hash=API_HASH)

GROUP_NAME = "Abu Ali Express in English"


with bot:
    print("Successfully connected to Telegram!")
    print("Start session ---->>>")
    
    target_dialog = None
    
    for dialog in bot.get_dialogs():
        if dialog.chat.title == GROUP_NAME:
            target_dialog = dialog
            break

    if target_dialog:
        dialog_id = target_dialog.chat.id
        unread_count = target_dialog.unread_messages_count  # Fetch the count of unread messages

        print(f"Fetching unread messages from '{GROUP_NAME}' (Unread Count: {unread_count}) ---->")

        unread_messages = []
        if unread_count != 0:
            for message in bot.get_chat_history(dialog_id, limit= unread_count):
                unread_messages.append(message)
                # if message.media:
                #     if message.photo:
                #         print(f"Image found in Message ID {message.id}")
                #         file_path = bot.download_media(message)
                #         print(f"Image downloaded to: {file_path}")
                #         break


        
            print(f"Total unread messages in '{GROUP_NAME}': {len(unread_messages)}")
            if unread_messages:
                summarizer.summarize_group(unread_messages,GROUP_NAME)


        else:
            print(f"No unread messages in '{GROUP_NAME}'.")
    
    
    else:
        print(f"Could not find the group '{GROUP_NAME}'.")




