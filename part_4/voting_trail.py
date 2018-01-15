from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post

voting_trail = ["amosbastian", "juliank"]
template = "@{}/{}"

steem = Steem()
blockchain = Blockchain()
stream = blockchain.stream(filter_by=["vote"])

if __name__ == '__main__':
    while True:
        try:
            for vote in stream:
                voter = vote["voter"]
                author = vote["author"]
                permlink = vote["permlink"]

                if voter in voting_trail:
                    post = template.format(author, permlink)
                    if Post(post).is_main_post():
                        print("Voting on {} post that {} voted on!".format(
                            permlink, voter))
                        steem.vote(post, 100)
        except Exception as error:
            print(repr(error))
            continue