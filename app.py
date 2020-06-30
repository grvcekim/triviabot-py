from flask import Flask, render_template
from config import *
import bot as b
import socket
import csv
import random
import sys 
#import os
#import sys

# def readbot_file():
#   with open(bot.py) as f:
#       read_data = f.read() 

app = Flask(__name__)


b.loadQuestions()

server = socket.socket()
server.connect((HOST, PORT))
server.send(bytes("PASS " + PASS + "\r\n", "utf-8"))
server.send(bytes("NICK " + NICK + "\r\n", "utf-8"))
server.send(bytes("JOIN #" + CHANNEL + "\r\n", "utf-8"))
b.joinChat()

b.chooseQuestion()

while True:
    # print(server.recv(2048).decode("utf-8"))
    line = server.recv(2048).decode("utf-8").split("\n")
    if len(line) == 2:
        line = line[0]
        # print(line)
        if "PING" in line:
            b.pong(line)
            continue
        else:
            user = b.getUser(line)
            msg = b.getMsg(line)
            print(user + ": " + msg)

    if b.checkAnswer(msg):
        b.sendMsg(user + " guessed the correct answer: " + b.answer)
        b.chooseQuestion()

    if b.game_over:
        print("game over")
        server.close()
        sys.exit(0)

# home route
@app.route("/")
def home():
    # return "hi"
    return b.question
    # return render_template('index.html', name = 'Jane', gender = 'Female')

# # serving form web page
# @app.route("/my-form")
# def form():
#     return render_template('index.html')

# # handling form data
# @app.route('/form-handler', methods=['POST'])
# def handle_data():
    
#     return "Request received successfully!"

# app.run(debug = True)
