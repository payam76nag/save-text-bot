find1 = False #switch for findmessage or save message
import telegram
import pymongo
import pprint
from pymongo import MongoClient#mongodb client
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
client=MongoClient()
db=client.test_database
db=client.test_collection
db=client.test_database
collection=client.test_collection
posts=db.posts#creat new collection named posts
#-----------------------------------------------------------------------------
bot = telegram.Bot(token='TOKEN')
updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher
#-----------------------------------------------------------------------------
def start(bot, update):
       bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
#-----------------------------------------------------------------------------
start_handler = CommandHandler('start', start)#Link start function to \start command
dispatcher.add_handler(start_handler)#add start handler to dispatcher
#-----------------------------------------------------------------------------
def echo(bot, update):#if command \findmessage entered this function finds message that includs the string o.w saves string to database
      global find1
      if find1==True:
              for post in posts.find({"id": update.message.chat_id}):
                temp=post["text"]
                if temp.find(update.message.text) > -1:
                    bot.send_message(chat_id=update.message.chat_id, text=temp)

      else:
        chat_id=update.message.chat_id
        mes=update.message.text
        post = {"id":chat_id,
                 "text":mes}
        posts.insert_one(post)
      find1=False
def findmassage(bot, update):#set the tag true for echo func
    global find1
    find1=True
    print(find1)
def removeall(bot,update):#remove all messages of user
    db.posts.remove({"id":update.message.chat_id})

echo_handler = MessageHandler(Filters.text,echo)
dispatcher.add_handler(echo_handler)
#----------------------------------------
find_handler = CommandHandler('findmessage', findmassage)
dispatcher.add_handler(find_handler)
#----------------------------------------
removeall_handler = CommandHandler('removeall', removeall)
dispatcher.add_handler(removeall_handler)

updater.start_polling()

