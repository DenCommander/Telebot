import telebot
import random
import requests
import os
import shutil

telebot.apihelper.proxy = {'https': 'socks5://telegram:telegram@qcpfo.tgproxy.me:1080'}
bot = telebot.TeleBot("692690848:AAH9uiZBg-VgQw-ctDhsjVwbU5gHn_-XNIc")
path=r'D:\temp'+'\\'



def GetUDir(message):
	return path + str(message.from_user.id) + '\\'



def FindSubString(strText, strSubString, Offset=None):
    try:
        Start = strText.find(strSubString)
        if Start == -1:
            return -1 # Not Found
        else:
            if Offset == None:
                Result = strText[Start+len(strSubString):]
            elif Offset == 0:
                return Start
            else:
                AfterSubString = Start+len(strSubString)
                Result = strText[AfterSubString:AfterSubString + int(Offset)]
            return Result
    except:
        return -1
def ensure_dir(file_path):
	directory = os.path.dirname(file_path)
	print(file_path)
	if not os.path.exists(directory):
		os.makedirs(directory)



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Йоу")



@bot.message_handler(commands=['startcollect'])
def startcollect(message):
	bot.send_message(message.chat.id, "Выберите стикеры для коллекции")

	UserDirectory =GetUDir(message)
	if os.path.exists(UserDirectory):
		shutil.rmtree(UserDirectory, ignore_errors=False, onerror=None)
	os.makedirs(UserDirectory)



@bot.message_handler(commands=['endcollect'])
def endcollect(message):
	bot.send_message(message.chat.id, "Коллекция создана")

	UserDirectory =GetUDir(message)
	#здесь надо запаковать все файлы из директории и отправить пользователю, но похоже не успею
	if os.path.exists(UserDirectory):
		shutil.rmtree(UserDirectory, ignore_errors=False, onerror=None)



@bot.message_handler(func=lambda message: True, content_types=['sticker'])
def default_command(message):
	UserDirectory = GetUDir(message)
	if os.path.exists(UserDirectory):
		#bot.send_message(message.chat.id, bot.get_file(message.sticker.file_id).file_path)
		#bot.send_message(message.chat.id, message.sticker.file_id)
		FileName = FindSubString(bot.get_file(message.sticker.file_id).file_path, "/")
		#bot.send_message(message.chat.id, FileName)
		#bot.send_message(message.chat.id, telebot.apihelper.FILE_URL.format(bot.token, bot.get_file(message.sticker.file_id).file_path))
		#bot.send_message(message.chat.id, bot.get_file_url(message.sticker.file_id))
		#bot.download_file(bot.get_file(message.sticker.file_id).file_path)
		r = requests.get(telebot.apihelper.FILE_URL.format(bot.token, bot.get_file(message.sticker.file_id).file_path), proxies=telebot.apihelper.proxy)
		if r.status_code == 200:
			#bot.send_message(message.chat.id, "ok")
			#directory=path + str(message.from_user.id)+'\\'
			#ensure_dir(directory)
			file_path =  UserDirectory + FileName
			f = open(file_path, "wb")
			f.write(r.content)  # записываем содержимое в файл; как видите - content запроса
			f.close()
	else:
		bot.send_sticker(message.chat.id, message.sticker.file_id)



@bot.message_handler(func=lambda message: ("подтверди" in message.text.lower() or "согласен?" in message.text.lower() or "согласен ?" in message.text.lower()),content_types=['text'])
def echo_all(message):
	bot.reply_to(message, "Истину глаголишь!")



@bot.message_handler(func=lambda message: random.randint(1, 2)==1 )
#@bot.message_handler(func=lambda message: True )
def echo_all(message):
	bot.reply_to(message, "Угу")




	#bot.download_file(telebot.apihelper.FILE_URL.format(bot.token, bot.get_file(message.sticker.file_id).file_path))
	#FILE_URL.format(token, file_path)

bot.polling()