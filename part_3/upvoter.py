from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
import json, os, time

def limit_reached(upvoted, upvote_list, author):
    if author not in upvoted:
        upvoted[author] = 0
        return False
    elif upvoted[author] == upvote_list[author]["upvote_limit"]:
        return True
    else:
        return False

def valid_post(post, upvote_list, upvoted):
    title  = post["title"]
    author = post["author"]

    if (post.is_main_post()
        and author in upvote_list
        and not limit_reached(upvoted, upvote_list, author)):
        return True
    else:
        return False

def run():
    username   = "steempytutorials"
    wif        = os.environ.get("UNLOCK")
    steem      = Steem(wif=wif)
    blockchain = Blockchain()
    stream     = map(Post, blockchain.stream(filter_by=["comment"]))
    upvote_list= json.load(open('upvote_list.json'))
    upvoted    = {}
    date       = int(time.strftime("%d"))
    hour       = int(time.strftime("%-H"))

    print("Entering blockchain stream!")
    while True:
        try:
            for post in stream:
                if int(time.strftime("%d")) is not date:
                    upvoted = {}
                    date = int(time.strftime("%d"))
                if int(time.strftime("%-H")) is not hour:
                    upvote_list  = json.load(open('upvote_list.json'))
                    hour = int(time.strftime("%-H"))

                if valid_post(post, upvote_list, upvoted):
                    try:
                        author = post["author"]
                        post.upvote(weight=upvote_list[author]["upvote_weight"],
                            voter=username)
                        print ("Upvoted {}".format(author))
                        upvoted[author] += 1
                    except Exception as error:
                        print(repr(error))
                        continue

        except Exception as error:
            #print(repr(error))
            continue

if __name__ == '__main__':
    run()
