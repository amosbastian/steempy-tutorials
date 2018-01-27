from steem import Steem
from steem.account import Account
from steem.post import Post
from steem.amount import Amount
from dateutil.parser import parse
from collections import namedtuple
import datetime

steem = Steem()

current_time = datetime.datetime.now()
time_period  = datetime.timedelta(hours=24)

account = "amosbastian"

User = namedtuple("User", ["name", "post", "pending"])
users = []

for vote in Account(account).history_reverse(filter_by="vote"):
    if vote["voter"] == account:
        time_voted = parse(vote["timestamp"])
        if current_time - time_voted < time_period:
            permlink = "@{}/{}".format(vote["author"], vote["permlink"])
            post = Post(permlink)
            if post.is_main_post():
                user = User(post["author"], post["title"],
                    Amount(post["pending_payout_value"]).amount)
                users.append(user)
        else:
            break

total_pending = sum([user.pending for user in users])
width = 40
for user in users:
    print("{0:16} - {1:43} - ${2}".format(
        user.name, user.post[:width] + (user.post[width:] and "..."),
        user.pending))

print("Total pending payout: ${}".format(total_pending))