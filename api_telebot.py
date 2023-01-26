import markup as markup
import re
from config import token
from mongo_db import collecsion_conn
conn=collecsion_conn('avto', 'gosnomer')
answer = collecsion_conn('avto','answer')
print(conn)

import telebot
from telebot import types

f=open('file.txt','w')
bot=telebot.TeleBot(token)

name=''
nubmbe_avto=''
sms=''
number=''
user_id=''
@bot.message_handler(commands=['start'])
def button_message(message):
    otvet = types.ReplyKeyboardMarkup(row_width=2)

    button1 = types.KeyboardButton(" Регистрация")
    button2 = types.KeyboardButton(" Написать владельцу авто")
    button3 = types.KeyboardButton(" Ответить на сообщение")

    otvet.add(button1, button2, button3)
    bot.send_message(message.chat.id,'Выбери действие', reply_markup=otvet)
@bot.message_handler(content_types=['text'])
def catalogchk(message):

    if message.text=='Написать владельцу авто':
        bot.send_message(message.from_user.id, 'Введите номер авто, чтобы отправить ему сообщение')
        bot.register_next_step_handler(message, send_message_avto)
    elif   message.text=='Регистрация':
        bot.send_message(message.from_user.id, 'Введите номер Вашего авто')
        bot.register_next_step_handler(message, conf_registr)


def conf_registr(message):
    global number
    number= message.text

    number=str(number).replace(' ','').upper()

    match = re.findall(r'[а-яА-Я]\d{3}[а-яА-Я][а-яА-Я]\d{3}', number)
    match2 = re.findall(r'[а-яА-Я]\d{3}[а-яА-Я][а-яА-Я]\d{2}', number)
    print(len(match2)+len(match))
    print(len(match))
    print(len(match2))
    if 1<=(len(match)+len(match2)):
        confirm = types.InlineKeyboardMarkup(row_width=2)
        but1 = types.InlineKeyboardButton(" Yes", callback_data='registr')
        confirm.add(but1)

        bot.send_message(message.from_user.id, f'Зарегистрировать на вас номер {number}', reply_markup=confirm)

    else:
        bot.send_message(message.from_user.id, 'Номер введен неверно, повторите регистрацию')



def send_message_avto(message):
    global nubmbe_avto
    global user_id
    n=0
    global number
    number = message.text

    number = str(number).replace(' ', '').upper()
    for x in conn.find({'gos_nome': number}).limit(1):
        print('Номер найден',x)
        user_id=x['user_id']
        print(user_id)

        bot.send_message(message.from_user.id, f'Ввседите сообщение для владельца авто {number}')

        n=1
    if n==0:
        bot.send_message(message.from_user.id, f'Номер {nubmbe_avto} не зарегистрирован')
    elif n==1:
        bot.register_next_step_handler(message, confirmation)


def confirmation(message):# подтверждение
    global sms
    global nubmbe_avto
    sms = message.text

    confirm =types.InlineKeyboardMarkup(row_width=2)
    but1=types.InlineKeyboardButton(" Yes", callback_data='yes')
    confirm.add(but1)
    bot.send_message(message.from_user.id, f' Отправляю сообщение для пользователя {nubmbe_avto} {sms}', reply_markup=confirm)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
   global user_id
   try:
       if call.data == "yes":
           bot.send_message(call.message.chat.id, "Сообщение отправлено пользователю")
           print('user_id', user_id)
           answ = types.InlineKeyboardMarkup(row_width=2)
           but1 = types.InlineKeyboardButton("Ответить на сообщение", callback_data='answer')
           answ.add(but1)
           bot.send_message(user_id,f'Вам отправлено сообщение {sms}', reply_markup=answ)


           answer.insert_one({'from_user':call.message.chat.id, 'user_id':user_id, 'sms':sms})

       elif call.data == 'registr':
           bot.send_message(call.message.chat.id, 'Номер зарегистрирован')
           conn.insert_one({'user_id':call.message.chat.id, 'gos_nome':number})

           for x in (conn.find()):
               print(x)

   except Exception as e:
       print(repr(e))


   if call.data=='answer':
       print('hi,hi')
       print(sms, call.message.chat.id)
       print(call.message)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline2(call):
    print(call.data)
    if call.data == 'anwer':

        print('hello_world')














bot.infinity_polling()
