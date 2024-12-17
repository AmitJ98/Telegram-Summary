import summarizer
from pyrogram import Client
from dotenv import load_dotenv
import os
# import json


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
        unread_messages_test = []
        
        if unread_count != 0:
            for message in bot.get_chat_history(dialog_id, limit= unread_count):
                if not message.caption and not message.text: #skip empty messages
                    continue
                unread_messages.append(message)

                """this code is used to create json file for testing"""
            #     content = message.text if message.text else ''    
            #     # Checking if the message has media (photo, video, document) with a caption
            #     media_caption = message.caption if message.caption else None

            #     media = None
            #     if message.photo or message.video or message.document:
            #         media = True
            #     else:
            #         media = False

            #     sender_id = message.from_user.id if message.from_user else None
            #     sender_username = message.from_user.username if message.from_user else None

            #     unread_messages_test.append({
            #         'message_id': message.id,
            #         'content': content,  # Text content 
            #         'timestamp': message.date.isoformat(),  # Storing timestamp in ISO format
            #         'sender_id': sender_id,
            #         'sender_username': sender_username,
            #         'media_type': media,  # 'True', 'False'
            #         'media_caption': media_caption,  # The caption if media 
            #     })



            # with open('unread_messages.json', 'w', encoding='utf-8') as f:
            #     json.dump(unread_messages_test, f, ensure_ascii=False, indent=4)

            print(f"Total of valid unread messages in '{GROUP_NAME}': {len(unread_messages)}")
            if unread_messages:
                summarizer.summarize_group(unread_messages,GROUP_NAME)


        else:
            print(f"No unread messages in '{GROUP_NAME}'.")
    
    
    else:
        print(f"Could not find the group '{GROUP_NAME}'.")



""""if need to fetch media"""
# if message.media:
#     if message.photo:
#         print(f"Image found in Message ID {message.id}")
#         file_path = bot.download_media(message)
#         print(f"Image downloaded to: {file_path}")
#         break
