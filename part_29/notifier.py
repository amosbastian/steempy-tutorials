from steem.blockchain import Blockchain
from steem import Steem
from steem.post import Post
from steem.amount import Amount

import sys
import twilio_api
import time


class Steem_node():
    def __init__(self, acount, number):
        self.tag = 'vote'
        self.account = account
        self.number = number
        self.nodes = ['https://api.steemit.com',
                      'https://rpc.buildteam.io',
                      'https://rpc.steemviz.com']
        self.steem = Steem(nodes=self.nodes)
        self.b = Blockchain(self.steem)
        self.timestamp = None
        self.block = self.b.get_current_block_num()
        print('Booted\nConnected to: {}'.format(self.nodes[0]))

    def send_sms(self, memo):
        print(twilio_api.send_sms(self.number, memo))

    # Convert rshares to dollar value
    # Author: emrebeyler
    # Source: https://goo.gl/dV7yVa
    def convert_rshares(self, rshares):
        reward_fund = self.steem.get_reward_fund()
        reward_balance, recent_claims = (reward_fund["reward_balance"],
                                         reward_fund["recent_claims"])
        base_price = self.steem.get_current_median_history_price()["base"]

        fund_per_share = Amount(reward_balance).amount / float(recent_claims)
        payout = float(rshares) * fund_per_share * Amount(base_price).amount
        return payout

    def process_vote(self, vote):
        print(vote)
        voter = vote['voter']
        author = vote['author']
        permlink = vote['permlink']
        weight = vote['weight']

        # Verify that utopian-io is the voter and that is votes on account
        if voter == 'utopian-io' and author == account:
            print(f"\nVoter: {voter}\nAuthor: {author}\nPermlink: {permlink}" +
                  f"\nWeight: {weight}\n{self.timestamp}\n")

            # Construct post from the permlink to retrieve vote rshares
            post = Post(f'@{self.account}/{permlink}', self.steem)

            # Look for utopian in active_votes
            active_votes = post['active_votes']
            for vote in active_votes:
                if vote['voter'] == 'utopian-io':
                    payout = self.convert_rshares(vote['rshares'])

            # Construct sms
            url = f"http://steemit.com/@{self.account}/{permlink}"
            body = (f"Upvote from Utopian-io for ${payout:.2f}\n" +
                    f"\n{url}\n\nBlock: {self.block}" +
                    f"\n{self.timestamp}")
            self.send_sms(body)

    def run(self):
        print(self.block)

        while True:
            try:
                # stream full blocks
                stream = self.b.stream_from(start_block=self.block,
                                            full_blocks=True)

                # process each block indiviudally
                for block in stream:
                    self.timestamp = block['timestamp']
                    print(f'{self.timestamp} Block: {self.block}', end='\r')

                    # go over each transaction indivually, process if tag is
                    # met and update index
                    for transaction in block['transactions']:
                        if transaction['operations'][0][0] == self.tag:
                            transfer = transaction['operations'][0][1]
                            self.process_vote(transfer)

                    self.block += 1

            except Exception as e:
                # common exception for api.steemit.com
                # when the head block is reached
                s = ("TypeError('an integer is"
                     " required (got type NoneType)',)")
                if repr(e) == s:
                    time.sleep(3)


if __name__ == '__main__':
    try:
        account = sys.argv[1]
        number = sys.argv[2]
        steem_node = Steem_node(account, number)
        steem_node.run()
    except Exception as e:
        print("Takes two argument: account number")
