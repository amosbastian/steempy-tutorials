from steem import Steem
from steem.transactionbuilder import TransactionBuilder
from steembase import operations

import time, random, os

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



def submit_post(title, tags, body, author):
    steemPostingKey = os.environ.get('steemPostingKey')
    steem = Steem(wif=steemPostingKey)

    permlink_title = ''.join(e for e in title if e.isalnum()).lower()
    permlink = "{}-%s%s".format(permlink_title) % (time.strftime("%Y%m%d%H%M%S"), random.randrange(0,9999,1))

    try:
        steem.post(title, body, author, permlink, None, None, None, None, tags, None, True)
        print ("Submitted post")
    except Exception as error:
        print(repr(error))

    return permlink


def run():
    author = 'sttest2'
    upvote_bot = 'minnowbooster'
    amount = 0.05

    post = [line.rstrip('\n') for line in open('post.txt')]
    title  = post[0]
    tags = post[1]
    body = '\n'.join(post[2:])

    permlink = submit_post(title, tags, body, author)
    buy_upvote(author, upvote_bot, amount, permlink)

if __name__ == '__main__':
        run()
