# -*- coding: utf-8 -*-
import logging
import os
import re

import MySQLdb
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
updater=Updater("BOT_TOKEN")

print "Runnig ..."



def start(bot,update):
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id,"این ربات قابلیت دانلود موزیک از سایت های 'soundcloud' و 'MusicBed' و همچنین 'Mixcloud' را دارد \nربات در حالت آزمایش  میباشد لطفا مشکلات احتمالی را به ایدی زیر منتقل کنید \n@amin_nekofar")
    bot.sendMessage(chat_id,"لینک موزیک را با این ایدی به اشتراک بگذارید \n **توجه داشته باشد که ارسال فایل های بالای  50مگابایت در تلگرام امکان پذیر نمیباشد**")


def get(bot,update):
    chat_id = update.message.chat_id
    gettext = update.message.text
    linkmusic = re.sub(r'.*\n', '', gettext)
    
    if linkmusic[:22]=="https://soundcloud.com" or linkmusic[:24]=="https://www.musicbed.com":
        web = "soundcloud"
        link = "soundscrape " + linkmusic
        download(bot,update,link,web,chat_id)
    elif linkmusic[:21]=="https://audiomack.com":
        web = "audiomack"
        link = "soundscrape " + linkmusic + "-of"
        download(bot,update,link,web,chat_id)
    elif linkmusic[:24]=="https://www.mixcloud.com":
        web = "mixcloud"
        link = "soundscrape " + linkmusic + "-of"
        download(bot,update,link,web,chat_id)
    else:
        web =  "unknown"
        bot.sendMessage(chat_id,"لینک مشکل دارد")

def download(bot,update,link,web,chat_id):
    os.popen('rm -rf *.mp3 ; rm -rf *.tmp',"r")
    user_name = update.message.chat['username']
    bot.sendMessage(chat_id,"در حال اماده سازی موزیک برای ارسال")
    print link
    os.system(link)
    chek = os.system("ls *.mp3")
    if chek == 0:
        p = os.popen('readlink -f *.mp3',"r") 
        while 1:
            line = p.readline()
            if not line: break
            bot.sendChatAction(chat_id,"UPLOAD_AUDIO")
            bot.send_audio(chat_id, audio=open(line[:-1],'rb'))
            os.popen('rm -rf *.mp3 ; rm -rf *.tmp',"r")
    elif chek == 512:
        p = os.popen('readlink -f *.wav',"r") 
        while 1:
            line = p.readline()
            if not line: break
            os.system("lame --preset insane *.wav")
            os.popen('rm -rf *.wav',"r") 
            p = os.popen('readlink -f *.mp3',"r")
       

    db = MySQLdb.connect("db_addres","db_user","db_password","db_name")
    cursor=db.cursor()
    chek = "SELECT * FROM `users` WHERE `ChatId` = %s" % (chat_id)
    try:
        cursor.execute(chek)
        if cursor.rowcount >= 1:
            send = "UPDATE `users` SET `Count`= Count + 1 WHERE `ChatId` = %s" %(chat_id)
            cursor.execute(send)
        else:
            sql = "INSERT INTO `users`(`id`, `ChatId`, `UserName`, `Web`, `Count`) VALUES (null, '%s', '%s', '%s', '1')" % (chat_id, user_name, web)
            cursor.execute(sql)
        db.commit()


    except:
        db.rollback()

    db.close()

def send(bot,update,args):
    gettext = str(args[0])
    linkmusic = re.sub(r'.*\n', '', gettext)
    link = "soundscrape " + linkmusic
    web = "soundcloud"
    db = MySQLdb.connect("localhost","root","0201243aA","socdl")
    cursor=db.cursor()
    chek = "SELECT `ChatId` FROM `users` WHERE 1"
    try:
        cursor.execute(chek)
    except:
        db.rollback()    
    count = cursor.rowcount
    listid = cursor.fetchall()
    for i in listid:
        chat_id = str(i)[1:][:-3] 
        print chat_id
        download(bot,update,link,web,chat_id)

def msg(bot,update,args):
    text = str(args[0])
    db = MySQLdb.connect("db_address","db_user","db_password","db_name")
    cursor=db.cursor()
    chek = "SELECT `ChatId` FROM `users` WHERE 1"
    try:
        cursor.execute(chek)
    except:
        db.rollback()    
    listid = cursor.fetchall()
    for i in listid:
        chat_id = str(i)[1:][:-3] 
        bot.sendMessage(chat_id,text)









updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(MessageHandler((Filters.text), get))
updater.dispatcher.add_handler(CommandHandler("send",send,pass_args= True))
updater.dispatcher.add_handler(CommandHandler("msg",msg,pass_args= True))

updater.start_polling()
updater.idle()
