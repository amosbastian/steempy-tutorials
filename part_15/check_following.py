from steem.account import Account
import sys

account = sys.argv[1]

for author in Account(account).get_following():
    print ('\n' + author)
    if account in Account(author).get_following():
        print  ('Follow back: Yes')
    else:
        print  ('Follow back: No')
