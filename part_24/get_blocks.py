from steem.blockchain import Blockchain
from steem import Steem

import sys
import operations


class Steem_node():
    def __init__(self, block, block_count, tag):
        self.block = block
        self.end_block = block_count + self.block - 1
        self.tag = tag
        self.nodes = ['https://rpc.buildteam.io', 'https://api.steemit.com',
                      'https://rpc.steemviz.com']
        self.steem = Steem(nodes=self.nodes)
        self.b = Blockchain(self.steem)
        print('Booted\nConnected to: {}'.format(self.nodes[0]))

    def process_operation(self, operation, tag, timestamp):
        if tag == 'transfer':
            transfer = operations.Transfer(operation, self.block, timestamp)
            transfer.print_operation()
        elif tag == 'transfer_to_vesting':
            transfer_to_vesting = operations.Transfer_to_vesting(operation,
                                                                 self.block,
                                                                 timestamp)
            transfer_to_vesting.print_operation()
        elif tag == 'withdraw_vesting':
            withdraw_vesting = operations.Withdraw_vesting(operation,
                                                           self.block,
                                                           timestamp)
            withdraw_vesting.print_operation()
        elif tag == 'convert':
            convert = operations.Convert(operation, self.block, timestamp)
            convert.print_operation()

    def run(self):
        run = 1

        while run == 1:
            try:
                stream = self.b.stream_from(start_block=self.block,
                                            end_block=self.end_block,
                                            full_blocks=True)
                for block in stream:
                    print('Block:', self.block)
                    transaction_index = 0

                    for transaction in block['transactions']:
                        if transaction['operations'][0][0] == self.tag:
                            self.process_operation(transaction['operations']
                                                   [0][1],
                                                   self.tag,
                                                   block['timestamp'])
                        transaction_index += 1

                    if self.block == self.end_block:
                        run = 0
                    else:
                        self.block += 1

            except Exception as e:
                print(repr(e))
                continue


if __name__ == '__main__':
    block = int(sys.argv[1])
    block_count = int(sys.argv[2])
    tag = sys.argv[3]
    steem_node = Steem_node(block, block_count, tag)
    steem_node  .run()
