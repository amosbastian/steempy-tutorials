from steem.post import Post
from steem.amount import Amount


class Bid():
    def __init__(self, user, amount, memo):
        self.user = user
        self.amount = Amount(amount)
        self.memo = memo
        self.post = 0


class Queue():
    def __init__(self, steem, account):
        self.list = {}
        self.total_sbd = 0
        self.steem = steem
        self.account = account

    def refund(self, bid, memo):
        print('Refund: ', memo)
        self.steem.transfer(to=bid.user,
                            amount=bid.amount['amount'],
                            asset=bid.amount['asset'],
                            memo=memo,
                            account=self.account)

    def verify_bid(self, bid):
        valid = 1

        while valid == 1:
            try:
                bid.post = Post(bid.memo)
                if bid.post['identifier'] in self.list:
                    self.refund(bid, 'Already in list\n')
                    valid = 0
            except Exception as e:
                self.refund(bid, 'Invalid url\n')
                valid = 0

            if bid.amount['asset'] != 'SBD':
                self.refund(bid, 'Invalid asset\n')
                valid = 0
            break

        return valid

    def add_bid(self, bid):
        print(f'\nProcessing bid from {bid.user} for {bid.amount}')

        if self.verify_bid(bid) == 1:
            print('Added bid to list\n')
            self.list[bid.post['identifier']] = bid.amount['amount']
            self.total_sbd += bid.amount['amount']

    def reset(self):
        self.list = {}
        self.total_sbd = 0

    def run_voting_round(self):
        print('Starting upvoting round:\n')

        for post in self.list:
            upvote_pct = self.list[post]/self.total_sbd*100
            self.steem.vote(post, upvote_pct, account=self.account)
            print(f'Upvoted {post} {upvote_pct:.2f}%')
        self.reset()

        print('\nFinished upvoting round')
