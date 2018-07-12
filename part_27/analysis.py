from steem.blockchain import Blockchain
from steem import Steem
from datetime import datetime


import threading
import sys
import database


class myThread (threading.Thread):
    def __init__(self, thread_id, start_block, end_block, n, blockchain):
        threading.Thread.__init__(self)
        self.db = database.Database()
        self.thread_id = thread_id
        self.start_block = start_block
        self.end_block = end_block
        self.n = n
        self.blockchain = blockchain
        self.current_block = self.start_block
        self.data_hour = {}
        self.data_minute = {}
        self.data_day = {}

        self.hour = None
        self.date = None
        self.counter = 0

        print(self.thread_id, self.start_block, self.end_block)

    # Increase frequency counter
    def process_transaction(self, string, data):
        string = str(self.date) + ' ' + string
        if string in data:
            data[string] += 1
        else:
            data[string] = 1

    def dump_data(self):
        print(f'Thread {self.thread_id}: Inserting data into database')
        self.insert_into_db(self.data_minute, 'txs_minute')
        self.insert_into_db(self.data_hour, 'txs_hour')
        self.insert_into_db(self.data_day, 'txs_day')

    def process_block(self, block):
        timestamp = block['timestamp']
        datetime_object = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')

        # Keep track of the date
        if datetime_object.date() != self.date:
            self.date = datetime_object.date()

        # For each hour of data processed upload the data into the database
        # and clear the buffers.
        if datetime_object.hour != self.hour:
            self.dump_data()
            self.data_hour = {}
            self.data_minute = {}
            self.data_day = {}
            self.hour = datetime_object.hour

        # Count each transaction inside the block
        for operation in block['transactions']:
            hour = datetime_object.hour
            minute = datetime_object.minute

            # Allow for multiple resolutions
            self.process_transaction(f'{hour}:{minute}:00', self.data_minute)
            self.process_transaction(f'{hour}:00:00', self.data_hour)
            self.process_transaction(f'00:00:00', self.data_day)

    # Loop through the data dict and insert each pair into the database
    def insert_into_db(self, data, table):
        for time, amount in data.items():
            string = f'{time}'
            self.db.insert_selection(string, amount, table)

    def run(self):
        run = 0

        while run == 0:
            stream = self.blockchain.stream_from(start_block=self.start_block,
                                                 end_block=self.end_block,
                                                 full_blocks=True)
            try:
                for block in stream:
                    self.process_block(block)
                    percentage = ((self.start_block-self.current_block) /
                                  self.n*100)
                    print(f"Thread {self.thread_id}: block {self.start_block}/"
                          f"{self.end_block} {percentage:.2f}%")
                    self.start_block += 1

                    run = 1
            except Exception as e:
                print('Error:', e)

        self.dump_data()


def run():
    # Global variables for creating threads
    steem = Steem(['https://api.steemit.com'])
    blockchain = Blockchain(steem)
    head_block = blockchain.get_current_block_num()
    block_count = int(sys.argv[1])
    amount_of_threads = int(sys.argv[2])
    blocks_per_thread = int(block_count/amount_of_threads)
    start_block = head_block-block_count
    threads = []

    # Calculate start_block and end_block for each thread
    for thread_id in range(0, amount_of_threads):
        thread = myThread(thread_id, start_block,
                          start_block + blocks_per_thread-1, blocks_per_thread,
                          blockchain)
        thread.start()
        threads.append(thread)
        start_block = start_block + blocks_per_thread

    # Wait for all the threads to finish
    for t in threads:
        t.join()


if __name__ == '__main__':
    run()
