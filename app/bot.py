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

        
            print(f"Total unread messages in '{GROUP_NAME}': {len(unread_messages)}")
            if unread_messages:
                summarizer.summarize_group(unread_messages,GROUP_NAME)


        else:
            print(f"No unread messages in '{GROUP_NAME}'.")
    
    
    else:
        print(f"Could not find the group '{GROUP_NAME}'.")






    # prints all dialogs and their id 
    # print("All chats I have: ")
    # for dialog in bot.get_dialogs():
    #     print(f"Dialog Type: {dialog.chat.type}, Chat Name: {dialog.chat.title}, Chat ID: {dialog.chat.id}")


    # group_id = -4781637743  # test froup id
    # message = "Hello, this is a message from the bot!"

    # try:
    #     # Send a message to the group with the specified group ID
    #     bot.send_message(group_id, message)
    #     print(f"Message sent to group with ID {group_id}")
    
    # except Exception as e:
    #     print(f"Error sending message: {e}")