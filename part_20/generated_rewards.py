from steem import Steem
from steem.account import Account
from steem.post import Post
from steem.amount import Amount
from dateutil.parser import parse
from datetime import datetime, timedelta

steem = Steem()
account = "juliank"

# Get days since account creation
created = parse(Account(account)["created"]).date()
today = datetime.today().date()
days = today - created

# Create dictionary
dates = {}
for day in range(days.days + 1):
    dates[str(created + timedelta(days=day))] = 0

# Iterate over all blog posts
post_limit = 0
while post_limit < Account(account)["post_count"]:
    print(post_limit, post_limit + 500)
    for post in steem.get_blog(account, post_limit, 500):
        post = Post(post["comment"])
        if post.is_main_post() and post["author"] == account:
            post_date = str(post["created"].date())
            payout = Amount(post["pending_payout_value"]).amount
            if payout == 0:
                payout = (Amount(post["total_payout_value"]).amount + 
                    Amount(post["curator_payout_value"]).amount)
            print(post_date, payout)
            dates[post_date] += payout
    post_limit += 500

# Getting x and y values
x = [datetime.strptime(date, "%Y-%m-%d").date() for date in dates.keys()]
y = [sum(list(dates.values())[0:i]) for i in range(len(dates.values()))]

def first_reward():
    for i, reward in enumerate(y):
        if reward > 0:
            return i

# Plotting the graph
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.xticks([x[0], x[first_reward() - 1], x[-1]], visible=True, rotation="horizontal")

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.xlabel("{} to {} for @{}".format(created, today, account))
plt.ylabel("Sum of post rewards generated")

plt.grid()
plt.plot(x, y)
plt.show()