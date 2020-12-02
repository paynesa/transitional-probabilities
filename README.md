# Statistical Learning via Transitional Probabilities

## Overview 
This code provides two slightly different implementations of statistical learning via transitional 
probabilities as originally proposed by <a href="https://pzacad.pitzer.edu/~dmoore/1996_Saffran,%20Aslin,%20Newport_Stat'l%20Learning%20at%208%20mos_Science.pdf"> Saffran, Aslin, and Newport (1996) </a> 
and modelled computationally by <a href="https://www.ling.upenn.edu/~ycharles/papers/quick.pdf">Yang and Gambell (2005) </a>. 

The transitional probabilities of two syllables `AB` is given by: `TP(AB) = freq(AB)/freq(A)`. Both models 
provided here calculate these probabilities and then apply them to the input data in an attempt to segment it into 
words. Precision, recall, and f-score are then reported by comparing the input data to the learner's proposed segmentation
on a per-utterance basis. I provide both the SLM as modelled by Yang and Gambell, and a slightly modified version wherein 
prediction of word boundaries is carried out separately for each utterance. 

## Running the Code
`run_slm.py` provides the traditional implementation of the SLM model using transitional 
probabilities as specified in Yang and Gambell (2005). 

`separate_utterance_slm.py`  provides a slightly modified version of the Yang and Gambell model 
that predicts word boundaries separately for each utterance rather than predicting over the entire data and 
then evaluating each utterance separately. 

Both models take in the following parameters: 

```positional arguments:
  path                  path of the file to perform SLM learning on

optional arguments:
  -h, --help            show this help message and exit
  -boundary {W,S}       boundary of interest (default=W)
  -keep_accents         keep accents when calculating TPs (default=ignore accents)
```
Finally, `mother.speech.txt` provides the annotated CHILDES data used by Yang and Gambell (2005) and provided
courtesy of Charles Yang. To replicate Yang and Gambell (2005), run `python3 run_slm.py mother.speech.txt`. 