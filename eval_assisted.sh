echo " Running Evaluation"
echo "============================"

mkdir -p eval

echo ">>> evaluating file: checkPoints/checkpoint_best.assisted.pt"
fairseq-generate preproc_data \
--path checkPoints/checkpoint_best.assisted.pt \
--batch-size 128 --beam 8 --remove-bpe > eval/eval_best.assisted.txt
echo ">>> saved generated report to file: eval/eval_best.assisted.txt"

