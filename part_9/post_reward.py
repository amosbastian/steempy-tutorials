from steem import Steem
from steem.amount import Amount
from steem.post import Post

steem = Steem()
reward_fund = steem.get_reward_fund()
reward_balance = Amount(reward_fund["reward_balance"]).amount
recent_claims = float(reward_fund["recent_claims"])
reward_share = reward_balance / recent_claims
print(f"One reward share is currently worth: {reward_share}")

post = Post("@steempytutorials/part-8-how-to-create-your-own-upvote-bot-using-steem-python")

total_rshares = 0
for vote in post["active_votes"]:
    total_rshares += float(vote["rshares"])

print(f"The total reward shares of this post are: {total_rshares:.2f}")

print(f"The post is worth ${total_rshares * reward_share:.2f}")
print(steem.get_current_median_history_price())
base = Amount(steem.get_current_median_history_price()["base"]).amount
print(f"The post is actually worth ${total_rshares * reward_share * base:.2f}")

