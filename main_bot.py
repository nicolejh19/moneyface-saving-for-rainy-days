import telebot
from telebot import types
from v1databasehelper import DBHelper
from datetime import datetime
import schedule
import time
from threading import Thread
from time import sleep
from _datetime import date
import logging
from genpie import chart
from decimal import *

bot = telebot.TeleBot("TOKEN")
dbhelper = DBHelper("NAME OF DATABASE")

main_menu_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu_buttons.add(types.KeyboardButton('Manage Savings'), types.KeyboardButton('Manage Spendings'), 
                    types.KeyboardButton('Promotions'), types.KeyboardButton('Manage Debts'),
                    types.KeyboardButton('$ocialite'), types.KeyboardButton('Help'))

my_s_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
my_s_button.add(types.KeyboardButton('Update'),types.KeyboardButton('My Records'),types.KeyboardButton('Back'))

update_spendings_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
update_spendings_button.add(types.KeyboardButton('Monthly Budget'),types.KeyboardButton('Daily Expenditure'),types.KeyboardButton('Back'))

update_savings_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
update_savings_button.add(types.KeyboardButton('Monthly Savings'),types.KeyboardButton('Bonus Savings'),types.KeyboardButton('Back'))

records_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
records_button.add(types.KeyboardButton('Current Month'), types.KeyboardButton('History'),types.KeyboardButton('Back'))

promotions_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
promotions_button.add(types.KeyboardButton('Food'),types.KeyboardButton('Clothes'),
                types.KeyboardButton('Transport'),types.KeyboardButton('Daily Necessities'),
                types.KeyboardButton('Others'),types.KeyboardButton('Back'))

promo_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
promo_button.add(types.KeyboardButton('Food'), types.KeyboardButton('Fashion'),
                types.KeyboardButton('Transport'), types.KeyboardButton('Daily Necessities'),
                types.KeyboardButton('Entertainment'), types.KeyboardButton('Student Deals'),types.KeyboardButton('Back'))

debt_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
debt_button.add(types.KeyboardButton('IOU'), types.KeyboardButton('UOMe'), types.KeyboardButton('Back'))

iou_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
iou_button.add(types.KeyboardButton('Show Debtees'), types.KeyboardButton('Update Debtees'),types.KeyboardButton('Back'))

uome_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
uome_button.add(types.KeyboardButton('Show Debtors'), types.KeyboardButton('Update Debtors'),types.KeyboardButton('Back'))

debtee_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
debtee_button.add(types.KeyboardButton('Add Debtee'), types.KeyboardButton('Delete Debtee'),types.KeyboardButton('Back'))

debtor_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
debtor_button.add(types.KeyboardButton('Add Debtor'), types.KeyboardButton('Delete Debtor'),types.KeyboardButton('Back'))

socialite_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
socialite_button.add(types.KeyboardButton('Challenge Friend'), types.KeyboardButton('Remind Friend'),types.KeyboardButton('Back'))

contact_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
contact_button.add(types.KeyboardButton(text='Share Contact', request_contact=True))

settings_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
settings_button.add(types.KeyboardButton('Reminders'), types.KeyboardButton('Help'), types.KeyboardButton('Back'))

opt_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
opt_button.add(types.KeyboardButton('Remind me hor'), types.KeyboardButton('Dunwan reminders'), types.KeyboardButton('Back'))

def is_float(amt):
    try:
        temp = float(amt)
        return True
    except ValueError as e:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    dbhelper.add_user(chat_id, username)
    start_text= "Welcome " + username + " to Saving for Rainy Days! 😄\nWe will guide you through rainy days and bring you luck to see the god of fortune.💰\n\nOur bot allows you to track your savings, spendings and debts. We also bring you easy access to promotions and encourage interactions with your friends in our $ocialite feature!\n\nTo begin your path to be in control of your wealth, press /main and we will guide you to your fortunes! If this is your first time using the bot, please go to Settings > Help in the main menu to learn how to use the bot.🤖 Good luck!\nWell wishes from Team MoneyFace🤑 "
    bot.send_message(chat_id=chat_id, text= start_text, reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['main'])
def main(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    main_text = "Hi " + username + "! Welcome to the main menu of Saving for Rainy Days! 😊"
    bot.send_message(chat_id=chat_id, text=main_text,reply_markup=main_menu_buttons)
    bot.clear_step_handler(message)
    bot.register_next_step_handler(message, process_next_step)

def process_next_step(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg == 'Manage Savings':
        body = "You have selected *Manage Savings*. 💰 \nTo input your monthly savings or bonus money received, select *Update*.💵 To track your current month savings and savings history, select *My Records*.🏦"
        bot.send_message(chat_id=chat_id, text= body,reply_markup= my_s_button,parse_mode="Markdown")
        bot.register_next_step_handler(message, process_my_savings)
    elif msg == 'Manage Spendings':
        body = "You have selected *Manage Spendings*. 💸\nSelect *Update* to input your monthly budget or daily expenditure.💵 Select *My Records* to track your current month expenditure and spending history. 🏦"
        bot.send_message(chat_id=chat_id, text= body,reply_markup= my_s_button, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_my_spendings)
    elif msg == 'Promotions':
        body = "You have selected *Promotions*. 🛒\nWe have curated the best resources for promotions for your easy access!😆\n(Even better: you don't have to subscribe and get spammed) Choose which category you want to get good deals from to become a saving guru now! 🤗"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=promo_button, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Manage Debts':
        body = "You have selected *Manage Debts*.🧾\nSelect *IOU* to update/review debtees and the amount YOU owe. Select *UOMe* to update/review your debtors and the amount THEY owe you. 💶"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=debt_button, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_debts)
    elif msg == '$ocialite':
        if dbhelper.is_user_phone_number_stored(chat_id):
            body = "You have selected *$ocialite*.👯 \nSelect *Challenge Friend* to challenge your friend to spend within an amount for this month! 💪 Select *Remind Friend* to remind your friend to pay you back! 😑"
            bot.send_message(chat_id=chat_id, text=body, reply_markup=socialite_button, parse_mode="Markdown")
            bot.register_next_step_handler(message, process_socialite)
        else:
            body = "To use this feature, we will require your contact. 📞 Please be assured that the information is used solely for engagement with your friends.🙂\nClick on the 'Share Contact' button below to share your contact with us. If you do not wish to share contact, type 'exit' to go back to main menu."
            bot.send_message(chat_id=chat_id, text=body, reply_markup=contact_button)
            bot.register_next_step_handler(message, extract_contact)
    elif msg == 'Settings':
        body = "You have selected *Settings*.✅\nSelect *Reminders* to decide if you want to receive our reminders.📝 Select *Help* to learn how to use this bot.📖"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=settings_button, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_settings)
    else: 
        bot.send_message(chat_id, text= "Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup= types.ReplyKeyboardRemove())

def process_my_savings(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Update':
        text = "To input your monthly savings at the start of each month, select *Monthly Savings* .\n\nJust received some money from your generous aunt or just received your scholarship money? 😎Go to *Bonus Savings* to increase your savings!"
        bot.send_message(chat_id=chat_id, text=text, reply_markup=update_savings_button, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_update_savings)
    elif msg == 'My Records':
        bot.send_message(chat_id=chat_id, text= "Do you want to check your current month savings or your savings history?", reply_markup=records_button)
        bot.register_next_step_handler(message, process_savings_records)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=main_menu_buttons)
        bot.register_next_step_handler(message, process_next_step)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.",reply_markup=types.ReplyKeyboardRemove())

def process_update_savings(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Monthly Savings':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        if not dbhelper.get_whether_current_monthly_saved(year_month, chat_id):
            text = "Please input your savings for this month. For example, if you want to save $888.88 this month, simply key in 888.88 😆 \n\nGod of Fortune says that the more you save, the richer you become! 🏦"
            bot.send_message(chat_id=chat_id, text=text, reply_markup= types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, process_monthly_savings)
        else:
            curr_savings = dbhelper.get_current_savings(year_month, chat_id)
            bot.send_message(chat_id=chat_id, text="Your savings for this month has already been set. In case you forgot, you have saved a total of $" + curr_savings + " this month. If you have extra savings, update your bonus savings instead. 💶")
            bot.register_next_step_handler(message, process_update_savings)
    elif msg == 'Bonus Savings':
        text = "Wah feeling rich now right! Good money drop from the sky.🥳 Key in how much more you want to save. For example, if your generous aunt gave you $88.88, just key in 88.88."
        bot.send_message(chat_id=chat_id, text=text, reply_markup= types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_bonus_savings)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=my_s_button)
        bot.register_next_step_handler(message, process_my_savings)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def process_monthly_savings(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if is_float(msg):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_monthly_savings(dt, year_month, msg, chat_id, 'MONTHLY')
        bot.send_message(chat_id=chat_id, text="Your savings for this month is $" + "{:.2f}".format(float(msg)) + ". 💶", reply_markup=update_savings_button)
        bot.register_next_step_handler(message, process_update_savings)
    elif msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text= "Exit",reply_markup=update_savings_button)
        bot.register_next_step_handler(message, process_update_savings)
    else:
        bot.send_message(chat_id=chat_id, text="Input your monthly savings properly leh.😠 If you want to save $888.88, just key in 888.88. If you don't intend to key in yet, type 'exit'.")
        bot.register_next_step_handler(message, process_monthly_savings)

def process_bonus_savings(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if is_float(msg):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        flag = dbhelper.add_monthly_savings(dt, year_month, msg, chat_id, 'BONUS')
        bot.send_message(chat_id=chat_id, text="Your bonus savings is $" + msg +".",reply_markup=update_savings_button)
        bot.register_next_step_handler(message, process_update_savings)
    elif msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text= "Exit", reply_markup=update_savings_button)
        bot.register_next_step_handler(message, process_update_savings)
    else:
        bot.send_message(chat_id=chat_id, text="Input your bonus savings properly leh. If you don't want to check in any bonus savings hor, then type 'exit'.")
        bot.register_next_step_handler(message, process_bonus_savings)

def is_aboveequal_average(current_amount, average_amount):
    if current_amount > average_amount:
        return ">"
    elif current_amount == average_amount:
        return "="
    else:
        return "<"

def process_savings_records(message):
    chat_id = message.from_user.id
    msg = message.text
    unix_date = int(message.date)
    dt = datetime.utcfromtimestamp(unix_date)
    year_month = str(dt.year) + str(dt.month)
    bot.clear_step_handler(message)
    if msg == 'Current Month':
        curr_savings = dbhelper.get_current_savings(year_month, chat_id)
        if is_float(curr_savings):
            average_savings = dbhelper.get_average_monthly_savings(chat_id)
            symflag = is_aboveequal_average(float(curr_savings), average_savings)
            if symflag == ">":
                comparison = "\nGood job! Your savings for this month is above the average savings for the past months. God of Fortune is proud of you."
            elif symflag == "=":
                comparison = "\nYour savings for this month is the same as the average savings for the past months. Keep on saving!"
            else:
                comparison = "\nYour savings for this month is below the average savings for the past months. Try to save more okay, you never know when there will be rainy days."
            bot.send_message(chat_id=chat_id, text="Here's the statistics:\n🗓 Savings for the current month: $" + curr_savings + "\n🗓 Average monthly savings: $" +  str(average_savings) + comparison)
        else:
            bot.send_message(chat_id=chat_id, text=curr_savings)
        bot.register_next_step_handler(message, process_savings_records)
    elif msg == 'History':
        total_savings = dbhelper.get_total_savings(chat_id)
        if total_savings != "0.00" and dbhelper.has_history_savings(chat_id, year_month):
            average_savings = dbhelper.get_average_monthly_savings(chat_id)
            send_text = "Here's the statistics:\n🗓 Total savings since using Saving for Rainy Days: $" + total_savings + "\n🗓Average monthly savings: $" +  str(average_savings) + "\nKeep on saving!"
        else:
            send_text = "There is no history of your savings. Keep saving and using Saving for Rainy Days to see your records next month!"
        bot.send_message(chat_id=chat_id, text=send_text)
        bot.register_next_step_handler(message, process_savings_records)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=my_s_button)
        bot.register_next_step_handler(message, process_my_savings)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def process_my_spendings(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Update':
        text = "To input your monthly budget at the start of each month, select *Monthly Budget*.\n\nJust bought your favourite bubble tea or spent on other things? 😔Go to *Daily Expenditure* to key in your spendings."
        bot.send_message(chat_id=chat_id, text= text, reply_markup=update_spendings_button)
        bot.register_next_step_handler(message, process_update)
    elif msg == 'My Records':
        text = "Do you want to check your current month expenditure or your spending history? Tracking your spendings makes you the one in control of your finances. 😎"
        bot.send_message(chat_id=chat_id, text= text, reply_markup=records_button)
        bot.register_next_step_handler(message, process_records)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=main_menu_buttons)
        bot.register_next_step_handler(message, process_next_step)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())   
     
def process_update(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg == 'Monthly Budget':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        if not is_float(dbhelper.get_monthly_budget(year_month, chat_id)):
            text = "Please input your budget for this month. For example, if you intend to set aside $300.50 for this month, just key in 300.5 😉\n\nSetting a reasonable budget is key to managing your finances. 💪"
            bot.send_message(chat_id=chat_id, text=text,reply_markup= types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, process_monthly_budget)
        else:
            curr_budget = dbhelper.get_monthly_budget(year_month, chat_id)
            bot.send_message(chat_id=chat_id, text="Your budget for this month has already been set. In case you forgot, I tell you again lah. $" + curr_budget + " 🤑")
            bot.register_next_step_handler(message, process_update)
    elif msg == 'Daily Expenditure':
        bot.send_message(chat_id=chat_id, text="Select the category to input your expenditure. Always remember to spend within your budget that you've planned! 💪", reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=my_s_button)
        bot.register_next_step_handler(message, process_my_spendings)
    else:
        bot.send_message(chat_id=chat_id, text= "Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def process_monthly_budget(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if is_float(msg):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_monthly_budget(year_month, msg, chat_id)
        bot.send_message(chat_id=chat_id, text="Your budget for this month is $" + "{:.2f}".format(float(msg)) + ". 🤑", reply_markup=update_spendings_button)
        bot.register_next_step_handler(message, process_update)
    elif msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text= "Exit", reply_markup=update_spendings_button)
        bot.register_next_step_handler(message, process_update)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget properly lah.🙄 If you prepared $200.50 to spend, just key in 200.5. 😌 If you don't want to key in yet, then type 'exit'.")
        bot.register_next_step_handler(message, process_monthly_budget)

def process_daily_expenditure(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Food':
        bot.send_message(chat_id=chat_id, text= "Input your expenditure for food. 🍱 If you spent $4.50 for lunch, key in 4.5.",reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_food)
    elif msg == 'Clothes':
        bot.send_message(chat_id=chat_id, text= "Input your expenditure for clothes. 🧥👗👔 If you spent $30 on a jacket, key in 30.", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_clothes)
    elif msg == 'Transport':
         bot.send_message(chat_id=chat_id, text= "Input your expenditure for transport. 🚇🚌 If your MRT fare was $1.77, key in 1.77.",reply_markup=types.ReplyKeyboardRemove())
         bot.register_next_step_handler(message, process_transport)
    elif msg == 'Daily Necessities':
         bot.send_message(chat_id=chat_id, text= "Input your expenditure for daily necessities. 🛍 If you spent $3.50 on a mask (necessity now), key in 3.5",reply_markup=types.ReplyKeyboardRemove())
         bot.register_next_step_handler(message, process_necessities)
    elif msg == 'Others':
        bot.send_message(chat_id=chat_id, text= "Input your expenditure for others (e.g. Entertainment). 🎭🎰 If you spent $15 in cinema, key in 15.",reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_others)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=update_spendings_button)
        bot.register_next_step_handler(message, process_update)
    else:
        bot.send_message(chat_id=chat_id, text= "Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def spending_warning(user_id, year_month):
    curr_monthly_exp = dbhelper.get_monthly_exp(user_id, year_month)
    curr_month_budget = dbhelper.get_monthly_budget(year_month, user_id)
    if is_float(curr_month_budget):
        perc_used = ((Decimal(curr_monthly_exp) / Decimal(curr_month_budget)) * 100).quantize(Decimal('1.00'))
        if perc_used > 100:
            res = "\n❗️❗️❗️ You have exceeded your budget of $" + curr_month_budget + " this month. 😧 Try to limit your expenditure to a minimum from now on and try harder to keep within your budget next month!"
        elif perc_used == 100:
            res = "\n❗️❗️❗️ You have hit your budget of $" + curr_month_budget + " this month. 😧 Try to limit your expenditure to a minimum from now on and try harder to keep within your budget next month!"
        elif perc_used >= 90:
            amt_left = (Decimal(curr_month_budget) - Decimal(curr_monthly_exp)).quantize(Decimal('1.00'))
            res = "\n❗️❗️ You have spent beyond 90% of your budget of $" + curr_month_budget + " this month. 😧 Try not to exceed your budget this month!\nYou have $" + str(amt_left) + " of your budget left. Spend wisely!"
        else:
            res = ""
    else:
        res = "\nReminder! You have not set your budget this month. Like that how to manage your finances? Go set your budget now! 🤑"
    return res
    
def process_food(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    bot.clear_step_handler(message)
    if is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'FOOD', amount, chat_id, year_month)
        warning_msg = spending_warning(chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on food today. Don't spend too much on junk food okay!" + warning_msg, reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for food properly leh.🤨 If never spend, just input '0' okay!")
        bot.register_next_step_handler(message, process_food)

def process_clothes(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    bot.clear_step_handler(message)
    if is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'CLOTHES', amount, chat_id, year_month)
        warning_msg = spending_warning(chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on clothes today. Don't buy excessively okay!" + warning_msg, reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for clothes properly leh.🤨 If never spend, just input '0' okay! ")
        bot.register_next_step_handler(message, process_clothes)

def process_transport(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    bot.clear_step_handler(message)
    if is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'TRANSPORT', amount, chat_id, year_month)
        warning_msg = spending_warning(chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on transport today. Travel cheaply via public transport okay!" + warning_msg, reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for transport properly leh.🤨If never spend, just input '0' okay!")
        bot.register_next_step_handler(message, process_transport)

def process_necessities(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    bot.clear_step_handler(message)
    if is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'NECESSITIES', amount, chat_id, year_month)
        warning_msg = spending_warning(chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on daily necessities today. Remember to buy only what you need!" + warning_msg,reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for daily necessities properly leh.🤨If never spend, just input '0' okay!")
        bot.register_next_step_handler(message, process_necessities)

def process_others(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    bot.clear_step_handler(message)
    if is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'OTHERS', amount, chat_id, year_month)
        warning_msg = spending_warning(chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on others today. Remember to spend within your budget!" + warning_msg, reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for 'others' properly leh.🤨 If never spend, just input '0' okay!")
        bot.register_next_step_handler(message, process_others)

def process_records(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Current Month':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        curr_exp = dbhelper.get_monthly_exp(chat_id, year_month)
        curr_budget = dbhelper.get_monthly_budget(year_month, chat_id)
        if not is_float(curr_exp):
            bot.send_message(chat_id=chat_id, text="You have not recorded your expenditure for this month. Go update your expenditure leh.")
        elif not is_float(curr_budget):
            bot.send_message(chat_id=chat_id, text="You have not set your budget for this month. Go set your budget leh.")
        else: 
            total_spending = float(curr_exp)
            curr_food_exp = float(dbhelper.get_monthly_category_exp(chat_id, year_month, 'FOOD'))
            curr_clothes_exp = float(dbhelper.get_monthly_category_exp(chat_id, year_month, 'CLOTHES'))
            curr_transport_exp = float(dbhelper.get_monthly_category_exp(chat_id, year_month, 'TRANSPORT'))
            curr_necc_exp = float(dbhelper.get_monthly_category_exp(chat_id, year_month, 'NECESSITIES'))
            curr_others_exp = float(dbhelper.get_monthly_category_exp(chat_id, year_month, 'OTHERS'))
            food = (curr_food_exp/total_spending) * 100
            clothes = (curr_clothes_exp/ total_spending) * 100
            transport = (curr_transport_exp/ total_spending) * 100
            necc = (curr_necc_exp/ total_spending) * 100
            others = (curr_others_exp / total_spending) * 100
            thePie = chart()
            highest_cat = thePie.make_piechart(food, clothes, transport, necc, others, monthly=False)
            perc_budget_used = ((Decimal(curr_exp) / Decimal(curr_budget)) * 100).quantize(Decimal('1.00'))
            if perc_budget_used > 100:
                warn_msg = "❗️❗️❗️ You have exceeded your budget this month! God of Fortune is disappointed. 🥺 Try harder next month!"
            elif perc_budget_used >= 90:
                warn_msg = "❗️❗️ You have hit or exceeded 90% of your budget set for the month! 😧 Be extra careful not to exceed your budget okay!"
            elif perc_budget_used >= 70:
                warn_msg = "❗️ You have hit or exceeded 70% of your budget set for the month! 🤑 Be careful not to exceed your budget okay!"
            else:
                warn_msg = ""
            bot.send_message(chat_id=chat_id, text="Here's the statistics:\n🗓 Budget for this month: $" + curr_budget + "\n🗓 Total spending for this month: $" + curr_exp + "\n🗓 Category with highest spending: " + highest_cat + "\n🗓 Percentage of budget used: " + str(perc_budget_used) + "%\n" + warn_msg + "Here is a breakdown of your spendings this month as shown in the pie chart below.\n")
            bot.send_photo(chat_id=chat_id, photo=open('/.../current.png' ,'rb')) #get path
        bot.register_next_step_handler(message, process_records)
    elif msg == 'History':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        average_monthly_exp = dbhelper.get_average_monthly_exp(chat_id)
        num_months_exp = dbhelper.get_num_months_exp(chat_id)
        if num_months_exp == 0 or not is_float(average_monthly_exp):
            bot.send_message(chat_id=chat_id, text="History of your spendings not available yet. Keep on tracking and you will see it next month!")
        else:
            percentage_of_months_within_budget = dbhelper.get_percentage_within_budget(chat_id)
            num_months_exceed = dbhelper.get_num_exceed_budget(chat_id)
            if Decimal(percentage_of_months_within_budget) == Decimal(100.00):
                resp_msg = "Excellent! 👏🏻 You have kept within budget all the time! 🥳 God of Fortune is very proud of you."
            elif Decimal(percentage_of_months_within_budget) >= Decimal(75.00):
                resp_msg = "Keep up the good work! 😊 Sticking to a budget may not be easy, but you have shown that you can do it! 🥰"
            elif Decimal(percentage_of_months_within_budget) >= Decimal(50.00):
                resp_msg = 'Keep trying! As the quote says, "Money, like emotions, is something you must control to keep your life on the right track.", try to control your expenditure. It may not be easy, but you can do it! 🥰'
            else:
                resp_msg = '😧 Try harder to keep within your budget every month! Here\'s a small piece of advice from Benjamin Franklin, “Beware of little expenses; a small leak will sink a great ship.” 💪🏻 Start controlling your expenditure today!'
            bot.send_message(chat_id=chat_id, text="Here's the statistics:\n🗓 Average monthly expenditure: $" + average_monthly_exp + "\n🗓 Out of " + str(num_months_exp) + " months of using Saving for Rainy Days, you have exceeded your budget " + str(num_months_exceed) + " times.\n🗓 Percentage of months successfully spending within budget: " + percentage_of_months_within_budget + "%\n" + resp_msg)
        bot.register_next_step_handler(message, process_records)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=my_s_button)
        bot.register_next_step_handler(message, process_my_spendings)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def process_promotions(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Food':
        bot.send_message(chat_id=chat_id, text= "☕️Look for cheap and good deals to satisfy your taste buds at SG Kiasu Foodies!🍜 \nDon't view it when you are on a diet though! 😜 \nt.me/kiasufoodies")
        bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Fashion':
        bot.send_message(chat_id=chat_id, text= "Bringing you the latest fashion promotions by SG Budget Babes! 👟\nGuys, don't be fooled by the name 👔, who says you ain't a babe? 😉\nBe a fashionista and a saving guru at the same time! 🕶\nt.me/budgetbabes")
        bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Transport':
         bot.send_message(chat_id=chat_id, text= "Travel cheaply with SG Cab Promos! 🚖\nDon't be fooled by it's name though, it provides promotions for other ride-hailing services aside from taxis! 🚘 \nt.me/sgcabcodes")
         bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Daily Necessities':
         bot.send_message(chat_id=chat_id, text= "Check out some good deals that you need in your daily life at SG Daily Deals & Lifestyle Hacks.💰\nHack your way through to becoming a saving guru! 💪\nt.me/SBsmarterway")
         bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Entertainment':
        bot.send_message(chat_id=chat_id, text= "Not sure how to have fun without spending too much? 🎮 Check out SG Weekend Plans that suggest some events for you to engage in for FREE! 👩‍💻\nt.me/sgweekend")
        bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Student Deals':
        bot.send_message(chat_id=chat_id, text= "A special category for YOU students 👨‍🎓 who especially need to save for your future!\nEnjoy the perks of being a student with these promotions specially for you at SG Student Promos! 👩🏽‍🎓\nt.me/sgstudentpromos")
        bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=main_menu_buttons)
        bot.register_next_step_handler(message, process_next_step)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def process_debts(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg == 'IOU':
        body = "To review your list of debtees, select *Show Debtees*. If you want to add or delete debtee from the list, select *Update Debtees*. 💸"
        bot.send_message(chat_id=chat_id, text= body, reply_markup=iou_button,parse_mode= "Markdown")
        bot.register_next_step_handler(message, process_iou)
    elif msg == 'UOMe':
        body = "To review your list of debtors, select *Show Debtors*. If you want to add or delete debtor from the list, select *Update Debtors*. 💸"
        bot.send_message(chat_id, text=body, reply_markup=uome_button, parse_mode= "Markdown")
        bot.register_next_step_handler(message, process_uome)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=main_menu_buttons)
        bot.register_next_step_handler(message, process_next_step)
    else:
        bot.send_message(chat_id=chat_id,text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def process_iou(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg == 'Show Debtees':
        all_debtees = dbhelper.get_all_debtees(chat_id)
        if not all_debtees:
            bot.send_message(chat_id=chat_id, text="Good! You don't owe anyone money!")
        else:
            res = "Here is a list of people you owe:\n"
            for i in all_debtees:
                res += i[0] + ": $" + i[1] + "\n"
            res += "Hurry save save save and buy only discounted items so that you can pay them back asap!"
            bot.send_message(chat_id=chat_id, text=res)
        bot.register_next_step_handler(message, process_iou)
    elif msg == 'Update Debtees':
        bot.send_message(chat_id=chat_id, text="Do you want to add or delete debtees?",reply_markup=debtee_button)
        bot.register_next_step_handler(message, update_debtee)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=debt_button)
        bot.register_next_step_handler(message, process_debts)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.",reply_markup=types.ReplyKeyboardRemove())

def process_uome(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg == 'Show Debtors':
        all_debtors = dbhelper.get_all_debtors(chat_id)
        if not all_debtors:
            bot.send_message(chat_id=chat_id, text="Good! No one owes you money.")
        else:
            res = "Here is a list of people who owe you:\n"
            for i in all_debtors:
                res += i[0] + ": $" + i[1] + "\n"
            res += "Hurry chase for your money back! The longer you wait the more they will forget. Use $ocialite at main menu to remind your friends if you shy."
            bot.send_message(chat_id=chat_id, text=res)
        bot.register_next_step_handler(message, process_uome)
    elif msg == 'Update Debtors':
        bot.send_message(chat_id=chat_id, text="Do you want to add or delete debtors?",reply_markup=debtor_button)
        bot.register_next_step_handler(message, update_debtor)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=debt_button)
        bot.register_next_step_handler(message, process_debts)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.",reply_markup=types.ReplyKeyboardRemove())

def update_debtee(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg == 'Add Debtee':
        body = "To add a debtee, please input in the following format: “[name of debtee],[amount you owed]“.\nE.g. If you owed Tan Ah Long $50, then key in Tan Ah Long,50. Do check before keying in and do not leave any spacing.🙂"
        bot.send_message(chat_id=chat_id, text=body, reply_markup= types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_debtee)
    elif msg == 'Delete Debtee':
        body = "Congratulations on paying back what you’ve owed!🥳 To delete a debtee, simply input the name of the debtee that is in your debtee list. \nE.g. If you have cleared your debts with Tan Ah Long, then simply key in Tan Ah Long."
        bot.send_message(chat_id=chat_id, text= body, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, delete_debtee)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=iou_button)
        bot.register_next_step_handler(message, process_iou)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def add_debtee(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Exit", reply_markup=debtee_button)
        bot.register_next_step_handler(message, update_debtee)
    else: 
        arr = msg.split(",")
        try:
            name_debtee, amt = arr[0], arr[1]
            dbhelper.add_debtee_iou(chat_id, name_debtee.upper(), amt)
            body = "You owed " + name_debtee + " $" + amt + " and it has been added to your debtee list. Remember to faster pay back okay!"
            bot.send_message(chat_id=chat_id, text=body, reply_markup=debtee_button)
            bot.register_next_step_handler(message, update_debtee)
        except IndexError:
            bot.send_message(chat_id=chat_id, text="Please follow the format for input.🙂 If you don't want to add debtee, input 'exit'.")
            bot.register_next_step_handler(message, add_debtee)

def delete_debtee(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Exit", reply_markup=debtee_button)
        bot.register_next_step_handler(message, update_debtee)
    else: 
        if dbhelper.is_debtee_present_iou(chat_id, msg.upper()):
            dbhelper.delete_debtee_iou(chat_id, msg.upper())
            bot.send_message(chat_id=chat_id,text="You have removed " + msg + " from your debtee list. Good job!", reply_markup=debtee_button)
            bot.register_next_step_handler(message, update_debtee)
        else:
            body = "The name you've keyed in is not in our database. Please check if you have keyed in the name of your debtee correctly or check if the person is in your debtee list and input again. If you have no debtee to delete, then input 'exit'."
            bot.send_message(chat_id=chat_id,text=body)
            bot.register_next_step_handler(message, delete_debtee)

def update_debtor(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg == 'Add Debtor':
        body = "To add a debtor, please input in the following format: “[name of debtor],[amount they owed you]“.\nE.g. If you lent Tan Ah Beng $50, then key in Tan Ah Beng,50. Do check before keying in and do not leave any spacing.🙂"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_debtor)
    elif msg == 'Delete Debtor':
        body = "Congratulations on receiving back your money!🥳 To delete a debtor, simply input the name of the debtor that is in your debtor list. \nE.g. If Tan Ah Beng paid you back, then simply key in Tan Ah Beng."
        bot.send_message(chat_id=chat_id, text=body, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, delete_debtor)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=uome_button)
        bot.register_next_step_handler(message, process_uome)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def add_debtor(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Exit", reply_markup=debtor_button)
        bot.register_next_step_handler(message, update_debtor)
    else: 
        arr = msg.split(",")
        try:
            name_debtor, amt = arr[0], arr[1]
            dbhelper.add_debtor_uome(chat_id, name_debtor.upper(), amt)
            body = "You lent " + arr[0] + " $" + arr[1] + " and it has been added to your debtor list. If you shy ah, can use our $ocialite feature to remind them to pay back okay!"
            bot.send_message(chat_id=chat_id, text=body, reply_markup=debtor_button)
            bot.register_next_step_handler(message, update_debtor)
        except IndexError:
            bot.send_message(chat_id=chat_id, text="Please follow the format for input.🙂 If you don't want to add debtor, input 'exit'.")
            bot.register_next_step_handler(message, add_debtor)

def delete_debtor(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.clear_step_handler(message)
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Exit", reply_markup=debtor_button)
        bot.register_next_step_handler(message, update_debtor)
    else: 
        if dbhelper.is_debtor_present_uome(chat_id, msg.upper()):
            dbhelper.delete_debtor_uome(chat_id, msg.upper())
            bot.send_message(chat_id=chat_id,text="You have removed " + msg + " from your debtor list. Good job!", reply_markup=debtor_button)
            bot.register_next_step_handler(message, update_debtor)
        else:
            body = "The name you've keyed in is not in our database. Please check if you have keyed in the name of your debtor correctly or check if the person is in your debtor list and input again. If you have no debtor to delete, then input 'exit'."
            bot.send_message(chat_id=chat_id,text=body)
            bot.register_next_step_handler(message, delete_debtor)
            
def extract_contact(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    bot.clear_step_handler(message)
    try: 
        contact = message.contact.phone_number
        if contact[0] != '+':
            contact = '+' + contact
        dbhelper.update_phone_number(chat_id, contact)
        body = "Great! 🥳 Select *Challenge Friend* to challenge your friend to spend within an amount for this month! 💪 Select *Remind Friend* to remind your friend to pay you back! 😑"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=socialite_button,parse_mode="Markdown"))
        bot.register_next_step_handler(message, process_socialite)
    except Exception as err:
        bot.send_message(chat_id=chat_id, text="Sending you back... 🙂", reply_markup=main_menu_buttons)
        bot.register_next_step_handler(message, process_next_step)

def process_socialite(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Challenge Friend':
        body = "To challenge your friend to spend within a reasonable amount that you decide for this month, please input your friend's contact number together with the amount to challenge. ☎️ Please input in the following format: “+[country code][number],[amount]”. \nE.g. if your friend’s number is 91234567 and his/her country code is 65 and the amount to challenge is $300, then key in +6591234567,300. Do check before keying in and do not leave any spacing.🙂"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, challenge_friend)
    elif msg == 'Remind Friend':
        body = "To remind your friend to pay you back the amount he/she owed you, please input your friend's contact number and the amount. ☎️ Please input in the following format: “+[country code][number],[amount]”. \nE.g. if your friend’s number is 91234567 and his/her country code is 65 and the amount he/she owed you is $50, then key in +6591234567,50. Do check before keying in and do not leave any spacing.🙂"
        bot.send_message(chat_id=chat_id, text= body, reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, remind_friend)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=main_menu_buttons)
        bot.register_next_step_handler(message, process_next_step)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())
       
def challenge_friend(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Exit", reply_markup=socialite_button)
        bot.register_next_step_handler(message, process_socialite)
    else:
        arr = msg.split(",")
        try: 
            friend_number, amt = arr[0], arr[1]
            if dbhelper.is_user_stored(friend_number):
                if is_float(arr[1]):
                    unix_date = int(message.date)
                    dt = datetime.utcfromtimestamp(unix_date)
                    year_month = str(dt.year) + str(dt.month)
                    friend_chat_id = dbhelper.get_user_id(friend_number)
                    friend_name = dbhelper.get_username(friend_chat_id)
                    flag = dbhelper.add_challenge(year_month, chat_id, friend_chat_id, amt)
                    if flag: 
                        bot.send_message(chat_id=friend_chat_id, text="Challenge Accepted!👌Are you up to face the challenge issued by " + username + "? You have been challenged to spend only $"+ amt +" this month!😣 Do your best and prove that YOU are the saving guru to "+ username + "! Do explore the Promotions feature to help you! 🙃 ")
                        bot.send_message(chat_id=chat_id, text="You have successfully challenged your friend!👍 Let's hope your friend can succeed the challenge.",reply_markup=socialite_button)
                    else:
                        bot.send_message(chat_id=chat_id, text="You already challenged " + friend_name + " to spend $" + amt + " for this month leh... Can give your friend a break and re-challenge next month again? 🙃Meanwhile you also up your game to be the saving guru by tracking your spendings can?", reply_markup=socialite_button)
                    bot.register_next_step_handler(message, process_socialite)
                else:
                    bot.send_message(chat_id=chat_id, text="Key in the amount properly leh.🤨 If you think your friend confirm cmi and don't want to challenge anymore, type 'exit'.")
                    bot.register_next_step_handler(message, challenge_friend)
            else:
                body = "Unfortunately, the contact that you keyed in is not in our database.😪 Get your friend to use 'Saving for Rainy Days' today and activate the $ocialite feature to interact with your friends!😀"
                bot.send_message(chat_id=chat_id, text=body, reply_markup=socialite_button)
                bot.register_next_step_handler(message, process_socialite)
        except IndexError:
            bot.send_message(chat_id=chat_id, text="Key in the number and amount properly leh.🤨 If you think your friend confirm cmi and don't want to challenge anymore, type 'exit'.\nOtherwise, please input in the following format: “+[country code][number],[amount]”. Do check before keying in and do not leave any spacing.🙂")
            bot.register_next_step_handler(message, challenge_friend)

def remind_friend(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Exit", reply_markup=socialite_button)
        bot.register_next_step_handler(message, process_socialite)
    else:
        arr = msg.split(",")
        try: 
            friend_number, amt = arr[0], arr[1]
            if dbhelper.is_user_stored(friend_number):
                if is_float(amt):
                    friend_chat_id = dbhelper.get_user_id(friend_number)
                    bot.send_message(chat_id=friend_chat_id, text="O$P$: Hearsay you still owe " + username + " $" + str(amt) + " 💰ah...Can pay back quickly or not… 😠 People also need to save money one leh…")
                    bot.send_message(chat_id=chat_id, text="We have helped you chase your friend to pay you back!💵 Hopefully, your money comes back to you quickly.", reply_markup=socialite_button)
                    bot.register_next_step_handler(message, process_socialite)
                else:
                    bot.send_message(chat_id=chat_id, text="Key in the amount properly leh.🤨 If your friend already paid you back and no need to bug them anymore, type 'exit'.")
                    bot.register_next_step_handler(message, remind_friend)
            else:
                body = "Unfortunately, the contact that you keyed in is not in our database.😪 Get your friend to use 'Saving for Rainy Days' today and activate the $ocialite feature to interact with your friends!😀"
                bot.send_message(chat_id=chat_id, text=body, reply_markup=socialite_button)
                bot.register_next_step_handler(message, process_socialite)
        except IndexError:
            bot.send_message(chat_id=chat_id, text="Key in the number and amount properly leh.🤨 If your friend already paid you back and no need to bug them anymore, type 'exit'.\nOtherwise, please input again in the following format: “+[country code][number],[amount]”. Do check before keying in and do not leave any spacing.🙂")
            bot.register_next_step_handler(message, remind_friend) 

def process_settings(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Reminders':
        body = "Do you want to receive our daily and monthly reminders?"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=opt_button)
        bot.register_next_step_handler(message, process_opt)
    elif msg == 'Help':
        body = "*How to use Saving for Rainy Days?*\n\nVisit https://tinyurl.com/savingforrainydays to find out! 🌐"
        bot.send_message(chat_id=chat_id, text=body, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_settings)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=main_menu_buttons)
        bot.register_next_step_handler(message, process_next_step)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())   
     
def process_opt(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    bot.clear_step_handler(message)
    if msg == 'Remind me hor':
        dbhelper.switch_on_reminder(chat_id)
        bot.send_message(chat_id=chat_id, text="We will send you daily reminders and your monthly report.")
        bot.register_next_step_handler(message, process_opt)
    elif msg == 'Dunwan reminders':
        dbhelper.switch_off_reminder(chat_id)
        bot.send_message(chat_id=chat_id, text="We trust that you will key in your daily expenditure on your own ah. No reminders will be sent to you already.")
        bot.register_next_step_handler(message, process_opt)
    elif msg == 'Back':
        bot.send_message(chat_id=chat_id, text= "Sending you back...", reply_markup=settings_button)
        bot.register_next_step_handler(message, process_settings)
    else:
        bot.send_message(chat_id=chat_id, text="Please note that our bot interacts with you mainly through the buttons.😅 Press /main to be redirected back to the main menu.", reply_markup=types.ReplyKeyboardRemove())

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(10)

def get_savings_msg(past_month_savings):
    if is_float(past_month_savings):
        savings_msg = "$" + past_month_savings
    else:
        savings_msg = "No records of savings last month"
    return savings_msg

def get_ave_savings_msg(average_savings):
    if average_savings != 0:
        ave_savings_msg = "$" + str(average_savings)
    else:
        ave_savings_msg = "No history of savings available"
    return ave_savings_msg

def get_budget_msg(past_month_budget):
    if is_float(past_month_budget):
        budget_msg = "$" + past_month_budget
    else:
        budget_msg = "No budget set last month"
    return budget_msg

def get_succ_or_fail_msg(past_month_budget, past_month_exp):
    if is_float(past_month_budget) and is_float(past_month_exp):
        if Decimal(past_month_exp) <= Decimal(past_month_budget):
            succ_or_fail_msg = "\n🥳 Congrats! You successfully kept within budget last month!"
        else:
            succ_or_fail_msg = "\n😔 You did not manage to spend within budget last month. Try harder this month! 💪🏻"
    else:
        succ_or_fail_msg = ""
    return succ_or_fail_msg

def get_exp_msg(past_month_exp):
    if is_float(past_month_exp): 
        exp_msg = "$" + past_month_exp 
    else:
        exp_msg = "No records of expenditure last month"
    return exp_msg

def get_ave_exp_msg(average_exp):
    if not is_float(average_exp):
        ave_exp_msg = "No history of expenditure available"
    else:
        ave_exp_msg = "$" + average_exp
    return ave_exp_msg

def monthly():
    # dbhelper.test_monthly_overview_1()
    if date.today().day == 1:
        list_of_users = dbhelper.get_all_users()
        year_month = str(date.today().year) + str(date.today().month - 1)
        for i in list_of_users:
            if dbhelper.wants_reminder(i):
                past_month_exp = dbhelper.get_monthly_exp(i, year_month)
                past_month_savings = dbhelper.get_current_savings(year_month, i)
                past_month_budget = dbhelper.get_monthly_budget(year_month, i)
                average_savings = dbhelper.get_average_monthly_savings(i)
                savings_msg = get_savings_msg(past_month_savings)
                ave_savings_msg = get_ave_savings_msg(average_savings)
                budget_msg = get_budget_msg(past_month_budget)
                succ_or_fail_msg = get_succ_or_fail_msg(past_month_budget, past_month_exp)
                exp_msg = get_exp_msg(past_month_exp)
                average_exp = dbhelper.get_average_monthly_exp(i)
                ave_exp_msg = get_ave_exp_msg(average_exp)
                default_msg = "It is a new month!🤗 Start planning for your monthly savings and budget. Here's a summary of your savings and spendings last month:\n🗓 Monthly savings: " + savings_msg + "\n🗓 Average monthly savings: " + ave_savings_msg + "\n🗓 Monthly budget: " + budget_msg + "\n🗓 Monthly expenditure: " + exp_msg + "\n🗓 Average monthly expenditure: " + ave_exp_msg 
                if is_float(past_month_exp): ### GOT PAST MONTH EXPENDITURE ###
                    flag = dbhelper.add_monthly_exp(i, year_month)
                    total_spending = float(past_month_exp)
                    curr_food_exp = float(dbhelper.get_monthly_category_exp(i, year_month, 'FOOD'))
                    curr_clothes_exp = float(dbhelper.get_monthly_category_exp(i, year_month, 'CLOTHES'))
                    curr_transport_exp = float(dbhelper.get_monthly_category_exp(i, year_month, 'TRANSPORT'))
                    curr_necc_exp = float(dbhelper.get_monthly_category_exp(i, year_month, 'NECESSITIES'))
                    curr_others_exp = float(dbhelper.get_monthly_category_exp(i, year_month, 'OTHERS'))
                    food = (curr_food_exp/total_spending) * 100
                    clothes = (curr_clothes_exp/ total_spending) * 100
                    transport = (curr_transport_exp / total_spending) * 100
                    necc = (curr_necc_exp/ total_spending) * 100
                    others = (curr_others_exp / total_spending) * 100
                    monthly = chart()
                    spent_most = monthly.make_piechart(food, clothes, transport, necc, others)
                    default_msg += "\n🗓 Category with highest spendings: " + spent_most + succ_or_fail_msg
                    bot.send_message(chat_id=i, text=default_msg)
                    bot.send_photo(chat_id=i, photo=open('/Users/User/Downloads/Orbital/Versions/monthly.png' ,'rb'))  
                else:
                    bot.send_message(chat_id=i, text=default_msg)
    else:
        return

def monthly_challenges():
    # dbhelper.test_add_challenge("INSERT USER ID", "INSERT USER ID", "300")            
    # dbhelper.test_add_challenge("INSERT USER ID", "INSERT USER ID", "90")
    # test_c = dbhelper.test_all_challenges()
    # for i in test_c:
    #     print("challenger: " + str(i[0]) + " challenged: " + str(i[1]) + " amount: " + i[2] + " in: " + i[3])
    if date.today().day == 1:
        list_challenges = dbhelper.get_all_challenges()
        year_month = str(date.today().year) + str(date.today().month - 1)
        for i in list_challenges:
            user_id_challenger, user_id_challenged = i[0], i[1]
            challenger_name = dbhelper.get_username(user_id_challenger)
            challenged_name = dbhelper.get_username(user_id_challenged)
            str_outcome = dbhelper.is_challenge_successful(i[0], i[1], year_month)
            challenge_amount = str(dbhelper.get_challenge_amount(user_id_challenger, user_id_challenged, year_month))
            if str_outcome == "success":
                bot.send_message(chat_id=user_id_challenged, text="Congratulations " + challenged_name + "!🎊 You have successfully completed the challenge to spend within a budget of $" + challenge_amount + " issued by " + challenger_name + ". We have already flaunted your achievement to " + challenger_name + " to let him/her know that YOU are the saving guru!🎉")
                bot.send_message(chat_id=user_id_challenger, text="Yo " + challenger_name + "!🤠 Remember the challenge that you issued to " + challenged_name + " to spend within a budget of $" + challenge_amount + " last month? " + challenged_name + " has successfully completed your challenge and is crowned as the saving guru!🎉 Maybe you can ask him/her for tips on how to save more and spend less?😉")
            elif str_outcome == "fail":
                bot.send_message(chat_id=user_id_challenged, text="Oh no!😣 You have failed the challenge to spend within a budget of $" + challenge_amount + " issued by " + challenger_name + ". It's okay, just manage your spendings and savings better next month! You can check out the Promotions feature to help you save a bit more while you spend! 💪") 
                bot.send_message(chat_id=user_id_challenger, text="Yo " + challenger_name + "!🤠 Remember the challenge that you issued to " + challenged_name + " to spend within a budget of $" + challenge_amount + " last month? " + "Sadly, he/she has failed the challenge.😩 Do you have any good tips to help your friend to spend lesser?")
            elif str_outcome == "monthly expenditure not keyed in":
                bot.send_message(chat_id=user_id_challenged, text="Remember the challenge to spend within a budget of $" + challenge_amount + " issued by " + challenger_name + "? Sadly, you did not track your monthly expenditure and we are unable to determine if you are up for the challenge.😢 Maybe start tracking your spendings and savings in the new month?😉") 
                bot.send_message(chat_id=user_id_challenger, text="Yo " + challenger_name + "!🤠 Remember the challenge that you issued to " + challenged_name + " to spend within a budget of $" + challenge_amount + " last month? " + "Sigh, your friend did not track his/her spendings at all so we are not sure if he/she succeeded the challenge.😢 Maybe you can urge your friend to start managing his/her finances in the new month?😉")
            dbhelper.remove_challenge(user_id_challenger, user_id_challenged, year_month)
        # test_c = dbhelper.test_all_challenges()
        # print("\nsecond for loop")
        # for i in test_c:
        #     print("challenger: " + str(i[0]) + " challenged: " + str(i[1]) + " amount: " + i[2] + " in: " + i[3])
    else:
        return

def send_daily():
    list_of_users = dbhelper.get_all_users()
    for i in list_of_users:
        if dbhelper.wants_reminder(i):
            bot.send_message(chat_id= i, text="Reminder: Have you keyed in your expenditure (if any) for today? 🤔 \nTracking your expenses and savings consistently helps you manage your finances better!")

while True:
    schedule.every().day.at("21:00").do(send_daily) 
    schedule.every().day.at("09:00").do(monthly)
    schedule.every().day.at("10:00").do(monthly_challenges)
    Thread(target=schedule_checker).start()
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        logging.error(err)
        time.sleep(5)
        print("Internet error!")
