import telebot
from telebot import types
import redis
bot = telebot.TeleBot("5963311354:AAGQlGantjnUrkJf3mUCAuOUhxYFoqWfaeE")
total_sum = 0
cache = redis.Redis(host='redis')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Начать", callback_data='start')
    markup.add(button1)
    bot.send_message(message.chat.id, "Привет! Я бот для подсчета скидок?.", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def calculate_total(message):
    global total_sum
    if message.text.isnumeric():
        with open('numbers.txt', 'a') as f:
            f.write(message.text + '\n')
            total_sum += int(message.text)
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Ввести еще число", callback_data='input')
            button2 = types.InlineKeyboardButton("Общая сумма", callback_data='total')
            button3 = types.InlineKeyboardButton("Итог", callback_data='discount')
            markup.add(button1, button2, button3)
            cache.set(name='total_sum', value=total_sum)
            bot.send_message(message.chat.id, "Общая сумма: " + str(total_sum), reply_markup=markup)
    elif message.text == "stop":
        bot.send_message(message.chat.id, "Ввод закончен. Общая сумма: " + str(total_sum))
    elif message.text == "discount":
        discount = total_sum * 0.6
        bot.send_message(message.chat.id, "-60% составляет: " + str(discount))
    elif message.text == "total":
        bot.send_message(message.chat.id, "Общая сумма: " + str(total_sum))
    else:
        bot.send_message(message.chat.id, "Я не понимаю, пожалуйста, введите число или команду.")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'start':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Напиши мне число и я добавлю его к общей сумме.')
    elif call.data == 'input':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите число')
    elif call.data == 'total':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Общая сумма: {total_sum}')
    elif call.data == 'discount':
        discount = total_sum * 0.4
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'-60% составляет: {discount}')
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Неизвестная команда')

bot.polling()