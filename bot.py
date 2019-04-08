import logging
import constants, base_w
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Contact, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
updater = Updater(token=constants.token)
dispatcher = updater.dispatcher

add = ret = False
add_money = 0

def start(bot, update):
    message = update.message
    if message.chat.id in constants.admins:
        bottons = [['Прибавить 👌 даме']]
        if message.chat.id in constants.black_jack:
            bottons[0].append('Снять баллы')
        elif message.chat.id in constants.ouct:
            bottons = [['Снять баллы', 'Посмотреть статистику']]
        keyboard = ReplyKeyboardMarkup(bottons, resize_keyboard = True)
        bot.send_message(message.chat.id,'Приветствую тебя, покорителя женских половых и не половых органов', reply_markup=keyboard)
    else:
        bottons = [[InlineKeyboardButton('Посмотреть баллы на своем кошельке', callback_data='1')]]
        keyboard = InlineKeyboardMarkup(bottons)
        if message.chat.id not in base_w.id():
            base_w.init(message.chat.id, message.chat.first_name)
            bot.send_message(message.chat.id, text=constants.hello_text, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Чем могу помочь?', reply_markup=keyboard)

def answer_questions(bot, update):
    message = update.message
    global add, add_money, ret
    if message.chat.id in constants.admins:
        if message.text == 'Прибавить 👌 даме' and (message.chat.id not in constants.black_jack or message.chat.id not in constants.ouct):
            bot.send_message(message.chat.id, 'Напишите кол-во очков, которые хотите прибавить')
            add = True
        elif add == True:
            add = False
            add_money = int(message.text)
            bottons = []
            names = base_w.names()
            for i in names:
                botton = [InlineKeyboardButton(i, callback_data=i+'$$$give')]
                bottons.append(botton)
            reply_markup = InlineKeyboardMarkup(bottons)
            bot.send_message(message.chat.id, 'Выберите имя девочки', reply_markup=reply_markup)
        elif message.chat.id in constants.black_jack or message.chat.id in constants.ouct:
            if message.text == 'Снять баллы':
                bot.send_message(message.chat.id, 'Напишите, на сколько вы хотите ограбить девушку!?')
                ret = True
            elif ret == True:
                ret = False
                add_money = int(message.text)
                bottons = []
                names = base_w.names()
                for i in names:
                    botton = [InlineKeyboardButton(i, callback_data=i+'$$$stole')]
                    bottons.append(botton)
                reply_markup = InlineKeyboardMarkup(bottons)
                bot.send_message(message.chat.id, 'Выберите имя девочки', reply_markup=reply_markup)
            elif message.text == 'Посмотреть статистику' and message.chat.id in constants.ouct:
                bot.send_message(message.chat.id, str(base_w.stat_()))
    else:
        for i in constants.admins:
            try:
                bot.send_message(i, message.text + '\n id: '+ str(message.chat.id) +
                                 '\n first name: '+ str(message.chat.first_name))
            except:
                pass



def button(bot,update):
    query = update.callback_query
    try:
        if str(query.data) == '1':
            bottons = [[InlineKeyboardButton('Обновить', callback_data='1')]]
            keyboard = InlineKeyboardMarkup(bottons)
            bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id , text='Текущий баланс: '+base_w.money(query.message.chat.id), reply_markup=keyboard)
        elif str(query.data).split('$$$')[1] == 'give':
            base_w.add(str(query.data).split('$$$')[0], add_money)
            bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id, text='Деньга успешно добавлена')
        elif str(query.data).split('$$$')[1] == 'stole':
            base_w.stole(str(query.data).split('$$$')[0], add_money)
            bot.edit_message_text(message_id=query.message.message_id, chat_id=query.message.chat.id,
                                  text='Вот какашка, отобрал последние деньги у бабушки')
    except:
        pass


start_handler = CommandHandler('start', start)
answer_handler = MessageHandler(Filters.all, answer_questions)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(answer_handler)
dispatcher.add_handler(CallbackQueryHandler(button))
updater.start_polling(timeout=5, clean=True )