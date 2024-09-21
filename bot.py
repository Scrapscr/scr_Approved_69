import re
from telethon.sync import TelegramClient
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext
import os

# API credentials (Directly added here as requested)
api_id = 28328472
api_hash = 'c8f1f603401f2e4d41b191709f2481bf'
bot_token = '7869709672:AAF7Lx0NwlHVmWYdTUaaXRha8quwREQ1u5Q'

# Pattern for the format "number|mm|yy|code"
pattern = r'(\d+)\|(\d{2})\|(\d{2})\|(\d+)'

# Initialize the Telethon client
client = TelegramClient('session_name', api_id, api_hash)

# Function to scrape channel messages
async def scrape_channel(channel_name, message_limit):
    scraped_data = []
    async with client:
        async for message in client.iter_messages(channel_name, limit=message_limit):
            if message.text:
                matches = re.findall(pattern, message.text)
                for match in matches:
                    scraped_data.append(f"Found: {match}")
    return scraped_data

# Function to handle scraping requests from the user
def handle_scrape_request(update: Update, context: CallbackContext):
    user_input = update.message.text.strip()
    
    try:
        # Parse the input, expecting format like "MUMIRUDARKSIDE 100"
        channel_username, message_limit = user_input.split()
        message_limit = int(message_limit)

        # Notify the user that the scraping is starting
        update.message.reply_text(f"Starting to scrape {message_limit} messages from {channel_username}...")

        # Run the scraping task
        async def run_scrape():
            scraped_data = await scrape_channel(channel_username, message_limit)
            if scraped_data:
                for data in scraped_data:
                    update.message.reply_text(data)
            else:
                update.message.reply_text("No data found in the specified format.")

        client.loop.run_until_complete(run_scrape())

    except ValueError:
        update.message.reply_text("Invalid input format. Please use: <username/link> <number> (e.g., MUMIRUDARKSIDE 100)")

# Function to start the bot and send an intro message
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send the channel username/link and the number of messages to scrape in this format: <username/link> <number> (e.g., MUMIRUDARKSIDE 100)")

# Main function to run the bot
def main():
    # Initialize the bot with the provided token
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Handler for the /start command
    dispatcher.add_handler(CommandHandler("start", start))

    # Handler for user input (channel scrape requests)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_scrape_request))

    # Start polling for messages
    updater.start_polling()

    # Keep the bot running
    updater.idle()

if __name__ == '__main__':
    main()
