from logging import getLoggerClass
from pyrogram import Client,filters
import os
import time
import urllib.request

app = Client(session_name=os.environ['SESSION_STRING'],api_id=os.environ['API_ID'],api_hash=os.environ['API_HASH'],bot_token=os.environ['BOT_TOKEN'])


#  Creating of a Image Folder
if os.path.exists("IMG"):
    print("Path Exists")
else:
    os.makedirs("IMG")

chitchat_users = []

def uploader():
    print("Im Sending Photo...")
    urllib.request.urlretrieve(url="https://cataas.com/cat",filename="IMG/cat.jpg")
    for user in chitchat_users:
        app.send_photo(chat_id=user,photo="IMG/cat.jpg")
        print(user)
    print(chitchat_users)

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
        



@app.on_message(filters.command("start"))
def start_command(client,message):
    global chitchat,user_name,send_pics
    chitchat = message['chat']['id']
    user_name = message['chat']['username']
    print("\nHey Welcome use ",user_name)
    print("\nHaving id of ",chitchat)
    app.send_message(chat_id=os.environ['LOGGING_CHANNEL'],text="We got a new user "+ str(chitchat))
    send_pics = 1
    chitchat_users.append(chitchat)
    app.send_message(chat_id=chitchat,text="Hey "+user_name+" You have started the Cat Image Bot will sent you cat Image from now every 10 mins.")
    cat_imager()

@app.on_message(filters.command("stop"))
def stop_command(client,message):
    global stchitchat,send_pics
    stchitchat = message['chat']['id']
    app.send_message(chat_id=stchitchat,text="Thank You for Using our service...")
    app.send_message(chat_id=os.environ['LOGGING_CHANNEL'],text="We lost a user "+ str(chitchat))
    chitchat_users.remove(stchitchat)

@app.on_message(filters.command("source"))
def source(client,message):
    source_request = message['chat']['id']
    app.send_message(source_request,"[GitHub]('https://github.com/red-drive/Cat-Img-Bot.git')")

app.run()
