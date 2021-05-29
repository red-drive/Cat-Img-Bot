from logging import getLoggerClass
from pyrogram import Client,filters
import os
import time
import urllib.request
from pymongo import MongoClient
dbname = os.environ['DB_NAME']

cluster = MongoClient("mongodb://"+os.environ['DB_USER']+":"+os.environ['DB_PASS']+"@cluster0-shard-00-00.twn2c.mongodb.net:27017,cluster0-shard-00-01.twn2c.mongodb.net:27017,cluster0-shard-00-02.twn2c.mongodb.net:27017/"+dbname+"?ssl=true&replicaSet=atlas-15u7xa-shard-0&authSource=admin&retryWrites=true&w=majority")
db = cluster[dbname]
collection = db['cat_db']

app = Client(session_name=os.environ['SESSION_STRING'],api_id=os.environ['API_ID'],api_hash=os.environ['API_HASH'],bot_token=os.environ['BOT_TOKEN'])
chitchat_users = []

#  Creating of a Image Folder
if os.path.exists("IMG"):
    print("Path Exists")
else:
    os.makedirs("IMG")
#  Importing Users from Table
result = collection.find({})
for chit in result["_id"]:
  chitchat_users.append(chit)

def uploader():
    print("Im Sending Photo...")
    urllib.request.urlretrieve(url="https://cataas.com/cat",filename="IMG/cat.jpg")
    for user in chitchat_users:
        app.send_photo(chat_id=user,photo="IMG/cat.jpg")

def cat_imager():
    global send_pics
    print("doing This")
    while int(send_pics) == 1:
        if chitchat_users == []:
            print("No User To Send Photo") 
            break
        else:    
            uploader()

        time.sleep(600)
        



@app.on_message(filters.command("start") & filters.private)
def start_command(client,message):
    global chitchat,user_name,send_pics
    chitchat = message['chat']['id']
    user_name = message['chat']['username']
    send_pics = 1
    chitchat_users.append(chitchat)
    try:
      collection.insert_one({"_id":chitchat,"user":user_name})
      app.send_message(chat_id=chitchat,text="Hey "+user_name+" You have started the Cat Image Bot will sent you cat Image from now every 10 mins.")
      cat_imager()
    except:
      app.send_message(chitchat,text="You have already Subscribed to our bot")

@app.on_message(filters.command("stop"))
def stop_command(client,message):
    global stchitchat,send_pics
    stchitchat = message['chat']['id']
    try:
      collection.delete_one({"_id":stchitchat})
      app.send_message(chat_id=stchitchat,text="Thank You for Using our service...")
      chitchat_users.remove(stchitchat)
    except:
      app.send_message(stchitchat,text="You have been not yet Subscribed for removing you sorry")

@app.on_message(filters.command("source"))
def source(client,message):
    source_request = message['chat']['id']
    app.send_message(source_request,"[GitHub]('https://github.com/red-drive/Cat-Img-Bot.git')")

app.run()
