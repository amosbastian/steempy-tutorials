<center>![steem-python.png](https://res.cloudinary.com/hpiynhbhq/image/upload/v1515886103/kmzfcpvtzuwhvqhgpyjp.png)</center>

This tutorial is part of a series where different aspects of programming with `steem-python` are explained. Links to the other tutorials can be found in the curriculum section below. This part will explain how to set up SMS notifications for votes on the STEEM Blockchain


---
#### Repository
https://github.com/steemit/steem-python

#### What will I learn

- Installing and configuring twilio
- Process votes
- Calculate $ value of a post
- Construct and send a SMS

#### Requirements

- Python3.6
- `steem-python`
- twilio

#### Difficulty
- basic
---

### Tutorial

#### Preface
Nowadays users often become bombarded with notifications and for this reason I have personally shut off almost all of them. I barely receive any text though so I figured I would look into setting up custom notifications by sms for votes performed by `utopian-io` on this account.


#### Setup
Download the files from [Github](https://github.com/amosbastian/steempy-tutorials/tree/master/part_28). There 2 are files `notifier.py` which is the main file that scans the STEEM Blockchain and takes two arguments `account` and `number`, `twilio_api.py` which contains the code for uploading sending an SMS via the Twilio API.

Run scripts as following:
`> python post_submitter.py juliank post.json`

### Installing and configuring twilio

Installation is simple using pip:

```
pip3 install twilio

```

However to use the Twilio API a account is required. There is a free trail account. Go to the following [link](https://www.twilio.com/) and create an account. After that you register your number and also receive a number to send messages from and obtain the `account_sid` and `auth_token`. Add this information inside `notifier.py`. Include the + for the number.


```
# Your Account Sid and Auth Token from twilio.com/console
account_sid = ''
auth_token = ''
number = ''
client = Client(account_sid, auth_token)


# Send sms and return sid
def send_sms(to, body):
    message = client.messages.create(body=body, from_=number, to=to)
    return(message.sid)
```
<br>
The trail account comes with $15 of credit. Depending on which country you are in this can be a lot of texts. The rate in the US is less than 1 cent.

#### Process votes
The block stream is set up to filter for `votes`. More information about that in this tutorial. A `vote` has the following structure.

```
{
	'voter': 'fxtuber10',
	'author': 'sherbanu',
	'permlink': 'steemtuner-fun-at-live-session-sudden-surprise-quiz-competition-with-exciting-rewards',
	'weight': 10000
}
```
<br>
In this example we will look for only incoming votes from the `utopian-io` account.

```
if voter == 'utopian-io' and author == account:
```
<br>
With this information it is possible to send a notification text that a vote has been received, at what time, in which block and with what upvote weight. However, we would like to know the $ value of the vote.

#### Calculate $ value of a post

This can be done by constructing a `Post` object and extracting additional information about the post from it.The `identifier` to create the post is made up out of a `@`, the user `account` and the `permlink` of the post.

```
# Construct post from the permlink to retrieve vote rshares
			post = Post(f'@{self.account}/{permlink}', self.steem)
```


From the post we can then extract the `active_votes` list. This is a list containing all the current votes on a post. We will need to filter for the vote made by `utopian-io`. This returns an number in `rshares`. Which is a `%` of the current `reward pool` and still has to be converted to $.

```
# Look for utopian in active_votes
active_votes = post['active_votes']
for vote in active_votes:
		if vote['voter'] == 'utopian-io':
				payout = self.convert_rshares(vote['rshares'])
```
<br>
To convert the `rshares` to dollar value we use the code provided by @emrebeyler in his tutorial about [rshares](https://goo.gl/dV7yVa):

```
def convert_rshares(self, rshares):
		reward_fund = self.steem.get_reward_fund()
		reward_balance, recent_claims = (reward_fund["reward_balance"],
																		 reward_fund["recent_claims"])
		base_price = self.steem.get_current_median_history_price()["base"]

		fund_per_share = Amount(reward_balance).amount / float(recent_claims)
		payout = float(rshares) * fund_per_share * Amount(base_price).amount
		return payout
```


#### Construct and send a SMS
The sms function takes a `number` to send the text to and the body of the text. The `number` has already been set so only the `body` has to be constructed. In this example we choose to have the `$ amount` included, as well as convert the `permlink` to an `url` so it becomes clickable from the phone and include the `block` and `timestamp`.

```
# Construct sms
url = f"http://steemit.com/@{self.account}/{permlink}"
body = (f"Upvote from Utopian-io for ${payout:.2f}\n" +
				f"\n{url}\n\nBlock: {self.block}" +
				f"\n{self.timestamp}")

self.send_sms(body)


def send_sms(self, memo):
		print(twilio_api.send_sms(self.number, memo))
```


#### Running the script
Running the code will scan the blockchain until a vote is found by `utopian-io` and send an sms with the details about the upvote and the $ value. This script can easily be adjusted for any kind of custom notifications. It can be used to receive a text from every upvote from every account. Or filter out votes that have a value greater than a preset amount. As there is a small fee to send the sms it is recommended to set some reasonable parameters.



#### Curriculum
##### Set up:
- [Part 0: How To Install Steem-python, The Official Steem Library For Python](https://steemit.com/utopian-io/@amosbastian/how-to-install-steem-python-the-official-steem-library-for-python)
- [Extracting EXIF (Meta)Data From Images With Python](https://steemit.com/utopian-io/@steempytutorials/extracting-exif-meta-data-from-images-with-python)

---

The code for this tutorial can be found on [GitHub](https://github.com/amosbastian/steempy-tutorials/tree/master/part_28)!

This tutorial was written by @juliank.
