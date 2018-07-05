from steem.blockchain import Blockchain
from steem import Steem

import sys
import db


class Steem_node():
    def __init__(self, block, block_count):
        self.block = block
        self.end_block = block_count + self.block - 1
        self.tag = 'transfer'
        self.nodes = ['https://api.steemit.com',
                      'https://rpc.buildteam.io',
                      'https://rpc.steemviz.com']
        self.steem = Steem(nodes=self.nodes)
        self.b = Blockchain(self.steem)
        print('Booted\nConnected to: {}'.format(self.nodes[0]))

    def process_transaction(self, index, block, operation):
        date = block['timestamp']
        to = operation['to']
        user = operation['from']
        amount = operation['amount']
        memo = operation['memo']

        db.insert_selection(self.block, index, date, to, user, amount, memo)

    def run(self):
        run = 1

        # run until end_block
        while run == 1:
            try:
                # stream full blocks starting at start_block
                stream = self.b.stream_from(start_block=self.block,
                                            end_block=self.end_block,
                                            full_blocks=True)

                # process each block indiviudally
                for block in stream:
                    print('\nBlock: ', self.block)

                    # keep track of transaction index inside block
                    index = 0

                    # go over each transaction indivually, process if tag is
                    # met and update index
                    for transaction in block['transactions']:
                        if transaction['operations'][0][0] == self.tag:
                            self.process_transaction(index,
                                                     block,
                                                     transaction['operations']
                                                     [0][1])
                        index += 1

                    # Check if current block equals the end_block, break if so
                    # else update the current block
                    if self.block == self.end_block:
                        run = 0
                    else:
                        self.block += 1

            except Exception as e:
                print('Error:', e)
                continue


if __name__ == '__main__':
    block = int(sys.argv[1])
    block_count = int(sys.argv[2])
    steem_node = Steem_node(block, block_count)
    steem_node.run()
