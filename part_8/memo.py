from steem import Steem
from steem.blockchain import Blockchain
import json
import datetime

def converter(object_):
    if isinstance(object_, datetime.datetime):
        return object_.__str__()

def run():
    steem = Steem()
    blockchain = Blockchain()
    stream = blockchain.stream(filter_by=["transfer"])

    username = "amosbastian"

    while True:
        try:
            for transfer in stream:
                if transfer["to"] == username:
                    url, permlink = transfer["memo"].split("@")
                    if "https://steemit.com/" in url:
                        steem.vote(f"@{permlink}", 100)
        except Exception as error:
            print(repr(error))
            continue
                