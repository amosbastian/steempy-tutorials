from steem.account import Account

user = Account('steempytutorials')
print ("Voting power is at {}%".format(user.voting_power()))
