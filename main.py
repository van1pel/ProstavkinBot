from telegram.ext import Updater, CommandHandler
from datetime import datetime as dt
from yfinance import Ticker
from forismatic import *
from PIL import Image, ImageDraw, ImageFont
import textwrap
from dotenv import dotenv_values


config = dotenv_values("conf.env")
bot_token = config['bot_token']  #prostavushka_bot
chat_id = config['bot_token']  #chat_id Amsterdam

updater = Updater(token=bot_token, use_context=True)  #запуск экземпляра бота

dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm ProstavushkaBot, supported commands:"
                                                                    "/dima - Time since @usebooz started his project")
def dima(update, context):
    start = dt.fromtimestamp(1615969080)
    end = dt.now()
    elapsed=end-start
    context.bot.send_message(chat_id=update.effective_chat.id, text="Time since @usebooz started his project: %02d days %02d hours %02d minutes %02d seconds" % (elapsed.days, elapsed.seconds // 3600, elapsed.seconds // 60 % 60, elapsed.seconds % 60))

def mail(update, context):
    try:
        mail_info =Ticker("MAIL.ME").info
        bid = float(mail_info["regularMarketPrice"])
        regularMarketPreviousClose = float(mail_info["regularMarketPreviousClose"])
        if bid != 0:
            change = regularMarketPreviousClose/bid
            message = "Mail.ru price: %02d ₽\nregularMarketPreviousClose: %02d ₽\n" % (bid, regularMarketPreviousClose)
            percent = ((bid - regularMarketPreviousClose) / regularMarketPreviousClose) * 100
            if percent > 0:
                message += "upwards trend 📈 +%.2f %%"  % percent
            else:
                message += "downwards trend 📉 %.2f %%"  % percent
        else:
            bid = regularMarketPreviousClose
            message = "Рынок закрыт\nЦена закрытия: " + f"{abs(int(bid)):,}" + '₽'
        # Считаем прибыль
        data = {
        'roman': {'name': 'Роман', 'stock_num': 205, 'avg_price': 1851},
        'ivan': {'name': 'Вано', 'stock_num': 95, 'avg_price': 1996},
        'nikolay': {'name': 'Пакетя', 'stock_num': 25, 'avg_price': 1890},
        'serega': {'name': 'Красавчик', 'stock_num': 28, 'avg_price': 2036},
        'brat_koli': {'name': 'Брат Коли', 'stock_num': 40, 'avg_price': 1944}
        }

        balance = 0
        overall_mail_holdings = 0

        message += '\n-'
        for key in data:
            direction_pic = '🐠'
            direction_text = ' всрал '
            if data[key]['avg_price'] < bid:
                direction_pic = '🦈'
                direction_text = ' поднял '
            income = data[key]['stock_num'] * bid - data[key]['stock_num'] * data[key]['avg_price']
            message += '\n' + direction_pic + ' ' + data[key]['name'] + direction_text + f"{abs(int(income)):,}" + '₽'
            # Статистика
            balance += income
            overall_mail_holdings += data[key]['stock_num'] * bid

        direction_stat = ' всрато '
        if balance > 0:
            direction_stat = ' поднято '
        message += '\n-\n' + '💰 Общими усилиями' + direction_stat + f"{abs(int(balance)):,}" + '₽\n💵 По текущему курсу инвестировано ' + f"{int(overall_mail_holdings):,}" + '₽'
        
        # Выводим результат
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Stock market is not available")

def quote(update, context):
    f = forismatic.ForismaticPy()
    author = ''
    if f.get_Quote('ru')[1]:
        author = '\n- ' + f.get_Quote('ru')[1]
    message = '🔮 ' + f.get_Quote('ru')[0] + author
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

path = '/home/ubuntu/prostavushka_bot/kolya.png'
path_tmp = '/home/ubuntu/prostavushka_bot/kolya_tmp.png'
wrapper = textwrap.TextWrapper(width=35)

def kolya_wisdom (update, context):
    f = forismatic.ForismaticPy()
    author = ''
    if f.get_Quote('ru')[1]:
        author = '\n\n                       - ' + f.get_Quote('ru')[1]
    message = wrapper.fill(text=f.get_Quote('ru')[0]) + author
    font_size = 14 - int(len(message)/50);
    unicode_font = ImageFont.truetype("/home/ubuntu/prostavushka_bot/DejaVuSans.ttf", font_size)
    im = Image.open(path)
    draw_text = ImageDraw.Draw(im)
    draw_text.text(
        (60,45),
        message,
        font=unicode_font,
        fill=('#1C0606')
        )
    im.save(path_tmp)
    context.bot.send_photo(chat_id, photo=open(path_tmp, 'rb'))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
dima_handler = CommandHandler('dima', dima)
dispatcher.add_handler(dima_handler)
dima_handler = CommandHandler('mail', mail)
dispatcher.add_handler(dima_handler)
quote_handler = CommandHandler('quote', quote)
dispatcher.add_handler(quote_handler)
kolya_wisdom_handler = CommandHandler('kolya_wisdom', kolya_wisdom)
dispatcher.add_handler(kolya_wisdom_handler)

updater.start_polling()
