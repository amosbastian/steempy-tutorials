from steem.blockchain import Blockchain
from steem import Steem

import sys


class Steem_node():
    def __init__(self, block, block_count, operation):
        self.block = block
        self.end_block = block_count + self.block - 1
        self.operation = operation
        self.nodes = ['https://rpc.buildteam.io', 'https://api.steemit.com',
                      'https://rpc.steemviz.com']
        self.steem = Steem(nodes=self.nodes)
        self.b = Blockchain(self.steem)
        print('Booted\nConnected to: {}'.format(self.nodes[0]))

    def run(self):
        run = 1

        while run == 1:
            try:
                stream = self.b.stream_from(start_block=self.block,
                                            end_block=self.end_block,
                                            full_blocks=True)
                for block in stream:
                    print('\nBlock: ', self.block)
                    transaction_index = 0

                    for transaction in block['transactions']:
                        if transaction['operations'][0][0] == self.operation:
                            print(transaction_index,
                                  transaction['operations'][0][1])
                        transaction_index += 1

                    if self.block == self.end_block:
                        run = 0
                    else:
                        self.block += 1

            except Exception as e:
                continue


if __name__ == '__main__':
    block = int(sys.argv[1])
    block_count = int(sys.argv[2])
    operation = sys.argv[3]
    steem_node = Steem_node(block, block_count, operation)
    steem_node.run()
