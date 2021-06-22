echo " Training New Model"
echo "========================================================="

echo ">>> setting up environment"
rm -rf preproc_data
mkdir preproc_data

echo ">>> converting data to bin and idx format"
fairseq-preprocess --source-lang src --target-lang trg \
--trainpref extracted_data/assisted.train \
--validpref extracted_data/assisted.dev \
--testpref extracted_data/assisted.test \
--destdir preproc_data \
--workers 30

echo ">>> training model"

fairseq-train preproc_data --save-dir checkPoints \
--lr 0.00011 --lr-scheduler 'fixed' \
--optimizer adam --adam-betas '(0.9, 0.999)' --adam-eps 1e-08 \
--dropout 0.2 --arch 'transformer' --warmup-updates 4000 \
--encoder-embed-dim 256 --encoder-ffn-embed-dim 1024 \
--decoder-embed-dim 256 --decoder-ffn-embed-dim 1024 \
--encoder-layers 3 --encoder-attention-heads 4 \
--decoder-layers 3 --decoder-attention-heads 4 \
--seed 0 --scoring bleu --max-tokens 2000 --max-epoch $2\
--checkpoint-suffix '.assisted' --no-epoch-checkpoints
