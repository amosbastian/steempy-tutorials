from steem import Steem
from steem.blockchain import Blockchain
from steem.post import Post
from steem.account import Account
import json, os, time

def start_upvote_cycle(upvote_queue, account):
    for identifier in upvote_queue:
        try:
            upvote_weight = upvote_queue[identifier]
            print ("Upvoting {} for {} %".format(identifier, upvote_weight))
            steem.vote(identifier, upvote_weight, account)
            print ("Succes, sleeping for 3 seconds")
            time.sleep(3)
        except Exception as e:
            print (repr(e))

    # clear queue
    upvote_queue = {}


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
    account     = "sttest1"
    account      = Account(account)
    wif          = os.environ.get("UNLOCK")
    steem        = Steem(wif=wif)
    blockchain   = Blockchain()
    stream       = map(Post, blockchain.stream(filter_by=["comment"]))
    upvote_list  = json.load(open('upvote_list.json'))
    upvoted      = {}
    upvote_queue = {}
    date         = int(time.strftime("%d"))
    hour         = int(time.strftime("%-H"))

    print("Entering blockchain stream!")
    while True:
        try:
            for post in stream:

                time_string = str(post.time_elapsed())
                post_age = time_string.split(":")

                try:
                    # Omit posts older than 10 min
                    if int(post_age[0]) > 0 or int(post_age[1]) > 10:
                        break
                except Exception as e:
                    #print (repr(e))
                    break

                # start upvoting cycle at 100% votint power
                if account.voting_power() == 100:
                    start_upvote_cycle(upvote_queue, account)

                # check for new date
                if int(time.strftime("%d")) is not date:
                    upvoted = {}
                    date = int(time.strftime("%d"))
                #check for new hour
                if int(time.strftime("%-H")) is not hour:
                    upvote_list  = json.load(open('upvote_list.json'))
                    hour = int(time.strftime("%-H"))

                # verify post and add to queue
                if valid_post(post, upvote_list, upvoted):
                    try:
                        author = post["author"]
                        print ("\nAdding to queue{}\nPermlink: {}".format(author, post['identifier']))
                        if post['identifier'] not in upvote_queue:
                            upvote_queue[post['identifier']] = upvote_list[author]["upvote_weight"]
                            print ("Upvoted {} for {}%".format(author, upvote_list[author]["upvote_weight"]))
                            upvoted[author] += 1
                    except Exception as error:
                        print(repr(error))
                        continue

        except Exception as error:
            #print(repr(error))
            continue

if __name__ == '__main__':
    run()
