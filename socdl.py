# -*- coding: utf-8 -*-
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import logging
import os
import re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
updater=Updater("BOT-TOKEN")

print "Running..."



def start(bot,update):
    bot.sendMessage(update.message.chat_id,"این ربات قابلیت دانلود موزیک از سایت های 'soundcloud' و 'MusicBed' و همچنین 'Mixcloud' را دارد")
    bot.sendMessage(update.message.chat_id,"لینک موزیک رو برام به اشتراک بزار")


def get(bot,update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id," در حال دریافت فایل")
    gettext = update.message.text
    linkmusic = re.sub(r'.*\n', '', gettext)
    link = "soundscrape " + linkmusic
    os.system(link)
    p = os.popen('readlink -f *.mp3',"r")
    while 1:
        line = p.readline()
        if not line: break
        bot.sendMessage(chat_id,"در حال ارسال فایل")
        bot.send_audio(chat_id, audio=open(line[:-1],'rb'))
        os.popen('rm -rf *.mp3 ; rm -rf *.tmp',"r")

updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(MessageHandler((Filters.text), get))


updater.start_polling()
updater.idle()
updater.stop()

