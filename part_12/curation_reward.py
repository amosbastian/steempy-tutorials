from steem import Steem
from steem.post import Post
from steem.amount import Amount
from dateutil.parser import parse
from datetime import timedelta

steem = Steem()

# Everything we need to calculate the reward
reward_fund = steem.get_reward_fund()
reward_balance = Amount(reward_fund["reward_balance"]).amount
recent_claims = float(reward_fund["recent_claims"])
reward_share = reward_balance / recent_claims
base = Amount(steem.get_current_median_history_price()["base"]).amount

# The post
post = Post("@steempytutorials/part-11-how-to-build-a-list-of-transfers-and-broadcast-these-in-one-transaction-with-steem-python")

### Sorting votes by rshares
# Create list of all votes, sort them by reward and print the top five
votes = [vote for vote in post["active_votes"]]
for vote in sorted(votes[:5], key=lambda x: float(x["rshares"]), reverse=True):
    print("{0:16} voted for ${1} - {2:>5}%".format(
        vote["voter"],
        str(float(vote["rshares"]) * reward_share * base)[:5],
        vote["percent"] / 100))

### Curation reward penalty
def curation_penalty(post, vote):
    post_time = post["created"]
    vote_time = parse(vote["time"])
    time_elapsed = vote_time - post_time
    reward = time_elapsed / timedelta(minutes=30) * 1.0

    if reward > 1.0:
        reward = 1.0
    return reward


### Calculating curation reward per vote
curation_pct = 0.25
def curation_reward(post, vote):
    rshares = float(vote["rshares"])
    base_share = reward_share * base

    return (rshares * curation_penalty(post, vote) * curation_pct) * base_share

### Adding everything together
curation_share = sum([curation_reward(post, vote) for vote in votes])
print(f"Estimated curation reward for this post is ${curation_share:.2}")

### Revisiting the votes
for vote in sorted(votes[:5], key=lambda x: float(x["rshares"]), reverse=True):
    print("{0:16} voted for ${1} - {2:>5}%".format(
        vote["voter"],
        str(curation_reward(post, vote))[:5],
        vote["percent"] / 100))