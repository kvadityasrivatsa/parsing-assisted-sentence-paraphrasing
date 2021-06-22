import re
import os
import argparse

if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument('--src-path', action='store', dest='src_path', type=str, default=None,
	                    help='path to source directory.')
	parser.add_argument('--dst-path', action='store', dest='dst_path', type=str, default=None,
	                    help='path to destination directory.')
	parser.add_argument('--tok-count', action='store', dest='tok_count', type=int, default=0,
	                    help='number of control tokens in input files.')
	parser.add_argument('--sent-count', action='store', dest='sent_count', type=int, default=359,
	                    help='number of sentences in input files.')
	parser.add_argument('--dst-prefix', action='store', dest='dst_prefix', type=str, default='epoch',
	                    help='filename prefix for output files.')
	parser.add_argument('--max-epochs', action='store', dest='max_epochs', type=int, default=50,
	                    help='generate till max_epochs file only.')

	res = parser.parse_args()

	os.mkdir(res.dst_path)

	for file in os.listdir(res.src_path):

		hypo = {i+1:'' for i in range(res.sent_count)}

		file_id = int(file.rstrip('.txt').split('_')[4])

		if file_id > res.max_epochs:
			continue

		with open(os.path.join(res.src_path,file)) as infile:

			for line in infile.readlines():

				line = line.rstrip('\n').split()

				# if re.match('S-[0-9]+',line[0]):
				# 	# print(line)
				# 	sent.append(' '.join(line[1+res.tok_count:]))
				# 	print(sent[-1])

				# elif re.match('T-[0-9]+',line[0]):
				# 	# print(line)
				# 	targ.append(' '.join(line[1:]))
				# 	print(targ[-1])

				# elif re.match('H-[0-9]+',line[0]):
				if re.match('H-[0-9]+',line[0]):
					sent_id = int(line[0].split('-')[1])
					# print(line)
					hypo[sent_id] = ' '.join(line[2:])
					# print(hypo[-1])
					# print()

					# print(line)
					# print(sent_id)
					# print(' '.join(line[2:]))
					# print()


		out = [hypo[i]+'\n' for i in range(res.sent_count)]

		with open(os.path.join(res.dst_path,'{}_{}'.format(res.dst_prefix,file_id)),'w') as outfile:
			outfile.writelines(out)

