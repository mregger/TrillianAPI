#!/usr/bin/env python3
#
#by Eduardo"

import os
import json
import time
import re
import praw
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

trillian = ChatBot('Trillian',
	storage_adapter='chatterbot.storage.SQLStorageAdapter',
	database_url='./trillian.db')
trillian.set_trainer(ListTrainer)

api = praw.Reddit(
client_id=os.environ['REDDIT_CLIENT_ID'],
client_secret=os.environ['REDDIT_CLIENT_SECRET'],
user_agent='python:Trillian:v1 by /u/mregger'
)

max_words = 30
max_threads = 10
requests = 0
'''
Get list of subreddits, and ignore the \n character at the end of each word
'''
f = open('subreddit_list.txt')
subreddits = [s[:-1] for s in f.readlines()]

class Post:
    def __init__(self, content, id, parent):
        pass
        self.content = content
        self.parent = parent
        self.id = id
        self.children = []

    def add_child(self, child):
        pass
        self.children.append(child)

def normalize_text(text):
	pass
	pattern = re.match(r'(\s[oO][pP]\s)|([oO][pP]\s)|(\s[oO][pP]\'s\s)|([oO][pP]\'s\s)|(\s[oO][pP]\'s\.)|(\s[oO][pP]\.)', text)
	if pattern is not None:
		#print('Before: ', text)
		if pattern.group(1) is not None:
			text = text.replace(pattern.group(1), ' you')
		if pattern.group(2) is not None:
			text = text.replace(pattern.group(2), 'You ')
		if pattern.group(3) is not None:
			text = text.replace(pattern.group(3), ' your')
		if pattern.group(4) is not None:
			text = text.replace(pattern.group(4), 'Your ')
		if pattern.group(5) is not None:
			text = text.replace(pattern.group(5), ' you.')
		if pattern.group(6) is not None:
			text = text.replace(pattern.group(6), ' yours.')
		#print('After: ', text)
	return text

def scrutinize(text):
	pass
	#print('Checking: ', text, ' length: ', len(text))
	if len(text) > 255:
		pass
		'''
		Match posts with more than 20 words
		'''
		#print('Too long: ', text)
		return False
	if re.match('([a-z]\/\S*)', text) is not None:
		pass
		'''
		Match references to subreddits, or users
		'''
		#print('Contains subreddit, or user mentions: ', text)
		return False
	if re.match('([Rr]eddit)', text) is not None:
		pass
		'''
		Match any reference to reddit or redittors
		'''
		#print('Contains reddit or redditor mentions: ', text)
		return False
	if re.match('(\[deleted\])', text) is not None:
		pass
		'''
		Match deleted comments
		'''
		#print('Was deleted: ', text)
		return False
	if re.match('(\[removed\])', text) is not None:
		pass
		'''
		Match deleted comments
		'''
		#print('Was removed: ', text)
		return False
	return True

def extract_replies(submission, parent):
	pass
	global requests
	#time.sleep(1)
	'''
	Parse content, then visit subcomments
	TODO: Normalize text, so we get less inconsistent data:
	Ex.: mentions ot OP of thread -> change OP by 'you'

	'''
	heap = Post(normalize_text(submission.body), submission.id, parent)
	if type(submission).__name__ == 'Comment':
		pass
		children = submission.replies
	elif type(submission).__name__ == 'MoreComments':
		pass
		#children = submission.comments()
	for child in children:
		if type(child).__name__ != 'MoreComments' and scrutinize(child.body):
			child = extract_replies(child, heap)
			heap.add_child(child)
		else:
			pass
			#print('Not accepted: ', child.body)
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

def print_tree(heap, d):
    pass
    s = ''
    for i in range(0, d):
        s += '-'
    print(s,' ', heap.content)
    for c in heap.children:
        print_tree(c, d+1)

if __name__ == "__main__":
	pass
	for subreddit in subreddits:
		pass
		'''
		Find and ignore sticky posts first
		'''
		stickies = []
		for i in range(0, max_threads):
			pass
			try:
				stickies.append(api.subreddit(subreddit).sticky(i).id)
			except:
				break

		submissions = api.subreddit(subreddit).hot(limit=max_threads)
		for submission in submissions:
			if submission.id in stickies:
				continue
			requests += 1
			pass
			'''
			TODO:
			create a recursive method, which takes in a submission, sets the body of
			it in a heap object, and sets its children as the return value of its
			recursive call. The parameters should be a comment from the
			submission. Returns the heap.
			print(submission.title)
			comments = submission.comments.list()
			for comment in comments:
			    pass
			    print('\t', comment.id)
			    print('--')
			print('--------------------')
			'''
			heap = Post(submission.title, submission.id, None)
			print(' ## ', heap.content, ' ## ')
			replies = submission.comments
			replies = replies[:replies.__len__()]
			print()

			for reply in replies:
				if type(reply).__name__ != 'MoreComments' and scrutinize(reply.body):
					child = extract_replies(reply, heap)
					heap.add_child(child)

			#print_tree(heap, 0)
			train(heap)
