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
        
        # Create PrettyTable
        table = create_table(data)
        if table:
            # Split the table into batches
            count_rows = len(table._rows)
            batch_size = 25
            for start in range(0, count_rows, batch_size):
                end = min(start + batch_size, count_rows)


                # batch_table = table[start:end]
                # # Format the batch table as plain text
                # plain_text_table = batch_table.get_string()
                temp_table = table.get_string(start=start, end=end)
                part_temp_table = f'<pre>{temp_table}</pre>'
                # Send the plain text table as a message                
                # update.effective_message.reply_text(plain_text_table)
                update.effective_message.reply_text(part_temp_table, parse_mode=ParseMode.HTML)
        else:
            update.effective_message.reply_text("Không thể tạo bảng từ dữ liệu.")
    else:
        update.effective_message.reply_text("Không thể lấy dữ liệu từ API.")

def create_table(data) -> PrettyTable:
    try:

        # Kiểm tra xem data có phải là chuỗi không
        if isinstance(data, str):
            # Nếu là chuỗi, chuyển đổi thành đối tượng Python
            json_data = json.loads(data)
        elif isinstance(data, list):
            # Nếu là danh sách, sử dụng trực tiếp
            json_data = data
        else:
            # Nếu không phải là chuỗi hoặc danh sách, xử lý lỗi hoặc trả về
            raise ValueError("Invalid data format")

        table = PrettyTable()
        headers = ["Address", "Voting Power", "Alias", "Uptime", "Percentage"]      
        table.align["Address"] = "l"
        table.align["Voting Power"] = "l"
        table.align["Alias"] = "l"
        table.align["Uptime"] = "l"
        table.align["Percentage"] = "l"
        table.title = "Top Validators"
        table.field_names = headers
        for entry in data:
            voting_power = entry['votingPower'] / 6
            truncated_address = entry['address'][:4] + "..." + entry['address'][-4:]
            table.add_row([truncated_address, voting_power, entry['alias'], entry['uptime'], entry['percentage']])
        
        return table
    except Exception as e:
        print(f"Error creating table: {e}")
        return None


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
