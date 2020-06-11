import telebot
from telebot import types
import json
from databasehelper import DBHelper
import schedule
import time
from datetime import datetime
from threading import Thread
from time import sleep
from _datetime import date

bot = telebot.TeleBot("TOKEN")
dbhelper = DBHelper("NAME OF DATABASE")

#Keyboard buttons
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

#Prompts main menu buttons: 'My Spendings', 'Promotions', 'My Savings'
@bot.message_handler(commands=['main'])
def main(message):
    chat_id = message.from_user.id
    username = message.from_user.first_name
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    main_text = "Hi " + username + "!\nWelcome to the main menu of Saving for Rainy Days! 😊 \n\nHere’s a quick guide to our features:\n1) To update your savings and look at your saving records, select *My Savings*. Also, don’t forget to key in your monthly savings! Any bonus money received can also be checked in. 🥳 \n\n2) Click *My Spendings* to update your daily spendings and monitor your spending history. 💸Remember to key in your monthly budget and update your daily expenditure!\n\n3) Select *Promotions* to check out the latest good deals in different categories.\n\nMonthly savings and expenditure should be keyed in at the start of each month and we will remind you to key in your daily spendings.😉\nWhat are you waiting for? Save now and control your spendings!"
    bot.send_message(chat_id=chat_id, text=main_text,reply_markup=main_menu_buttons,parse_mode="Markdown")
    bot.register_next_step_handler(message, process_next_step)

#Handles the main menu buttons: 'My Spendings', 'Promotions', 'My Savings'
def process_next_step(message):
    chat_id = message.from_user.id
    msg = message.text
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    if msg == 'My Savings':
        body = "You have selected *My Savings*. 💰 \n\nTo input your monthly savings or bonus money received, select *Update*.💵\n\nTo track your current month savings and savings history, select *My Records*.🏦"
        bot.send_message(chat_id=chat_id, text= body,reply_markup= my_s_button,parse_mode="Markdown")
        bot.register_next_step_handler(message, process_my_savings)
    elif msg == 'My Spendings':
        body = "You have selected *My Spendings*. 💸\n\nSelect *Update* to input your monthly budget or daily expenditure.💵\n\nSelect *My Records* to track your current month expenditure and spending history. 🏦"
        bot.send_message(chat_id=chat_id, text= body,reply_markup= my_s_button, parse_mode="Markdown")
        bot.register_next_step_handler(message, process_my_spendings)
    elif msg == 'Promotions':
        bot.send_message(chat_id=chat_id, text= "Choose which category you want to get good deals from! 🤗", reply_markup=promotions_button)
        bot.register_next_step_handler(message, process_promotions)
    else: 
        bot.send_message(chat_id, text= "Oh dear, you just destroyed my train of thoughts.😩 Type '/main' for me to restart.", reply_markup= types.ReplyKeyboardRemove())

#Handles 'My Savings' buttons: 'Update' and 'My Records'
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

#Handles 'Update' button in 'My Savings'
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

def process_savings_records(message):
    chat_id = message.from_user.id
    msg = message.text
    unix_date = int(message.date)
    dt = datetime.utcfromtimestamp(unix_date)
    year_month = str(dt.year) + str(dt.month)
    if msg == 'Current Month':
        curr_savings = dbhelper.get_current_savings(year_month, chat_id)
        if curr_savings.isnumeric() or is_float(curr_savings):
            bot.send_message(chat_id=chat_id, text="You have saved $" + curr_savings + " this month. Tell you something, go /main to check out promotions and save somemore okay.", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(chat_id=chat_id, text=curr_savings, reply_markup=types.ReplyKeyboardRemove())
    elif msg == 'History':
        total_savings = dbhelper.get_total_savings(chat_id)
        bot.send_message(chat_id=chat_id, text=total_savings, reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id=chat_id, text="My brain is not so good. Now I forgot what you want to do. Go back to /main leh :C", reply_markup=types.ReplyKeyboardRemove())

#Process 'My Spendings' button: buttons include 'Update', 'My Records' and 'Back'
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
    
#Process 'Update' button: buttons include 'Monthly Budget', 'Daily Expenditure' and 'Back'
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

#Process 'Monthly Budget' button
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

#Process 'Daily Expenditure' button
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

#Process food button
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

#Process clothes button
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

#Process transport button
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

#Process necessities button
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

#Process others button
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

#Process 'Records' button
def process_records(message):
    chat_id = message.from_user.id
    msg = message.text
    curr_exp = dbhelper.get_monthly_exp(chat_id, year_month)
    curr_budget = dbhelper.get_monthly_budget(year_month, chat_id)
    if msg == 'Current Month':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        #TO-DO 
        #PIE CHART 
        curr_food_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'FOOD')
        curr_clothes_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'CLOTHES')
        curr_transport_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'TRANSPORT')
        curr_necc_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'NECESSITIES')
        curr_others_exp = dbhelper.get_monthly_category_exp(chat_id, year_month, 'OTHERS')
        if curr_exp.isnumeric() or is_float(curr_exp): 
            bot.send_message(chat_id=chat_id, text="You have spent $" + curr_exp +  " so far in this month\n" + curr_budget + "\nGo back to /main to check out good promotions okay! Don't say I never say ah!", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(chat_id=chat_id, text=curr_exp, reply_markup=types.ReplyKeyboardRemove())
    elif msg == 'History':
        unix_date = int(message.date)
        dt = datetime.utcfromtimestamp(unix_date)
        year_month = str(dt.year) + str(dt.month)
        average_monthly_exp = dbhelper.get_average_monthly_exp(chat_id)
        percentage_of_months_within_budget = dbhelper.get_percentage_within_budget(chat_id)
        if not average_monthly_exp.isnumeric() or not is_float(average_monthly_exp):
            bot.send_message(chat_id=chat_id, text="History of your spendings not available. Keep on tracking and you will see it next month!", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(chat_id=chat_id, text="Your average monthly expenditure is $" + average_monthly_exp + + " since you started using Saving for Rainy Days. You have kept within budget " + percentage_of_months_within_budget + "% of the time" + "\nPress /main to continue your tracking!", reply_markup=types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id=chat_id, text="Oopsies...Press /main to resurrect me", reply_markup=types.ReplyKeyboardRemove())

#Process 'Promotions' button: buttons include 'Food', 'Clothes', 'Transport', 'Daily Necessities', 'Others' and 'Back'
def process_promotions(message):
    chat_id = message.from_user.id
    bot.send_chat_action(chat_id=chat_id, action="Typing")
    msg = message.text
    if msg == 'Food':
        #direct to food channel
        #TO-DO
        bot.send_message(chat_id=chat_id, text= "Eat cheaply! t.me/kiasufoodies")
        bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Clothes':
        #direct to clothes channel
        #TO-DO
        bot.send_message(chat_id=chat_id, text= "Buy cheap and nice clothes!")
        bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Transport':
        #direct to transport channel
        #TO-DO
         bot.send_message(chat_id=chat_id, text= "Travel cheaply!")
         bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Daily Necessities':
        #direct to transport channel
        #TO-DO
         bot.send_message(chat_id=chat_id, text= "Sheng Shiong cheaper than NTUC hor!")
         bot.register_next_step_handler(message, process_promotions)
    elif msg == 'Others':
        bot.send_message(chat_id=chat_id, text= "Other stuff")
        bot.register_next_step_handler(message, process_promotions)
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
        ##SEND THE LIST OF DEBTEES TO USER THAT'S ALL
        #BACKEND PLEASE
        body = "Yo to do"
    elif msg == 'Update Debtees':
        bot.send_message(chat_id=chat_id, text="Do you want to add or delete debtees?",reply_markup=debtee_button)
        bot.register_next_step_handler(message, update_debtee)
    else:
        bot.send_message(chat_id=chat_id, text="No debtees to deal with? That's great! Continue to save at /main.",reply_markup=types.ReplyKeyboardRemove())

def process_uome(message):
    chat_id = message.from_user.id
    msg = message.text
    if msg == 'Show Debtors':
        ##SEND THE LIST OF DEBTORS TO USER THAT'S ALL
        #BACKEND PLEASE
        body = "Yo to do"
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
            #arr[0] is name of debtee, arr[1] is amount owed
            #add in database 
            # TODO process
            body = "You owed " + arr[0] + " $" + arr[1] + " and it has been added to your debtee list. Remember to faster pay back okay! Go to /main to see if you got any savings to help you pay."
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
        if nameisindatabase:
            #TODO delete from database
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
            #arr[0] is name of debtor, arr[1] is amount owed
            #add in database 
            # TODO process
            body = "You lent " + arr[0] + " $" + arr[1] + " and it has been added to your debtor list. If you shy ah, can use our $ocialite feature to remind them to pay back okay! Go to /main to check out."
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
        if nameisindatabase:
            #TODO delete from database
            bot.send_message(chat_id=chat_id,text="You have removed " + msg + " from your debtor list. Good job! Meanwhile, explore other features at /main!")
        else:
            body = "The name you've keyed in is not in our database. Please check if you have keyed in the name of your debtor correctly or check if the person is in your debtor list and input again. If you have no debtor to delete, then input 'exit'."
            bot.send_message(chat_id=chat_id,text=body)
            bot.register_next_step_handler(message, delete_debtor)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(10)

#monthly reminder + process monthly shit
#library does not support monthly check so we do with dates
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
                transport = (curr_transport_exp/ total_spending) * 100
                necc = (curr_necc_exp/ total_spending) * 100
                others = (curr_others_exp / total_spending) * 100ast_month_exp = dbhelper.get_monthly_exp(i, year_month)
                ### TO DO ###
                ### PIE CHART ###
                default_msg = "It is a new month!🤗 Start planning for your monthly savings and budget. Here's a summary of your savings and spendings last month:\n🗓 Monthly savings: " + savings_msg + "\n🗓 Average monthly savings: " + ave_savings_msg + "\n🗓 Monthly budget: " + budget_msg + "\n🗓 Monthly expenditure: " + exp_msg + succ_or_fail_msg + "\n🗓 Average monthly expenditure: " + ave_exp_msg 
                bot.send_message(chat_id=i, text=default_msg)
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
    schedule.every().day.at("21:00").do(send_daily)
    schedule.every().day.at("00:00").do(monthly)
    Thread(target=schedule_checker).start()
    bot.polling(none_stop=True)
