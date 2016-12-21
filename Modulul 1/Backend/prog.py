from flask import Flask
from flask_cors import CORS, cross_origin
import MySQLdb, aiml,os
from memory_check import Memory
import threading
from mood import Mood
from personBD import *
from personality import *
from randomAnswer import RandomAnswer

app = Flask(__name__)

db = MySQLdb.connect(host="ppdatabase.ccvycmsqlp8u.eu-central-1.rds.amazonaws.com",    # your host, usually localhost
                     user="mariusdonici",         # your username
                     passwd="carrymeteodorescu",  # your password
                     db="ia")        # name of the data base

cur = db.cursor()

# Use all the SQL you like

# for row in cur.fetchall():
#     print row[0]
cur.execute("SELECT * FROM Users")

table= cur.fetchall()
cur.execute("SELECT * FROM Question")
questions = cur.fetchall()

db.close()

rnd = RandomAnswer()
sessionId=12345
# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")

initialize_bot(kernel,sessionId)

botMood = Mood()

attr=getPeopleAttributes()
iKnowOp=2

# Press CTRL-C to break this loop
@app.route('/<question>')
def main(question):
    global attr
    global iKnowOp
    print botMood.get_current_mood(question)
    #users=table
    bootMemory= Memory()
    res=kernel.respond(question,sessionId)
    if bootMemory.checkQuestionRepetition(question)==1:
        bootMemory.addQuestion(question)
        response=bootMemory.getRandomForRepetition()
        bootMemory.addResponse(response)
        return response
    bootMemory.addQuestion(question)
    bootMemory.addResponse(res)

    if len(attr)>1:
        attr=verifyExistence(kernel,sessionId,attr)
    if len(attr)==1:
        iKnowOp=1
    if len(attr)==0:
        iKnowOp=0
        decideToMemorate(kernel,sessionId)
    if res=='':
        res = rnd.answer(questions)
    return res


def deleteContent(fName):
    with open(fName, "w"):
        pass

if __name__ == '__main__':
    CORS(app)
    deleteContent('question.txt')
    app.run();