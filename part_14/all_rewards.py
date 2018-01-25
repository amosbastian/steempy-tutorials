from steem import Steem
from steem.post import Post
from steem.amount import Amount
from steem.account import Account
from dateutil.parser import parse
from datetime import timedelta, datetime

steem = Steem()

post = Post("@steempytutorials/part-12-how-to-estimate-curation-rewards")

# Everything we need to calculate the reward
reward_fund = steem.get_reward_fund()
reward_balance = Amount(reward_fund["reward_balance"]).amount
recent_claims = float(reward_fund["recent_claims"])
reward_share = reward_balance / recent_claims
base = Amount(steem.get_current_median_history_price()["base"]).amount

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

### Calculating beneficiary shares
def beneficiaries_pct(post):
    weight = sum([beneficiary["weight"] for beneficiary in post["beneficiaries"]])
    return  weight / 10000.0

### Calculating author and beneficiary rewards
def estimate_rewards(post):
    votes = [vote for vote in post["active_votes"]]
    total_share = sum([float(vote["rshares"]) * reward_share * base for vote in votes])
    curation_share = sum([curation_reward(post, vote) for vote in votes])
    author_share = (total_share - curation_share) * (1.0 - beneficiaries_pct(post))
    beneficiary_share = (total_share - curation_share) * beneficiaries_pct(post)

    print(f"Estimated total reward for this post is ${total_share:.2f}")
    print(f"Estimated author reward for this post is ${author_share:.2f}")
    print(f"Estimated beneficiary reward for this post is ${beneficiary_share:.2f}")
    print(f"Estimated curation reward for this post is ${curation_share:.2f}\n")

### Estimating rewards in last `N` days
account = "steempytutorials"
time_period  = timedelta(days=3)

posts = set()
for post in Account(account).history_reverse(filter_by="comment"):
    try:
        post = Post(post)
        if post.time_elapsed() < time_period:
            if post.is_main_post() and not post["title"] in posts:
                posts.add(post["title"])
                print(post["title"])
                estimate_rewards(post)
        else:
            break
    except Exception as error:
        continue
