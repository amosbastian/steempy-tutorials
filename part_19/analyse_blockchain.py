from steem.blockchain import Blockchain
import sys

def run():
	blockchain 		= Blockchain()
	head_block 		= blockchain.get_current_block_num()
	start_block		= head_block-(int(sys.argv[1]))
	stream 			= blockchain.stream_from(start_block=start_block)
	block_count 	= int(sys.argv[1])
	current_block 	= start_block
	stats 			= {}
	operations		= 0
	counter			= 0

	print ("Starting from block {} for {} blocks\n".format(start_block, block_count))

	for post in stream:
		if post['block'] != current_block:
			counter += 1
			print ("Block {}/{} {:.2f}%".format(counter, block_count, counter/block_count*100))
			current_block = post['block']
		elif post['block'] == start_block+block_count:
			break

		operation = post['op'][0]

		if operation not in stats:
			stats[operation] = 1
		else:
			stats[operation] += 1
		operations += 1

	print ("operations {}\n".format(operations))
	for operation in stats:
		print (operation, stats[operation])

if __name__ == '__main__':
	run()
