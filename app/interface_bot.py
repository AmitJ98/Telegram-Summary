from pyrogram import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from database_management.users_data_table import insert_new_user, fetch_user_data, delete_user, update_chat_list, update_time
from database_management.users_data_table import check_user_existence
from summarizer_bot import scan_chats_for_summarization


load_dotenv()
INTERFACE_BOT_API_KEY = os.getenv("INTERFACE_BOT_API_KEY")

# Create the Application object
interface_bot = Application.builder().token(INTERFACE_BOT_API_KEY).build()


async def is_user_registered(user_id: int):
    exsit = check_user_existence(user_id)
    return exsit


def allready_registered(func):
    """Decorator Check if the user is registered, if not send a message to register."""
    
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        if await is_user_registered(user_id):
            await update.message.reply_text("You are already registered.")
            return
        else:
            return await func(update, context)
        
    return wrapper


def rquiered_registration(func):
    """Decorator Check if the user is registered, if not send a message to register."""
    
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        if await is_user_registered(user_id):
            return await func(update, context)
        else:
            await update.message.reply_text(
                "You are not registered for this service. Please register using the /register command.")
            return
        
    return wrapper


async def verify_api_key_and_hash(api_key: str, api_hash: str, user_id: int):
    """Verify the API key and hash for the user.
        check if the API key and hash are valid for the user."""
    
    try:
        user_bot = Client("user_bot", api_id=api_key, api_hash=api_hash)
        await user_bot.start()
        user_info = await user_bot.get_me()
        await user_bot.stop()

        if user_info.id == user_id:
            return user_info
        else:
            return None
        
    except Exception:
        return None


async def handle_api_key_and_hash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the API key and hash sent by the user,
        Verify the API key and hash and register the user.
        insert the user info into the database."""
    
    message_text = update.message.text
    splited_message = message_text.split(", ")
    print(update.message.from_user.id,print(type(update.message.from_user.id)))
    if len(splited_message) != 2:
        await update.message.reply_text("Invalid input. Please follow the format and try again.")
        return

    api_id, api_hash = splited_message
    user_info = await verify_api_key_and_hash(api_id, api_hash, update.message.from_user.id)
    print(user_info.id,type(user_info.id))
    if user_info:
        is_inserted = insert_new_user(user_info.id, api_id, api_hash, [])
        if is_inserted:
            await update.message.reply_text(f"Successfully registered! Your user ID: {user_info.id}")
            # 
            # need to delete the message of user where he sends me his keys
            #
        else:
            await update.message.reply_text("Failed to register you. Please try again later.")
        return

    else:
        await update.message.reply_text("Failed to verify your API Key and Hash. Please check them again.")
        return


# /start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """start command handler, send a welcome message to the user."""

    await update.message.reply_text(
        "Welcome to the Telegram Chat Summarizion Bot\n"
        "Use /Settings - To view and update your settings\n"
        "Use /Register to register new account\n"
        "Use /Help to see the available commands\n."
    )


# /register command handler
@allready_registered
async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """explain how to register with the bot."""

    guide_text = (
        "To register with the bot, follow these steps:\n\n"
        "1️⃣ **Create a Telegram Developer Account**:\n"
        "   - Go to [Telegram API Development Tools](https://my.telegram.org/auth).\n"
        "   - Log in using your phone number linked to Telegram.\n\n"
        "2️⃣ **Retrieve Your API Credentials**:\n"
        "   - After logging in, go to the **'API Development Tools'** section.\n"
        "   - Fill in the required fields to create a new application:\n"
        "     - Application Name: Can be anything.\n"
        "     - Short Description: doesnt realy matter.\n"
        "   - Submit the form and Telegram will provide:\n"
        "     - **API ID** (numeric key).\n"
        "     - **API Hash** (alphanumeric key).\n\n"
        "3️⃣ **Send Credentials to This Bot**:\n"
        "   - Copy your **API ID** and **API Hash**.\n"
        "   - Send them to the bot in the following format:\n"        
        "     YOUR_API_ID, YOUR_API_HASH\n"
        "     Example: `123456, abcdef123456`\n\n"
        "⚠️ *Note*: Your credentials will be securely stored, and sensitive messages will be deleted after processing.\n\n"
        "If you encounter any issues, type /help for assistance."
    )

    await update.message.reply_text(guide_text, parse_mode="Markdown", disable_web_page_preview=True)


async def scan_chats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await scan_chats_for_summarization(user_id)


# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here is a list of available commands:\n"
        "/Start - To start interacting with the bot\n"
        "/Settings - To view and update your settings\n"
        "/Help - To see the list of available commands\n"
        "/Scan - To scan all your chats for summarization\n"
    )




# Add command handlers to the application
interface_bot.add_handler(CommandHandler("Start", start_command))
interface_bot.add_handler(CommandHandler("Help", help_command))
interface_bot.add_handler(CommandHandler("Scan", scan_chats_command))
interface_bot.add_handler(CommandHandler("Register", register_command)) 

# Add message handler to the application
interface_bot.add_handler(MessageHandler(filters.TEXT, handle_api_key_and_hash))


# Start the bot
if __name__ == "__main__":
    interface_bot.run_polling()




