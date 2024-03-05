#!/usr/bin/env python3
import asyncio
import logging
import math
import os
import re
import json
import requests

from prettytable import PrettyTable
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, ConversationHandler, CallbackContext
from datetime import datetime

TOKEN = os.environ.get("TOKEN")
APP_URL = os.environ.get("APP_URL")
PORT = int(os.environ.get('PORT', '8443'))

# Hàm xử lý command /status
def status(update: Update, context: CallbackContext):
    api_url = 'https://namadafinder.cryptosj.net/sortedResults'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Create a PrettyTable instance
        table = PrettyTable()
        table.field_names = ["Address", "Voting Power", "Proposer Priority", "Alias", "Uptime", "Percentage"]
        
        # Add data to the table
        for entry in data:
            voting_power = entry['votingPower'] / 6
            truncated_address = entry['address'][:4] + "..." + entry['address'][-4:]
            table.add_row([truncated_address, voting_power, entry['proposerPriority'], entry['alias'], entry['uptime'], entry['percentage']])
        
        # Format the PrettyTable output as HTML inside a <pre> tag
        part_temp_table = f'<pre>{table.get_html_string()}</pre>'
        
        # Send the HTML-formatted table as a message
        update.effective_message.reply_text(part_temp_table, parse_mode=ParseMode.HTML)
    else:
        update.effective_message.reply_text("Không thể lấy dữ liệu từ API.")

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("status", status))


    # log all errors
    # dp.add_error_handler(error)

    # updater.start_polling()



    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_URL + TOKEN)
    updater.idle()

    return

if __name__ == '__main__':
    main()
