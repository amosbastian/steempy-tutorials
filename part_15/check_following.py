from steem.account import Account
import sys

account = sys.argv[1]

for following in Account(account).get_following():
    print ('\n' + following)
    if account in Account(following).get_following():
        print  ('Follow back: Yes')
    else:
        print  ('Follow back: No')
