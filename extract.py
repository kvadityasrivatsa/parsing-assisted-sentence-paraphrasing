import pandas as pd
from tqdm import tqdm

mode = 'assisted'

# df = pd.read_csv('wiki.test.aligned.csv')

def vanilla(phase):

	print(f'>> generating vanilla_mode data for {phase} set')

	df = pd.read_csv(f'aligned_data/{phase}.csv')

	src_file = open(f'extracted_data/vanilla.{phase}.src','w')
	trg_file = open(f'extracted_data/vanilla.{phase}.trg','w')

	for row in tqdm(df.iterrows(),total=len(df)):

		src_sentence = row[1]['src_tok']
		trg_sentence = row[1]['trg_tok']

		print(src_sentence, file = src_file)
		print(trg_sentence, file = trg_file)

def assisted(phase):

	print(f'>> generating assisted_mode data for {phase} set')

	df = pd.read_csv(f'aligned_data/{phase}.csv')

	src_file = open(f'extracted_data/assisted.{phase}.src','w')
	trg_file = open(f'extracted_data/assisted.{phase}.trg','w')

	for row in tqdm(df.iterrows(),total=len(df)):

		src_toks = row[1]['src_tok'].split()
		src_deps = row[1]['src_dep'].split()
		src_sentence = ' '.join([f'< {t} @ {d} >' for t,d in zip(src_toks,src_deps)])

		trg_toks = row[1]['trg_tok'].split()
		trg_deps = row[1]['trg_dep'].split()
		trg_sentence = ' '.join([f'< {t} @ {d} >' for t,d in zip(trg_toks,trg_deps)])

		print(src_sentence, file = src_file)
		print(trg_sentence, file = trg_file)

if mode == 'vanilla':

	vanilla('train')
	vanilla('test')
	vanilla('dev')

elif mode == 'assisted':

	assisted('train')
	assisted('test')
	assisted('dev')
