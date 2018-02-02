from steem.blockchain import Blockchain
from steem import Steem
from steem.post import Post
import threading, time, sys, os, queue, json

class myThread (threading.Thread):
	def __init__(self, thread_id, start_block, end_block, n, blockchain, workQueue, queueLock):
		threading.Thread.__init__(self)
		self.thread_id 		= thread_id
		self.start_block 	= start_block
		self.end_block 		= end_block
		self.n 				= n
		self.blockchain 	= blockchain
		self.stream			= self.blockchain.stream_from(start_block=start_block, end_block=end_block)
		self.current_block	= self.start_block
		self.workQueue		= workQueue
		self.queueLock		= queueLock

		print (self.thread_id, self.start_block, self.end_block)

	def run(self):
		data = {}
		for post in self.stream:
			if post['block'] != self.current_block:
				percentage = (self.current_block-self.start_block)/self.n*100
				print ("Thread {} is at block {}/{} {:.2f}%".format(self.thread_id,post['block'],self.end_block, percentage))
				self.current_block = post['block']

			operation = post['op'][0]

			if operation not in data:
				data[operation] = 1
			else:
				data[operation] += 1

		self.queueLock.acquire()
		self.workQueue.put(data)
		self.queueLock.release()

def run():
	start 				= time.clock()
	blockchain 			= Blockchain()
	head_block 			= blockchain.get_current_block_num()-int(sys.argv[1])
	block_count			= int(sys.argv[1])
	amount_of_threads	= int(sys.argv[2])
	n 					= int(block_count/amount_of_threads)
	start				= head_block-block_count
	threads = []

	queueLock = threading.Lock()
	workQueue = queue.Queue(amount_of_threads)

	for x in range(0, amount_of_threads):
	   thread = myThread(x, start, start+ n-1, n, blockchain, workQueue, queueLock)
	   thread.start()
	   threads.append(thread)
	   start = start + n

	print()

	for t in threads:
	   t.join()

	merged_data = {}

	while not workQueue.empty():
		data = workQueue.get()
		for key in data:
			if key not in merged_data:
				merged_data[key] = data[key]
			else:
				merged_data[key] += data[key]

	print (merged_data)

if __name__ == '__main__':
	run()
