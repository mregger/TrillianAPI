#!/usr/bin/env python3
#
#by Eduardo"

import sys
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
    if len(sys.argv) > 1 and sys.argv[1] == 'lts':
        app.run(debug=False, port=80, host='0.0.0.0')
    elif len(sys.argv) > 1 and sys.argv[1] == 'help':
        print('To run in debug mode, use the command\n\t$ ./app.py\nTo run in production mode:\n\t $ sudo ./app.py lts&')
    else:
        app.run(debug=True, port=5000)
