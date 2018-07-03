from steem.blockchain import Blockchain
from steem.account import Account
from steem import Steem
from datetime import datetime

import sys
import os
import classes


class Steem_node():
    def __init__(self, block, account):
        self.block = block
        self.account = account
        self.nodes = ['https://rpc.steemviz.com', 'https://rpc.buildteam.io',
                      'https://api.steemit.com']
        self.steemPostingKey = os.environ.get('steemPostingKey')
        self.steem = Steem(wif=self.steemPostingKey, nodes=self.nodes)
        self.b = Blockchain(self.steem)
        self.queue = classes.Queue(self.steem, self.account)
        print('\nConnected to: {}'.format(self.nodes[0]))

    def process_timestamp(self, block):
        timestamp = block['timestamp']
        datetime_object = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        if datetime_object.second == 54:
            account = Account(self.account)
            print(f'\nVoting power: {account.voting_power()}%\n')
            if account.voting_power() == 100:
                self.queue.run_voting_round()

    def process_transaction(self, transaction):
        if transaction['operations'][0][0] == 'transfer':
            operation = transaction['operations'][0][1]
            self.process_transfer(operation)

    def process_transfer(self, operation):
        user = operation['from']
        amount = operation['amount']
        memo = operation['memo']
        bid = classes.Bid(user, amount, memo)

        if operation['to'] == self.account:
            self.queue.add_bid(bid)

    def run(self):
        while True:
            try:
                stream = self.b.stream_from(start_block=self.block,
                                            full_blocks=True)
                for block in stream:
                    print('Block:', self.block)
                    self.process_timestamp(block)

                    for transaction in block['transactions']:
                        self.process_transaction(transaction)

                    self.block += 1

            except Exception as e:
                print(repr(e))
                continue


if __name__ == '__main__':
    block = int(sys.argv[1])
    account = sys.argv[2]
    steem_node = Steem_node(block, account)
    steem_node.run()
