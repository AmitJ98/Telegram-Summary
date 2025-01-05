from pyrogram import Client
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv
from database_management import insert_new_user, fetch_user_data, delete_user, update_chat_list, update_time



load_dotenv()
INTERFACE_BOT_API_KEY = os.getenv("INTERFACE_BOT_API_KEY")

# Create the Application object
interface_bot = Application.builder().token(INTERFACE_BOT_API_KEY).build()


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
    
    if len(splited_message) != 2:
        await update.message.reply_text("Invalid input. Please follow the format and try again.")
        return

    api_id, api_hash = splited_message
    user_info = await verify_api_key_and_hash(api_id, api_hash, update.message.from_user.id)
    if user_info:
        pass
        #
        #   insert the user info into the database
        #
        await update.message.reply_text(f"Successfully registered! Your user ID: {user_info.id}")
        # 
        # need to delete the message of user where he sends me his keys
        #
        return

    else:
        await update.message.reply_text("Failed to verify your API Key and Hash. Please check them again.")
        return


# /start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """start command handler, send a welcome message to the user."""

    await update.message.reply_text(
        "Welcome to the Telegram Chat Summarizion Bot\n"
        "/settings - To view and update your settings\n"
        "Use /Register to register new account\n"
        "Use /help to see the available commands\n."
    )


# /register command handler
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


# /help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here is a list of available commands:\n"
        "/start - To start interacting with the bot\n"
        "/settings - To view and update your settings\n"
        "/help - To see the list of available commands\n"
    )




# Add command handlers to the application
interface_bot.add_handler(CommandHandler("start", start_command))
interface_bot.add_handler(CommandHandler("help", help_command))
interface_bot.add_handler(CommandHandler("register", register_command)) 

# Add message handler to the application
interface_bot.add_handler(MessageHandler(filters.TEXT, handle_api_key_and_hash))


# Start the bot
if __name__ == "__main__":
    interface_bot.run_polling()




