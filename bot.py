from config import *
import socket
import csv
import random
import sys
from app import server

questions = []
q_num = 0
question = ""
answer = ""
game_over = False

def joinChat():
    while True:
        line = server.recv(2048).decode("utf-8").split("/n").pop()
        if "End of /NAMES list" in line:
            sendMsg("triviabot has joined the chat")
            return

def loadQuestions():
    global questions
    with open(FILE, 'r') as csv_file: 
        # creating a csv reader object 
        csv_reader = csv.reader(csv_file) 
        # extracting each data row one by one 
        for row in csv_reader: 
            questions.append((row[0], row[1]))
        questions = questions[1:]
        # randomizes order of questions
        random.shuffle(questions)
        print("Questions loaded.")
        print("Total number of questions: %d" % len(questions)) 
        # print(questions)

def chooseQuestion():
    global questions, q_num, question, answer, game_over
    if q_num == len(questions):
        sendMsg("Those are all the questions we have! Thanks for playing :^)")
        game_over = True
        return
    curr = questions[q_num]
    question = curr[0]
    answer = curr[1]
    q_num += 1
    sendMsg("Question #%d of %d: %s" % (q_num, len(questions), question))    

# pongs server back to not timeout
def pong(line):
    server.send(bytes(line.replace("PING", "PONG") + "\r\n", "utf-8"))
    print("ponged")

# extracts username
def getUser(line):
    # print("user " + line.split("!")[0][1:])
    return line.split("!")[0][1:]

# extracts message
def getMsg(line):
    # print("msg " + line.split(":")[2])
    return line.split(":")[2]

# checks if message contains correct answer
def checkAnswer(msg):
    global answer
    if answer.lower() not in msg.lower():
        return False
    return True

def sendMsg(msg):
    server.send(bytes("PRIVMSG #" + CHANNEL + " :" + msg + "\r\n", "utf-8"))
    print("Sent:", msg)




# loadQuestions()

# server = socket.socket()
# server.connect((HOST, PORT))
# server.send(bytes("PASS " + PASS + "\r\n", "utf-8"))
# server.send(bytes("NICK " + NICK + "\r\n", "utf-8"))
# server.send(bytes("JOIN #" + CHANNEL + "\r\n", "utf-8"))
# joinChat()

# chooseQuestion()

# while True:
#     # print(server.recv(2048).decode("utf-8"))
#     line = server.recv(2048).decode("utf-8").split("\n")
#     if len(line) == 2:
#         line = line[0]
#         # print(line)
#         if "PING" in line:
#             pong(line)
#             continue
#         else:
#             user = getUser(line)
#             msg = getMsg(line)
#             print(user + ": " + msg)

#     if checkAnswer(msg):
#         sendMsg(user + " guessed the correct answer: " + answer)
#         chooseQuestion()

#     if game_over:
#         print("game over")
#         server.close()
#         sys.exit(0)

# def main():
#     print "Hello World"

# if __name__ == "__main__":
#     main()