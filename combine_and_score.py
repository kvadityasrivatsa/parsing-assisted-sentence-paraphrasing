import re
import pandas as pd
from tqdm import tqdm 
from bleu import list_bleu

VANILLA_FILE = 'eval/eval_best.vanilla.txt'
ASSISTED_FILE = 'eval/eval_best.assisted.txt'
ALIGNED_FILE = 'aligned_data/test.csv'
OUTFILE = 'combined_output.txt'

def parse_aligned_file(path, sentences):

	df = pd.read_csv(path)
	sid = 0
	for row in df.iterrows():
		sentences[sid]['Sp'] = row[1]['src_dep'] 
		sentences[sid]['Tp'] = row[1]['trg_dep']
		sid+=1
	return sentences


def parse_fairseq_output(path):

	sentences = {}
	sid = None
	with open(path,'r') as infile:
		for line in infile.readlines():
			line = line.split()

			if line[0].startswith('S-'):	# source sentencesence
				sid = int(line[0].split('-')[1])
				sentences[sid] = {'S':None,'T':None,'H':None}
				sentences[sid]['S'] = ' '.join(line[1:])

			elif line[0].startswith('T-'):	# target sentencesence
				sentences[sid]['T'] = ' '.join(line[1:])

			elif line[0].startswith('H-'):	# predicted sentencesence
				sentences[sid]['H'] = ' '.join(line[2:])

	return sentences

def decode_assisted(sentences):
	for s in tqdm(sentences):
		sent = sentences[s]
		
		S = re.sub('<|>','',re.sub('> <','$split$',sent['S']))
		S = ' '.join([word.split()[0] for word in S.split('$split$')])
		sentences[s]['S'] = S

		T = re.sub('<|>','',re.sub('> <','$split$',sent['T']))
		T = ' '.join([word.split()[0] for word in T.split('$split$')])
		sentences[s]['T'] = T

		H = re.sub('<|>','',re.sub('> <','$split$',sent['H']))
		H = ' '.join([word.split()[0] for word in H.split('$split$')])
		sentences[s]['H'] = H
	return sentences

if __name__ == '__main__':

	doc = {}
	doc_score = {}

	vanilla_sentences = parse_fairseq_output(VANILLA_FILE)
	vanilla_sentences = parse_aligned_file(ALIGNED_FILE,vanilla_sentences)

	assisted_sentences = decode_assisted(parse_fairseq_output(ASSISTED_FILE))

	cumm_bleu_vanilla = list()
	cumm_bleu_assisted = list()

	outfile = open(OUTFILE,'w')
	for sid in tqdm(range(len(vanilla_sentences))):

		doc[sid] = ''

		# print(f"SID: {sid}",file=outfile)
		# print(f"S_: {vanilla_sentences[sid]['S']}",file=outfile)
		# print(f"T_: {vanilla_sentences[sid]['T']}",file=outfile)
		# print(file=outfile)
		# print(f"Sp: {vanilla_sentences[sid]['Sp']}",file=outfile)
		# print(f"Tp: {vanilla_sentences[sid]['Tp']}",file=outfile)
		# print(file=outfile)
		# print(f"H1: {vanilla_sentences[sid]['H']}",file=outfile)
		# print(f"H2: {assisted_sentences[sid]['H']}",file=outfile)
		# print(file=outfile)

		ref = vanilla_sentences[sid]['T']
		hyp1 = vanilla_sentences[sid]['H']
		hyp2 = assisted_sentences[sid]['H']

		sent_bleu_vanilla = list_bleu([[ref]],[hyp1])
		sent_bleu_assisted = list_bleu([[ref]],[hyp2])

		cumm_bleu_vanilla.append(sent_bleu_vanilla)
		cumm_bleu_assisted.append(sent_bleu_assisted)

		doc[sent_bleu_assisted-sent_bleu_vanilla] = ''

		doc[sid] += f"SID: {sid}\n"
		doc[sid] += f"S_: {vanilla_sentences[sid]['S']}\n"
		doc[sid] += f"T_: {vanilla_sentences[sid]['T']}\n"
		doc[sid] += f"\n"
		doc[sid] += f"Sp: {vanilla_sentences[sid]['Sp']}\n"
		doc[sid] += f"Tp: {vanilla_sentences[sid]['Tp']}\n"
		doc[sid] += f"\n"
		doc[sid] += f"H1: {vanilla_sentences[sid]['H']}\n"
		doc[sid] += f"H2: {assisted_sentences[sid]['H']}\n"
		doc[sid] += f"\n"
		doc[sid] += f"H1_BLEU: {sent_bleu_vanilla}\n"
		doc[sid] += f"H2_BLEU: {sent_bleu_assisted}\n"
		doc[sid] += '\n'+'='*70+'\n'

		doc_score[sid] = sent_bleu_assisted - sent_bleu_vanilla

		# print(f'H1_BLEU: {sent_bleu_vanilla}',file=outfile)
		# print(f'H2_BLEU: {sent_bleu_assisted}',file=outfile)
		# print('\n'+'='*70+'\n',file=outfile)

	doc_p =  dict()
	doc_n =  dict()

	for s in doc_score:
		if doc_score[s] >= 0:
			doc_p[s] = doc_score[s]
		else:
			doc_n[s] = doc[s]

	doc_p = dict(sorted(doc_p.items(), key=lambda item: item[1], reverse=True))
	doc_n = dict(sorted(doc_n.items(), key=lambda item: item[1], reverse=False))

	for s in doc_p:
		if doc_score[s] >=2:
			print(doc[s],file=outfile)

	for s in doc_n:
		if doc_score[s] <-2:
			print(doc[s],file=outfile)

	for s in doc_p:
		if doc_score[s] < 2:
			print(doc[s],file=outfile)

	for s in doc_n:
		if doc_score[s] >= -2:
			print(doc[s],file=outfile)
		
	print('Cummulative BLEU S:wcore (Vanilla): {}'.format(sum(cumm_bleu_vanilla)/len(cumm_bleu_vanilla)),file=outfile)
	print('Cummulative BLEU Score (Assisted): {}'.format(sum(cumm_bleu_assisted)/len(cumm_bleu_assisted)),file=outfile)

	print(cumm_bleu_vanilla)
	print(cumm_bleu_assisted)

	print(f'>> outputs and scores saved to {OUTFILE}')
