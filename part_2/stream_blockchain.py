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
	stream = blockchain.stream(filter_by=['comment'])

	for post in stream:
		print(json.dumps(post, default=converter, indent=4, sort_keys=True))
		break

if __name__ == '__main__':
	stream_blockchain()