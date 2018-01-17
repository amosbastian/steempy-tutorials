from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
import json
import datetime
import re

steem = Steem()
blockchain = Blockchain()
stream = map(Post, blockchain.stream(filter_by=["comment"]))

def converter(object_):
    if isinstance(object_, datetime.datetime):
        return object_.__str__()

REGEX = "(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)"
username = "amosbastian"

while True:
    try:
        for post in stream:
            mentions = re.findall(REGEX, post["body"])
            if username in mentions:
                print(f"Replying to {post['author']}")
                post.reply(f"Hey @{post['author']} thanks for mentioning me!")

    except Exception as error:
        print(repr(error))
        continue