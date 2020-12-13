#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
from datetime import date
from genpie import chart
from databasehelper import DBHelper

TOKEN = "" #fill in
bot = telebot.TeleBot(token=TOKEN)

dbhelper = DBHelper("splash.db", False)

def is_float(amt):
    try:
        temp = float(amt)
        return float(amt) >= 0
    except ValueError as e:
        return False

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
                    try:
                        bot.send_message(chat_id=i, text=default_msg)
                        bot.send_photo(chat_id=i, photo=open('/home/teammoneyface/monthly.png' ,'rb'))
                    except:
                        continue
                else:
                    try:
                        bot.send_message(chat_id=i, text=default_msg)
                    except:
                        continue
    else:
        return

def monthly_challenges():
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
                try:
                    bot.send_message(chat_id=user_id_challenged, text="Congratulations " + challenged_name + "!🎊 You have successfully completed the challenge to spend within a budget of $" + challenge_amount + " issued by " + challenger_name + ". We have already flaunted your achievement to " + challenger_name + " to let him/her know that YOU are the saving guru!🎉")
                except:
                    continue
                try:
                    bot.send_message(chat_id=user_id_challenger, text="Yo " + challenger_name + "!🤠 Remember the challenge that you issued to " + challenged_name + " to spend within a budget of $" + challenge_amount + " last month? " + challenged_name + " has successfully completed your challenge and is crowned as the saving guru!🎉 Maybe you can ask him/her for tips on how to save more and spend less?😉")
                except:
                    continue
            elif str_outcome == "fail":
                try:
                    bot.send_message(chat_id=user_id_challenged, text="Oh no!😣 You have failed the challenge to spend within a budget of $" + challenge_amount + " issued by " + challenger_name + ". It's okay, just manage your spendings and savings better next month! You can check out the Promotions feature to help you save a bit more while you spend! 💪")
                except:
                    continue
                try:
                    bot.send_message(chat_id=user_id_challenger, text="Yo " + challenger_name + "!🤠 Remember the challenge that you issued to " + challenged_name + " to spend within a budget of $" + challenge_amount + " last month? " + "Sadly, he/she has failed the challenge.😩 Do you have any good tips to help your friend to spend lesser?")
                except:
                    continue
            elif str_outcome == "monthly expenditure not keyed in":
                try:
                    bot.send_message(chat_id=user_id_challenged, text="Remember the challenge to spend within a budget of $" + challenge_amount + " issued by " + challenger_name + "? Sadly, you did not track your monthly expenditure and we are unable to determine if you are up for the challenge.😢 Maybe start tracking your spendings and savings in the new month?😉")
                except:
                    continue
                try:
                    bot.send_message(chat_id=user_id_challenger, text="Yo " + challenger_name + "!🤠 Remember the challenge that you issued to " + challenged_name + " to spend within a budget of $" + challenge_amount + " last month? " + "Sigh, your friend did not track his/her spendings at all so we are not sure if he/she succeeded the challenge.😢 Maybe you can urge your friend to start managing his/her finances in the new month?😉")
                except:
                    continue
            dbhelper.remove_challenge(user_id_challenger, user_id_challenged, year_month)
    else:
        return

#Daily reminder to user to key in daily spendings
def send_daily():
    list_of_users = dbhelper.get_all_users()
    for i in list_of_users:
        if dbhelper.wants_reminder(i):
            try:
                bot.send_message(chat_id= i, text="Reminder: Have you keyed in your expenditure (if any) today? 🤔 \nTracking your expenses and savings consistently helps you manage your finances better!")
            except:
                continue

send_daily()
monthly()
monthly_challenges()
