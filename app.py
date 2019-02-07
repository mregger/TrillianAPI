#!/usr/bin/env python3
#
#by Eduardo"

from flask import Flask, request
app = Flask(__name__)

from chatterbot import ChatBot
trillian = ChatBot('Trillian',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	database_url='./trillian.db')

@app.route('/', methods=['GET'])
def get_response():
    pass
    message = request.args.get('message')
    #return message.upper() + '\n'
    return str(trillian.get_response(message)) + '\n'

if __name__ == '__main__':
    pass
    app.run(debug=True)
