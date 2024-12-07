from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

bot = Client("my_account", api_id=API_ID, api_hash=API_HASH)

# Dialog Type: ChatType.CHANNEL, Chat Name: Abu Ali Express in English, Chat ID: -1001560386984

# Start the bot session
with bot:
    print("Successfully connected to Telegram!")
    print("Start session ---->>>")
    

    # prints all dialogs and their id 
    print("All chats I have: ")
    for dialog in bot.get_dialogs():
        print(f"Dialog Type: {dialog.chat.type}, Chat Name: {dialog.chat.title}, Chat ID: {dialog.chat.id}")

        if dialog.chat.type in ["group", "supergroup", "Private"]:
            print(f"Group Name: {dialog.chat.title} | Group ID: {dialog.chat.id}")

    # group_id = -4781637743  # test froup id
    # message = "Hello, this is a message from the bot!"

    # try:
    #     # Send a message to the group with the specified group ID
    #     bot.send_message(group_id, message)
    #     print(f"Message sent to group with ID {group_id}")
    
    # except Exception as e:
    #     print(f"Error sending message: {e}")