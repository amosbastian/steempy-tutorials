from steem import Steem
from steem.transactionbuilder import TransactionBuilder
from steembase import operations
from steem.post import Post
import sys, os, time, random

def add_to_transfers(author, memo, transfers, sbd,  n, account):
    amount = sbd/n

    transfers.append(    {
            'from': account,
            'to': author,
            'amount': '{0:.3f} SBD'.format(amount),
            'memo': memo
        })

def payout(transfers, account):
    print ("Paying out winners")
    tb = TransactionBuilder(no_broadcast=False)
    operation = [operations.Transfer(**x) for x in transfers]
    tb.appendOps(operation)
    tb.appendSigner(account, 'active')
    tb.sign()
    tx = tb.broadcast()
    print ("Payout succes")

def submit_post(title, tags, body, upvote_weight, account):
    steemPostingKey = os.environ.get('steemPostingKey')
    steem = Steem(wif=steemPostingKey)

    permlink_title = ''.join(e for e in title if e.isalnum()).lower()
    permlink = "{}-%s%s".format(permlink_title) % (time.strftime("%Y%m%d%H%M%S"), random.randrange(0,9999,1))

    print ("Submitting post...")
    steem.post(title, body, account, permlink, None, None, None, None, tags, None, False)
    print ("Post submitted")
    steem.vote('@{}/{}'.format(account, permlink), upvote_weight, account)
    print ("Post upvoted")

def get_winner_data(winner):
    index = 0
    photo_index = 0
    string = winner.split(" ")
    permlink = string[0]

    if len(string)>1:
        photo_index = string[1]

    for c in permlink:
        if c == '@':
            return (permlink[index:], int(photo_index))
        index += 1

def run():
    filename = sys.argv[-1]
    url_list = open(filename).read().splitlines()

    account = url_list[0]
    post_title = url_list[1]
    tags = url_list[2]
    upvote_weight = float(url_list[3])
    memo = url_list[4]
    sbd = float(url_list[5])
    n = len(url_list)-6

    header = "<center>\n# Test selection\n***\n"
    body = ""
    footer = "End of test selection\n</center>"

    transfers = []

    for x in range(6,len(url_list)):
        permlink , photo_index = get_winner_data(url_list[x])
        post = Post(permlink)
        author = post['author']
        title = post['title']
        image = post['json_metadata']['image'][photo_index]

        body += "Title: {}<br>Author: @{}<br>Permlink: {}<br>Image:{}\n***\n".format(title, author, permlink, image)
        add_to_transfers(author, memo, transfers, sbd,  n, account)

    body = header + body + footer
    submit_post(post_title, tags, body, upvote_weight, account)
    payout(transfers, account)

if __name__ == '__main__':
    run()
