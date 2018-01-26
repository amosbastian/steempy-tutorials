from steem.account import Account
import sys

# retrieve commend line variables
account1 = sys.argv[1]
account2 = sys.argv[2]

# create account objects
account1_following = Account(account1).get_following()
account2_following = Account(account2).get_following()
account1_followers = Account(account1).get_followers()
account2_followers = Account(account2).get_followers()


print ('Account1: {}\nAccount2: {}\n'.format(account1, account2))

if account2 in account1_following:
    print  ('Follow back: Yes')
else:
    print  ('Follow back: No')

mutual_following = []
# for each user that is followed retrieve the list of users
# followed by this user. When match add to list
for following in account2_following:
    if following in account1_following:
        mutual_following.append(following)


print ('Mutual following: {}'.format(len(mutual_following)))
print (mutual_following)

mutual_followers = []
# for each user that is following retrieve the list of users
# following this user. When match add to list
for follower in account2_followers:
    if follower in account1_followers:
        mutual_followers.append(follower)

print ('Mutual followers: {}'.format(len(mutual_followers)))
print (mutual_followers)
