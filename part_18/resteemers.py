from steem import Steem
from steem.account import Account
from steem.post import Post
from collections import Counter
import json
import datetime

def converter(object_):
    if isinstance(object_, datetime.datetime):
        return object_.__str__()

steem = Steem()
account = "steempytutorials"
resteemers = []
post_limit = 0

while post_limit < Account(account)["post_count"]:
    print(post_limit, post_limit + 500)
    for post in steem.get_blog(account, post_limit, 500):
        post = Post(post["comment"])
        if post.is_main_post() and post["author"] == account:
            permlink = post["permlink"]
            resteemed_by = steem.get_reblogged_by(account, permlink)
            if not resteemed_by == []:
                resteemed_by.remove(account)
            resteemers.extend(resteemed_by)

    post_limit += 500

for resteemer in Counter(resteemers).most_common(10):
    print("{0:16} has resteemed {1:16} {2:>3} times!".format(
        resteemer[0], account, resteemer[1]))