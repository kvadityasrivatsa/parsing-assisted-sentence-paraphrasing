
# Parsing Assisted Sentence Paraphrasing
This project utilizes dependency labels of sentences along with the sentence tokens as parallely learnt sequences to boost sentence paraphrasing performance.

## Getting Started

### Dependecies
- Python 3.7

### Installation
``` 
git clone https://github.com/kvadityasrivatsa/parsing-assisted-sentence-simplification
cd parsing-assisted-sentence-simplification
./setup.sh
```
### How to use
Train the submission model on [Google’s PAWS-Wiki dataset](https://github.com/google-research-datasets/paws)
- for Vanilla model (Transformer):
```
bash train_vanilla.sh <no. of max epochs>
```
   
- for Assisted Model (Transformer+Aligned parsed tokens):
```
bash train_assisted.sh <no. of max epochs>
```

## Pretrained Model
The checkpoint for the model with the best scores is available [here](https://drive.google.com/drive/folders/1w6fE4kO3WvNNuNMO_7jBQ91KCYR8cfIj?usp=sharing)

## Model Desciption
### Architecture
The model makes use of the Transformer architecture (Vaswani et. al., 2017) with 3 encoding and decosing layers, 4 attention heads, encoding and decoding embedding of 256 and full-connected layers with size 1024.
### Data Processing 
While the Vanilla model simply uses the raw aligned corpus for training, the Assisted model first uses Stanza'a Universal Dependency Parser to generate the dependency parses for each sentence and reformats the inputs to the Transformer encoder the following way:

**Raw Sentence**
```There are also specific discussions , public profile debates and project discussions```
 **Dep Tags:**
```expl root advmod amod nsubj punct amod compound conj cc compound conj punct```
**Resultant Paired Sequence:**
```<There @ expl> <are @ root> <also @ advmod> <specific @ amod> <discussions @ nsubj> <, @ punct> <public @ amod> <profile @ compound> <debates @ conj> <and @ cc> <project @ compound> <discussions @ conj> <. @ punct>```
## Author

  **KV Aditya Srivatsa** (k.v.aditya@research.iiit.ac.in)
 
 If you have any queries, please do reach out. 

## License
Refer to the [LICENSE](https://github.com/kvadityasrivatsa/parsing-assisted-sentence-paraphrasing/blob/main/LICENSE) file for more details.

