from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = "8130663773:AAHTHUHSdgjijnUCGwvGfgpkN0A7xgcu4aY"

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=2)
    item_button1 = KeyboardButton("Вклад")
    item_button2 = KeyboardButton("Кредит")
    markup.add(item_button1)
    markup.add(item_button2)
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Вклад')
def send_deposit(message):
    bot.send_message(message.chat.id, "Начальный вклад")
    bot.register_next_step_handler(message, ask_years)
@bot.message_handler(func=lambda message: message.text == 'Кредит')
def send_credit(message):
    bot.send_message(message.chat.id, "Сколько хотите взять денег?")
    bot.register_next_step_handler(message, ask_percent)


def ask_years(message):
    try:
        initial_deposit = float(message.text)
        bot.send_message(message.chat.id, "Введите количество лет:")
        bot.register_next_step_handler(message, ask_interest_rate, initial_deposit)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число для вклада.")
        bot.register_next_step_handler(message, ask_years)
def ask_interest_rate(message, initial_deposit):
    try:
        years = int(message.text)
        bot.send_message(message.chat.id, "Введите процентную ставку:")
        bot.register_next_step_handler(message, calculate_final_amount, initial_deposit, years)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите целое число для количества лет.")
        bot.register_next_step_handler(message, ask_interest_rate, initial_deposit)

def calculate_final_amount(message, initial_deposit, years):
    try:
        interest_rate = float(message.text)
        final_amount = initial_deposit * (1 + interest_rate / 100 * years)
        bot.send_message(message.chat.id, f"Итоговая сумма вклада через {years} лет: {final_amount:.2f}")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число для процентной ставки.")
        bot.register_next_step_handler(message, calculate_final_amount, initial_deposit, years)

def ask_percent(message):
    try:
        money = float(message.text)
        bot.send_message(message.chat.id, "Под какой процент вам их дают?")
        bot.register_next_step_handler(message, ask_credit_years, money)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, ask_percent)

def ask_credit_years(message, money):
    try:
        percent = float(message.text)
        bot.send_message(message.chat.id, "На сколько лет берете?")
        bot.register_next_step_handler(message, calculate_final_credit, money, percent)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, ask_credit_years, money)

def calculate_final_credit(message, money, percent):
    try:
        years = int(message.text)
        percent = percent / 100
        month_pay = (money * percent * (1 + percent) ** years) / (12 * ((1 + percent) ** years - 1))

        summa = month_pay * years * 12

        month_pay = round(month_pay, 2)
        summa = round(summa, 2)
        bot.send_message(message.chat.id, f"{month_pay=} {summa=}")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
        bot.register_next_step_handler(message, calculate_final_credit, money, years)




bot.infinity_polling()
