#!/usr/bin/env python3
#
#by Eduardo"

import asyncio
import json
import sys
import time
import websockets

from chatterbot import ChatBot
trillian = ChatBot('Trillian',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	database_url='./trillian.db')

async def handle_message(m):
	print(m)
	m = json.loads(m)['content']
	content = str(trillian.get_response(m))+'\n'
	r = json.dumps({
		'from': 'Trillian',
		'content': content,
		'timestamp': time.time()
	})
	return r

async def on_message(ws, path):
	while True:
		m = await ws.recv()
		r = await handle_message(m)
		await ws.send(r)

if __name__ == '__main__':
	pass
	if len(sys.argv) > 1 and sys.argv[1] == 'prod':
		server = websockets.serve(on_message, "0.0.0.0", 80)
	else:
		server = websockets.serve(on_message, "localhost", 5000)
	asyncio.get_event_loop().run_until_complete(server)
	asyncio.get_event_loop().run_forever()
