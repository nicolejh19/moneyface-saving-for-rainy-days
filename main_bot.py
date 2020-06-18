import telebot
from telebot import types
from databasehelper import DBHelper
from datetime import datetime
import schedule
import time
from threading import Thread
from time import sleep
from _datetime import date
import logging

bot = telebot.TeleBot("TOKEN")
dbhelper = DBHelper("NAME OF DATABASE")

###################### BUTTONS ############################
main_menu_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main_menu_buttons.add(types.KeyboardButton('Manage Savings'), types.KeyboardButton('Manage Spendings'), 
                    types.KeyboardButton('Promotions'), types.KeyboardButton('Manage Debts'),
                    types.KeyboardButton('$ocialite'), types.KeyboardButton('Help'))

my_s_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
my_s_button.add(types.KeyboardButton('Update'),types.KeyboardButton('My Records'))

update_spendings_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
update_spendings_button.add(types.KeyboardButton('Monthly Budget'),types.KeyboardButton('Daily Expenditure'))

update_savings_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
update_savings_button.add(types.KeyboardButton('Monthly Savings'),types.KeyboardButton('Bonus Savings'))

records_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
records_button.add(types.KeyboardButton('Current Month'), types.KeyboardButton('History'))

promotions_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
promotions_button.add(types.KeyboardButton('Food'), types.KeyboardButton('Clothes'),
                types.KeyboardButton('Transport'),types.KeyboardButton('Daily Necessities'),
                types.KeyboardButton('Others'))

promo_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
promo_button.add(types.KeyboardButton('Food'), types.KeyboardButton('Fashion'),
                types.KeyboardButton('Transport'), types.KeyboardButton('Daily Necessities'),
                types.KeyboardButton('Entertainment'), types.KeyboardButton('Student Deals'))

debt_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
debt_button.add(types.KeyboardButton('IOU'), types.KeyboardButton('UOMe'))

iou_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
iou_button.add(types.KeyboardButton('Show Debtees'), types.KeyboardButton('Update Debtees'))

uome_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
uome_button.add(types.KeyboardButton('Show Debtors'), types.KeyboardButton('Update Debtors'))

debtee_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
debtee_button.add(types.KeyboardButton('Add Debtee'), types.KeyboardButton('Delete Debtee'))

debtor_button = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
debtor_button.add(types.KeyboardButton('Add Debtor'), types.KeyboardButton('Delete Debtor'))

socialite_button = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
socialite_button.add(types.KeyboardButton('Remind Friend'))

contact_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
contact_button.add(types.KeyboardButton(text='Share Contact', request_contact=True))

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
    dbhelper.add_user(chat_id)
    start_text= start_text= "Welcome " + username + " to Saving for Rainy Days! 😄\nWe will guide you through rainy days and bring you luck to see the god of fortune.💰\n\nOur main features include: \n1) Tracking your monthly savings and daily savings (if any) \n2) Tracking your monthly expenditure and daily spendings \n3) Updating you with the latest promotions and good deals to boost your savings\n\nTo begin your path to be in control of your wealth, type /main and we will guide you to your fortunes!\nGood luck!\nWell wishes from Team MoneyFace🤑 "
    bot.send_message(chat_id=chat_id, text= start_text, reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=['main'])
def main(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    main_text = "Hi " + username + "!\nWelcome to the main menu of Saving for Rainy Days! 😊 \n\nHere’s a quick guide to our features:\n1) To update your savings and look at your saving records, select *My Savings*. Also, don’t forget to key in your monthly savings! Any bonus money received can also be checked in. 🥳 \n\n2) Click *My Spendings* to update your daily spendings and monitor your spending history. 💸Remember to key in your monthly budget and update your daily expenditure!\n\n3) Select *Promotions* to check out the latest good deals in different categories.\n\nMonthly savings and expenditure should be keyed in at the start of each month and we will remind you to key in your daily spendings.😉\nWhat are you waiting for? Save now and control your spendings!"
    bot.send_message(chat_id=chat_id, text=main_text,reply_markup=main_menu_buttons,parse_mode="Markdown")
    bot.register_next_step_handler(message, process_next_step)

def process_next_step(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
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
        body = "You have selected “Manage Debts”.🧾\nSelect *IOU* to update/review debtees and the amount YOU owe. Select *UOMe* to update/review your debtors and the amount THEY owe you. 💶"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=debt_button, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_debts)
    elif msg == '$ocialite':
        if dbhelper.is_user_phone_number_stored(chat_id):
            body = "You have selected *$ocialite*.👯 \nSelect *Challenge Friend* to challenge your friend to spend within an amount for this month! 💪 Select *Remind Friend* to remind your friend to pay you back! 😑"
            bot.send_message(chat_id=chat_id, body=body, reply_markup=socialite_button, parse_mode="Markdown")
            bot.register_next_step_handler(message, process_socialite)
        else:
            body = "To use this feature, we will require your contact. 📞 Please be assured that the information is used solely for engagement with your friends.🙂\nClick on the 'Share Contact' button below to share your contact with us. If you do not wish to share contact, type 'exit' to go back to main menu."
            bot.send_message(chat_id=chat_id, body=body, reply_markup=contact_button)
            bot.register_next_step_handler(message, extract_contact)
    else: 
        bot.send_message(chat_id, text= "Oh dear, you just destroyed my train of thoughts.😩 Type '/main' for me to restart.", reply_markup= types.ReplyKeyboardRemove())

def process_my_savings(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    if msg == 'Update':
        text = "To input your monthly savings at the start of each month, select *Monthly Savings*.\n\nJust received some money from your generous aunt or just received your scholarship money? 😎Go to *Bonus Savings* to increase your savings! ^_^ "
        bot.send_message(chat_id=chat_id, text=text, reply_markup=update_savings_button)
        bot.register_next_step_handler(message, process_update_savings)
    elif msg == 'My Records':
        bot.send_message(chat_id=chat_id, text= "Do you want to check your current month savings or your savings history?", reply_markup=records_button)
        bot.register_next_step_handler(message, process_savings_records)
    else:
        bot.send_message(chat_id=chat_id, text="Oh dear, you just destroyed my train of thoughts.😩 Type '/main' for me to restart. ",reply_markup=types.ReplyKeyboardRemove())

def process_update_savings(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    if msg == 'Monthly Savings':
        text = "Please input your savings for this month. For example, if you want to save $888.88 this month, simply key in 888.88 😆 \n\nGod of Fortune says that the more you save, the richer you become! 🏦"
        bot.send_message(chat_id=chat_id, text=text, reply_markup= types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_monthly_savings)
    elif msg == 'Bonus Savings':
        text = "Wah feeling rich now right! Good money drop from the sky. 🥳 Key in how much more you want to save. For example, if your generous aunt gave you $88.88, just key in 88.88."
        bot.send_message(chat_id=chat_id, text=text, reply_markup= types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_bonus_savings)
    else:
        bot.send_message(chat_id=chat_id, text="Alamak now I forgot what you want to do already. 🤦Type '/main' for me to reboot ", reply_markup=types.ReplyKeyboardRemove())

def process_monthly_savings(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    if msg.isnumeric() or is_float(msg):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        flag = dbhelper.add_monthly_savings(dt, year_month, msg, chat_id, 'MONTHLY')
        if flag: 
            bot.send_message(chat_id=chat_id, text="Your savings for this month is $" + "{:.2f}".format(float(msg)) + ". 💶 Go back to /main to explore other features!")
        else:
            curr_savings = dbhelper.get_current_savings(year_month, chat_id)
            bot.send_message(chat_id=chat_id, text="Your savings for this month has already been set. In case you forgot, you have saved a total of $" + curr_savings + " this month. 💶 Check out other features at /main!")
    else:
        bot.send_message(chat_id=chat_id, text="Input your monthly savings properly leh.😠 If you want to save $888.88, just key in 888.88")
        bot.register_next_step_handler(message, process_monthly_savings)

def process_bonus_savings(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    if msg.isnumeric() or is_float(msg):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        flag = dbhelper.add_monthly_savings(dt, year_month, msg, chat_id, 'BONUS')
        bot.send_message(chat_id=chat_id, text="Your bonus savings is " + msg +". Explore other features at /main! ^_^")
    else:
        bot.send_message(chat_id=chat_id, text="Input your bonus savings properly leh. Later I forget again you have to go back to /main hor")
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
    if msg == 'Current Month':
        curr_savings = dbhelper.get_current_savings(year_month, chat_id)
        if curr_savings.isnumeric() or is_float(curr_savings):
            average_savings = dbhelper.get_average_monthly_savings(chat_id)
            symflag = is_aboveequal_average(float(curr_savings), average_savings)
            if symflag == ">":
                comparison = "\nGood job! Your savings for this month is above the average savings for the past months. God of Fortune is proud of you."
            elif symflag == "=":
                comparison = "\nYour savings for this month is the same as the average savings for the past months. Keep on saving!"
            else:
                comparison = "\nYour savings for this month is below the average savings for the past months. Try to save more okay, you never know when there will be rainy days."
            bot.send_message(chat_id=chat_id, text="Here's the statistics:\n🗓 Savings for the current month: $" + curr_savings + "\n🗓Average monthly savings: $" +  str(average_savings) + comparison, reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(chat_id=chat_id, text=curr_savings, reply_markup=types.ReplyKeyboardRemove())
    elif msg == 'History':
        total_savings = dbhelper.get_total_savings(chat_id)
        if total_savings != "0.00" and dbhelper.has_history_savings(chat_id, year_month):
            average_savings = dbhelper.get_average_monthly_savings(chat_id)
            send_text = "Here's the statistics:\n🗓 Total savings since using Saving for Rainy Days: $" + total_savings + "\n🗓Average monthly savings: $" +  str(average_savings) + "\nKeep on saving!"
        else:
            send_text = "There is no history of your savings. Keep saving and using Saving for Rainy Days to see your records next month!"
        bot.send_message(chat_id=chat_id, text=send_text, reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id=chat_id, text="My brain is not so good. Now I forgot what you want to do. Go back to /main leh :C", reply_markup=types.ReplyKeyboardRemove())

def process_my_spendings(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    if msg == 'Update':
        text = "To input your monthly budget at the start of each month, select *Monthly Budget*.\n\nJust bought your favourite bubble tea or spent on other things? 😔Go to *Daily Expenditure* to key in your spendings."
        bot.send_message(chat_id=chat_id, text= text, reply_markup=update_spendings_button)
        bot.register_next_step_handler(message, process_update)
    elif msg == 'My Records':
        text = "Do you want to check your current month expenditure or your spending history? Tracking your spendings makes you the one in control of your finances. 😎"
        bot.send_message(chat_id=chat_id, text= text, reply_markup=records_button)
        bot.register_next_step_handler(message, process_records)
    else:
        bot.send_message(chat_id=chat_id, text="Aigoo, I cannot comprehend what you want me to do. 😪 Just go back to /main please.", reply_markup=types.ReplyKeyboardRemove())   
    
def process_update(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    if msg == 'Monthly Budget':
        text = "Please input your budget for this month. For example, if you intend to set aside $300.50 for this month, just key in 300.5 😉\n\nSetting a reasonable budget is key to managing your finances. 💪"
        bot.send_message(chat_id=chat_id, text=text,reply_markup= types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_monthly_budget)
    elif msg == 'Daily Expenditure':
        bot.send_message(chat_id=chat_id, text="Select the category to input your expenditure. Always remember to spend within your budget that you've planned! 💪", reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text= "Why you anyhow type ah? 😑 Go back to /main to look for promotions lah!", reply_markup=types.ReplyKeyboardRemove())

def process_monthly_budget(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    if msg.isnumeric() or is_float(msg):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        flag = dbhelper.add_monthly_budget(year_month, msg, chat_id)
        if flag: 
            bot.send_message(chat_id=chat_id, text="Your budget for this month is $" + "{:.2f}".format(float(msg)) + ". 🤑Go to /main to check out on the good deals coming up ok!")
        else:
            curr_budget = dbhelper.get_monthly_budget(year_month, chat_id)
            bot.send_message(chat_id=chat_id, text="Your budget for this month has already been set. In case you forgot, I tell you again lah. " + curr_budget + "🤑Go to /main to check out on the good deals coming up ok!")
    else:
        bot.send_message(chat_id=chat_id, text="Alamak, testing me hor. Input your budget properly lah. 🙄 If you prepared $200.50 to spend, just key in 200.5 😌")
        bot.register_next_step_handler(message, process_monthly_budget)

def process_daily_expenditure(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
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
    else:
        bot.send_message(chat_id=chat_id, text= "Finished your input for daily expenditure? 😀 Go back to /main to look for promotions lah!", reply_markup=types.ReplyKeyboardRemove())

def process_food(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    if amount.isnumeric() or is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'FOOD', amount, chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on food today. Don't spend too much on junk food okay!", reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for food properly leh 🤨")
        bot.register_next_step_handler(message, process_food)

def process_clothes(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    if amount.isnumeric() or is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'CLOTHES', amount, chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on clothes today. Don't buy excessively okay!", reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for clothes properly leh 🤨")
        bot.register_next_step_handler(message, process_clothes)

def process_transport(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    if amount.isnumeric() or is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'TRANSPORT', amount, chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on transport today. Travel cheaply via public transport okay!", reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for transport properly leh 🤨")
        bot.register_next_step_handler(message, process_transport)

def process_necessities(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    if amount.isnumeric() or is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'NECESSITIES', amount, chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on daily necessities today. Remember to buy only what you need!",reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for daily necessities properly leh 🤨")
        bot.register_next_step_handler(message, process_necessities)

def process_others(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    amount = message.text
    if amount.isnumeric() or is_float(amount):
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        dbhelper.add_daily_exp(dt, 'OTHERS', amount, chat_id, year_month)
        bot.send_message(chat_id=chat_id, text="You spent $" + amount + " on others today. Remember to spend within your budget!", reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_daily_expenditure)
    else:
        bot.send_message(chat_id=chat_id, text="Input your budget for 'others' properly leh 🤨")
        bot.register_next_step_handler(message, process_others)

def convert_str(amt):
    try:
        res = float(amt)
        return res                    
    except ValueError as e:
        return int(amt)

def process_records(message):
    chat_id = message.from_user.id
    msg = message.text
    curr_exp = dbhelper.get_monthly_exp(chat_id, year_month)
    curr_budget = dbhelper.get_monthly_budget(year_month, chat_id)
    if msg == 'Current Month':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        curr_exp = dbhelper.get_monthly_exp(chat_id, year_month)
        curr_budget = dbhelper.get_monthly_budget(year_month, chat_id)
        if not is_float(curr_exp):
            bot.send_message(chat_id=chat_id, text="You have not recorded your expenditure for this month. Go update your expenditure leh.", reply_markup=types.ReplyKeyboardRemove())
        elif not is_float(curr_budget):
            bot.send_message(chat_id=chat_id, text="You have not set your budget for this month. Go set your budget leh.", reply_markup=types.ReplyKeyboardRemove())
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
            ### TO DO ###
            ### PIE CHART ####
            perc_budget_used = ((Decimal(curr_exp) / Decimal(curr_budget)) * 100).quantize(Decimal('1.00'))
            if perc_budget_used > 100:
                warn_msg = "❗️❗️❗️ You have exceeded your budget this month! God of Fortune is disappointed. 🥺 Try harder next month!"
            elif perc_budget_used >= 90:
                warn_msg = "❗️❗️ You have hit or exceeded 90% of your budget set for the month! 😧 Be extra careful not to exceed your budget okay!"
            elif perc_budget_used >= 70:
                warn_msg = "❗️ You have hit or exceeded 70% of your budget set for the month! 🤑 Be careful not to exceed your budget okay!"
            else:
                warn_msg = ""
                bot.send_message(chat_id=chat_id, text="Here's the statistics:\n🗓 Budget for this month: $" + curr_budget + "\n🗓 Total spending for this month: $" + curr_exp + "\n🗓 Percentage of budget used: " + str(perc_budget_used) + "%\n" + warn_msg + "\nHere is a breakdown of your spendings this month as shown in the pie chart below.\n", reply_markup=types.ReplyKeyboardRemove())
    elif msg == 'History':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        average_monthly_exp = dbhelper.get_average_monthly_exp(chat_id)
        num_months_exp = dbhelper.get_num_months_exp(chat_id)
        if num_months_exp == 0 or not is_float(average_monthly_exp):
            bot.send_message(chat_id=chat_id, text="History of your spendings not available yet. Keep on tracking and you will see it next month!", reply_markup=types.ReplyKeyboardRemove())
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
            bot.send_message(chat_id=chat_id, text="Here's the statistics:\n🗓 Average monthly expenditure: $" + average_monthly_exp + "\n🗓 Out of " + str(num_months_exp) + " months of using Saving for Rainy Days, you have exceeded your budget " + str(num_months_exceed) + " times.\n🗓 Percentage of months successfully spending within budget: " + percentage_of_months_within_budget + "%\n" + resp_msg, reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id=chat_id, text="Oopsies...Press /main to resurrect me", reply_markup=types.ReplyKeyboardRemove())

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
        bot.send_message(chat_id=chat_id, text="Finished looking for good deals? Then start keying in your spendings to keep track of them at /main! 💸", reply_markup=types.ReplyKeyboardRemove())

def process_debts(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg == 'IOU':
        body = "To review your list of debtees, select *Show Debtees*. If you want to add or delete debtee from the list, select *Update Debtees*. 💸"
        bot.send_message(chat_id=chat_id, text= body, reply_markup=iou_button,parse_mode= "Markdown")
        bot.register_next_step_handler(message, process_iou)
    elif msg == 'UOMe':
        body = "To review your list of debtors, select *Show Debtors*. If you want to add or delete debtor from the list, select *Update Debtors*. 💸"
        bot.send_message(chat_id, text=body, reply_markup=uome_button, parse_mode= "Markdown")
        bot.register_next_step_handler(message, process_uome)
    else:
        bot.send_message(chat_id=chat_id,text="Don't have any debts to deal with? Explore other features at /main!", reply_markup=types.ReplyKeyboardRemove())

def process_iou(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg == 'Show Debtees':
        all_debtees = dbhelper.get_all_debtees(chat_id)
        if not all_debtees:
            bot.send_message(chat_id=chat_id, text="Good! You don't owe anyone money. Continue to save at /main.",reply_markup=types.ReplyKeyboardRemove())
        else:
            res = "Here is a list of people you owe:\n"
            for i in all_debtees:
                res += i[0] + ": $" + i[1] + "\n"
            res += "Hurry save save save and buy only discounted items so that you can pay them back asap! Find Promotions at /main."
            bot.send_message(chat_id=chat_id, text=res,reply_markup=types.ReplyKeyboardRemove())
    elif msg == 'Update Debtees':
        bot.send_message(chat_id=chat_id, text="Do you want to add or delete debtees?",reply_markup=debtee_button)
        bot.register_next_step_handler(message, update_debtee)
    else:
        bot.send_message(chat_id=chat_id, text="No debtees to deal with? That's great! Continue to save at /main.",reply_markup=types.ReplyKeyboardRemove())

def process_uome(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg == 'Show Debtors':
        all_debtors = dbhelper.get_all_debtors(chat_id)
        if not all_debtors:
            bot.send_message(chat_id=chat_id, text="Good! No one owes you money. Continue to save at /main.",reply_markup=types.ReplyKeyboardRemove())
        else:
            res = "Here is a list of people who owe you:\n"
            for i in all_debtors:
                res += i[0] + ": $" + i[1] + "\n"
            res += "Hurry chase for your money back! The longer you wait the more they will forget. Use $socialise at /main to remind your friends if you shy."
        bot.send_message(chat_id=chat_id, text=res,reply_markup=types.ReplyKeyboardRemove())
    elif msg == 'Update Debtors':
        bot.send_message(chat_id=chat_id, text="Do you want to add or delete debtors?",reply_markup=debtor_button)
        bot.register_next_step_handler(message, update_debtor)
    else:
        bot.send_message(chat_id=chat_id, text="No debtors to deal with? That's great too! Continue to save at /main.",reply_markup=types.ReplyKeyboardRemove())

def update_debtee(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg == 'Add Debtee':
        body = "To add a debtee, please input in the following format: “[name of debtee],[amount you owed]“.\nE.g. If you owed Tan Ah Long $50, then key in Tan Ah Long,50. Do check before keying in and do not leave any spacing.🙂"
        bot.send_message(chat_id=chat_id, text=body, reply_markup= types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_debtee)
    elif msg == 'Delete Debtee':
        body = "Congratulations on paying back what you’ve owed!🥳 To delete a debtee, simply input the name of the debtee that is in your debtee list. \nE.g. If you have cleared your debts with Tan Ah Long, then simply key in Tan Ah Long."
        bot.send_message(chat_id=chat_id, text= body, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, delete_debtee)
    else:
        bot.send_message(chat_id=chat_id, text="No debtees to update? Faster pay back if you got any debtees okay! Visit /main to help you save more.", reply_markup=types.ReplyKeyboardRemove())

def add_debtee(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Press /main to explore other features at main menu.")
    else: 
        arr = msg.split(",")
        try:
            name_debtee, amt = arr[0], arr[1]
            dbhelper.add_debtee_iou(chat_id, name_debtee.upper(), amt)
            body = "You owed " + name_debtee + " $" + amt + " and it has been added to your debtee list. Remember to faster pay back okay! Go to /main to see if you got any savings to help you pay."
            bot.send_message(chat_id=chat_id, text=body)
        except IndexError:
            bot.send_message(chat_id=chat_id, text="Please follow the format for input.🙂 If you don't want to add debtee, input 'exit'.")
            bot.register_next_step_handler(message, add_debtee)

def delete_debtee(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Press /main to explore other features at main menu.")
    else: 
        if dbhelper.is_debtee_present_iou(chat_id, msg.upper()):
            dbhelper.delete_debtee_iou(chat_id, msg.upper())
            bot.send_message(chat_id=chat_id,text="You have removed " + msg + " from your debtee list. Good job! Meanwhile, explore other features at /main!")
        else:
            body = "The name you've keyed in is not in our database. Please check if you have keyed in the name of your debtee correctly or check if the person is in your debtee list and input again. If you have no debtee to delete, then input 'exit'."
            bot.send_message(chat_id=chat_id,text=body)
            bot.register_next_step_handler(message, delete_debtee)

def update_debtor(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg == 'Add Debtor':
        body = "To add a debtor, please input in the following format: “[name of debtor],[amount they owed you]“.\nE.g. If you lent Tan Ah Beng $50, then key in Tan Ah Beng,50. Do check before keying in and do not leave any spacing.🙂"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_debtor)
    elif msg == 'Delete Debtor':
        body = "Congratulations on receiving back your money!🥳 To delete a debtor, simply input the name of the debtor that is in your debtor list. \nE.g. If Tan Ah Beng paid you back, then simply key in Tan Ah Beng."
        bot.send_message(chat_id=chat_id, text=body, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, delete_debtor)
    else:
        bot.send_message(chat_id=chat_id, text="No debtors to update? If you still got any debtors, can use our $ocialite feature to remind them to pay back okay! Visit /main to explore.", reply_markup=types.ReplyKeyboardRemove())

def add_debtor(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Press /main to explore other features at main menu.")
    else: 
        arr = msg.split(",")
        try:
            name_debtor, amt = arr[0], arr[1]
            dbhelper.add_debtor_uome(chat_id, name_debtor.upper(), amt)
            body = "You lent " + name_debtor + " $" + amt + " and it has been added to your debtor list. If you shy ah, can use our $ocialite feature to remind them to pay back okay! Go to /main to check out."
            bot.send_message(chat_id=chat_id, text=body)
        except IndexError:
            bot.send_message(chat_id=chat_id, text="Please follow the format for input.🙂 If you don't want to add debtor, input 'exit'.")
            bot.register_next_step_handler(message, add_debtor)

def delete_debtor(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Press /main to explore other features at main menu.")
    else: 
        if dbhelper.is_debtor_present_uome(chat_id, msg.upper()):
            dbhelper.delete_debtor_uome(chat_id, msg.upper())
            bot.send_message(chat_id=chat_id,text="You have removed " + msg + " from your debtor list. Good job! Meanwhile, explore other features at /main!")
        else:
            body = "The name you've keyed in is not in our database. Please check if you have keyed in the name of your debtor correctly or check if the person is in your debtor list and input again. If you have no debtor to delete, then input 'exit'."
            bot.send_message(chat_id=chat_id,text=body)
            bot.register_next_step_handler(message, delete_debtor)

def extract_contact(message):
    chat_id = message.from_user.id
    try:
        contact = message.contact.phone_number
        if contact[0] != '+':
            contact = '+' + contact
        dbhelper.update_phone_number(chat_id, contact)
        body = "Great! 🥳 Select *Challenge Friend* to challenge your friend to spend within an amount for this month! 💪 Select *Remind Friend* to remind your friend to pay you back! 😑"
        bot.send_message(chat_id=chat_id, text=body, reply_markup=socialite_button)
        bot.register_next_step_handler(message, process_socialite)
    except Exception as err:
        bot.send_message(chat_id=chat_id, text="Press /main to go back to the main menu 🙂", reply_markup=types.ReplyKeyboardRemove())

def process_socialite(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    if msg == 'Remind Friend':
        body = "To remind your friend to pay you back the amount he/she owed you, please input your friend's contact number and the amount. ☎️ Please input in the following format: “+[country code][number],[amount]”. \nE.g. if your friend’s number is 91234567 and his/her country code is 65 and the amount he/she owed you is $50, then key in +6591234567,50. Do check before keying in and do not leave any spacing.🙂"
        bot.send_message(chat_id=chat_id, text= body, reply_markup = types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, remind_friend)
    else:
        bot.send_message(chat_id=chat_id, text="Don't want to interact with your friends? Explore other features at /main!", reply_markup=types.ReplyKeyboardRemove())

def remind_friend(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    if msg.lower() == 'exit':
        bot.send_message(chat_id=chat_id, text="Press /main to explore other features at main menu.")
    else:
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
                body = "Unfortunately, the contact that you keyed in is not in our database.😪 Get your friend to use 'Saving for Rainy Days' today and activate the $ocialite feature to interact with your friends!�"
                bot.send_message(chat_id=chat_id, text=body, reply_markup=socialite_button)
                bot.register_next_step_handler(message, process_socialite)
        except IndexError:
            bot.send_message(chat_id=chat_id, text="Key in the number and amount properly leh.🤨 If your friend already paid you back and no need to bug them anymore, type 'exit'.\nOtherwise, please input again in the following format: “+[country code][number],[amount]”. Do check before keying in and do not leave any spacing.🙂")
            bot.register_next_step_handler(message, remind_friend)
                
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(10)

#Monthly reminder with pie chart for spendings for that month
def monthly():
    if date.today().day == 1:
        list_of_users = dbhelper.get_all_users()
        year_month = str(date.today().year) + str(date.today().month - 1)
        for i in list_of_users:
            past_month_exp = dbhelper.get_monthly_exp(i, year_month)
            past_month_savings = dbhelper.get_current_savings(year_month, i)
            past_month_budget = dbhelper.get_monthly_budget(year_month, i)
            average_savings = dbhelper.get_average_monthly_savings(i)
            if is_float(past_month_savings):
                savings_msg = "$" + past_month_savings
            else:
                savings_msg = "No records of savings last month"
            if average_savings != 0:
                ave_savings_msg = "$" + str(average_savings)
            else:
                ave_savings_msg = "No history of savings available"
            if is_float(past_month_budget):
                budget_msg = "$" + past_month_budget
            else:
                budget_msg = "No budget set last month"
            if is_float(past_month_exp): ### GOT PAST MONTH EXPENDITURE ###
                exp_msg = "$" + past_month_exp + "\n"
                if is_float(past_month_budget):
                    if Decimal(past_month_exp) <= Decimal(past_month_budget):
                        succ_or_fail_msg = "🥳 Congrats! You successfully kept within budget last month!"
                    else:
                        succ_or_fail_msg = "😔 You did not manage to spend within budget last month. Try harder this month! 💪🏻"
                flag = dbhelper.add_monthly_exp(i, year_month)
                average_exp = dbhelper.get_average_monthly_exp(i)
                ave_exp_msg = "$" + average_exp
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
                default_msg = "It is a new month!🤗 Start planning for your monthly savings and budget. Here's a summary of your savings and spendings last month:\n🗓 Monthly savings: " + savings_msg + "\n🗓 Average monthly savings: " + ave_savings_msg + "\n🗓 Monthly budget: " + budget_msg + "\n🗓 Monthly expenditure: " + exp_msg + succ_or_fail_msg + "\n🗓 Average monthly expenditure: " + ave_exp_msg + "\n🗓 Category with highest spendings: " + spent_most
                bot.send_message(chat_id=i, text=default_msg)
                bot.send_photo(chat_id=i, photo=open('.../monthly.png' ,'rb')) #get path 
            else:
                exp_msg = "No records of expenditure last month"
                succ_or_fail_msg = ""
                cat_msg = ""
                if not is_float(average_exp):
                    ave_exp_msg = "No history of expenditure available"
                bot.send_message(chat_id=i, text=default_msg)
    else:
        return

#Daily reminder to user to key in daily spendings
def send_daily():
    list_of_users = dbhelper.get_all_users()
    for i in list_of_users:
        bot.send_message(chat_id= i, text="Reminder: Have you keyed in your expenditure (if any) for today? 🤔 \nTracking your expenses and savings consistently helps you manage your finances better!")

while True:
    schedule.every().day.at("16:04").do(send_daily) 
    schedule.every().day.at("00:00").do(monthly)
    Thread(target=schedule_checker).start()
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        logging.error(err)
        time.sleep(5)
        print("Internet error!")
