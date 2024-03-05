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
def status(update, context):
    api_url = 'https://namadafinder.cryptosj.net/sortedResults'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        html_message = "<b>Status</b>\n"
        html_message += "<table border='1'><tr><th>Address</th><th>Voting Power</th><th>Proposer Priority</th><th>Alias</th><th>Uptime</th><th>Percentage</th></tr>"
        for entry in data:
            voting_power = entry['votingPower'] / 6
            truncated_address = entry['address'][:4] + "..." + entry['address'][-4:]
            html_message += "<tr>"
            html_message += f"<td>{truncated_address}</td>"
            html_message += f"<td>{voting_power}</td>"
            html_message += f"<td>{entry['proposerPriority']}</td>"
            html_message += f"<td>{entry['alias']}</td>"
            html_message += f"<td>{entry['uptime']}</td>"
            html_message += f"<td>{entry['percentage']}</td>"
            html_message += "</tr>"
        html_message += "</table>"
        
        # Gửi tin nhắn HTML
        update.message.reply_html(html_message, parse_mode=telegram.ParseMode.HTML)
    else:
        update.message.reply_text("Không thể lấy dữ liệu từ API.")

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("status", status))


    # log all errors
    dp.add_error_handler(error)

    # updater.start_polling()



    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_URL + TOKEN)
    updater.idle()

    return

if __name__ == '__main__':
    main()
