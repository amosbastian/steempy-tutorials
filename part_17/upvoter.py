from steem import Steem
from steem.post import Post
import datetime, time

steem = Steem()
current_time = datetime.datetime.now()



# Set these variables
account = "sttest1"
identifier = '@photocontests/photocontests-selection-201801260600032712'
max_age  = datetime.timedelta(minutes=30)

bool = True

while bool == True:
	post = Post(identifier)

	# Check in post data if account is there
	post_votes = post['active_votes']
	for upvoter in post_votes:
		if upvoter['voter'] == account:
			print ("Already voted")
			bool = False

	# Use created time stamp to calculate age
	creation_time = post['created']
	if current_time - creation_time > max_age:
		print ('Post is to old')
		bool = False

	if bool is not False:
		steem.vote(identifier, 100, account)
		print ("Post upvoted\nWaiting 3 seconds\n")
		time.sleep(3)
