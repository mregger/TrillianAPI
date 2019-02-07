#!/usr/bin/env python3
#
#by Eduardo"

import re
import os
import twitter
import urllib
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

trillian = ChatBot('Trillian',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	database_url='./trillian.db')

trillian.set_trainer(ListTrainer)

'''
Get list of twitter accounts, and ignore the \n character
'''
f = open('twitter_accounts.txt')
accounts = [a[:-1] for a in f.readlines()]

max_tweets = 100

api = twitter.Api(consumer_key=os.environ['TWITTER_API_KEY'],
consumer_secret=os.environ['TWITTER_API_SECRET'],
access_token_key=os.environ['TWITTER_ACCESS_TOKEN'],
access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
sleep_on_rate_limit=True)

class Tweet:
	def __init__(self, content, parent):
		pass
		self.content = content
		self.parent = parent
		self.children = []

	def add_child(self, child):
		pass
		self.children.append(child)


def normalize_text(text):
	pass
	text = re.sub('(@\S*)', '', text)
	#TODO: remove any empty lines
	if text.isspace():
		return None
	return text

def extract_replies(tweet, parent):
	pass
	t = tweet.AsDict()
	heap = Tweet(normalize_text(t['full_text']), parent)
	id = t['id']
	user = t['user']['screen_name']
	max_id = None
	q = 'q=&result_type=recent&count=100&tweet_mode=extended&to='+user+'&since='+str(id)
	try:
		replies = api.GetSearch(raw_query=q)
		for reply in replies:
			if reply.in_reply_to_status_id == id:
				heap.add_child(extract_replies(reply, heap))
	except twitter.error.TwitterError as e:
		print('oopsie')
		time.sleep(60)

	return heap

def train(heap):
	pass
	'''
	iterate through the heap DFS style, adding the parent content as a possible
	incoming message, and the child content as a possible response.
	'''
	for c in heap.children:
		if c.content is not None and heap.content is not None:
			trillian.train([heap.content, c.content])
			train(c)

def print_tree(heap):
	pass
	s = ''
	'''
	Some strings are None, because the original tweet only contained a @asd.
	so we only write down the tweets that were not only empty lines.
	'''
	for c in heap.children:
		if c.content is not None:
			s += c.content + ', '
	print('\t', s)
	for c in heap.children:
		print_tree(c)

if __name__ == '__main__':
	for account in accounts:
		print('\t### - '+account+' - ###')
		print('querrying...')
		q = 'q=&from='+account+'&count='+str(max_tweets)+'&tweet_mode=extended&result_type=recent'
		tweets = api.GetSearch(raw_query=q)
		heaps = []
		print('getting replies...')
		for tweet in tweets:
			pass
			heaps.append(extract_replies(tweet, None))
		print('training Trillian...')
		for h in heaps:
			pass
			train(h)
			print('-------------------------------')
