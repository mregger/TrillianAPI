#!/usr/bin/env python3
#
#by Eduardo"

from flask import Flask, request
app = Flask(__name__)

from chatterbot import ChatBot
trillian = ChatBot('Trillian', trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
trillian.train('chatterbot.corpus.english')

@app.route('/', methods=['GET'])
def get_response():
    pass
    message = request.args.get('message')
    #return message.upper() + '\n'
    return str(trillian.get_response(message)) + '\n'

if __name__ == '__main__':
    pass
    app.run(debug=True)
