from steem import Steem
from steem.transactionbuilder import TransactionBuilder
from steembase import operations

import time, random, os, json

def buy_upvote(author,upvote_bot, amount, permlink):
    transfers =[{
        'from': author,
        'to': upvote_bot,
        'amount': '{0:.3f} SBD'.format(amount),
        'memo': 'https://steemit.com/@{}/{}'.format(author, permlink)
    }]
    tb = TransactionBuilder()
    operation = [operations.Transfer(**x) for x in transfers]
    tb.appendOps(operation)
    tb.appendSigner(author, 'active')
    tb.sign()

    try:
        tx = tb.broadcast()
        print ("Buying vote succes")
    except Exception as error:
        print(repr(error))



def submit_post(title, tags, body, author, upvote_weight):
    steemPostingKey = os.environ.get('steemPostingKey')
    steem = Steem(wif=steemPostingKey)

    permlink_title = ''.join(e for e in title if e.isalnum()).lower()
    permlink = "{}-%s%s".format(permlink_title) % (time.strftime("%Y%m%d%H%M%S"), random.randrange(0,9999,1))

    try:
        steem.post(title, body, author, permlink, None, None, None, None, tags, None, False)
        steem.vote('@{}/{}'.format(author,permlink), upvote_weight, author)
        print ("Submitted post")
    except Exception as error:
        print(repr(error))

    return permlink




def run():
    author = 'sttest2'
    upvote_bot = 'minnowbooster'
    amount = 0.05

    hour = int(time.strftime("%-H"))

    while True:
        current_hour = int(time.strftime("%-H"))

        if current_hour is not hour:
            schedule = json.load(open('schedule.json'))
            posted = []

            for posting_time in schedule:
                if int(posting_time) == current_hour:
                    try:
                        title = schedule[posting_time]['title']
                        tags = schedule[posting_time]['tags']
                        filename = schedule[posting_time]['filename']
                        upvote_weight = schedule[posting_time]['upvote_weight']
                        body = open(filename,"r")
                        body = body.read()

                        permlink = submit_post(title, tags, body, author, upvote_weight)
                        posted.append(posting_time)
                    except Exception as error:
                        print(repr(error))
                        
            for posting_time in posted:
                del schedule[posting_time]
                print ("Removed entry from schedule")

            with open('schedule.json', 'w') as fp:
                json.dump(schedule, fp)
            print ("Saved file to harddrive")

            hour = int(time.strftime("%-H"))

        time.sleep(60)

    #buy_upvote(author, upvote_bot, amount, permlink)

if __name__ == '__main__':
        run()
