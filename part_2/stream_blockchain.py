from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
import json
import datetime

def converter(object_):
	if isinstance(object_, datetime.datetime):
		return object_.__str__()

def stream_blockchain():
	blockchain = Blockchain()
	stream = map(Post, blockchain.stream(filter_by=['comment']))
	while True:
		try:
			for post in stream:
				tags = post["tags"]
				if post.is_main_post() and "utopian-io" in tags:
					author = post["author"]
					title = post["title"]
					print("{} posted {}".format(author, title))
		except Exception as error:
			print(repr(error))
			continue

if __name__ == '__main__':
	stream_blockchain()