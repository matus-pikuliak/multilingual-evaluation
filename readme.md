# Installation


# Average is not Enough: Caveats of Multilingual Evaluation

This is an accompanying repository to our paper _Average is not Enough: Caveats of Multilingual Evaluation_

## Colab demo

You can use this code in Google Colab. Demo is available [here](https://colab.research.google.com/drive/1UipA-_2ig6aZtcnqSjvmWD4gy5qOUF2t?usp=sharing)

## Local Installation

First build the docker image:

```
docker build . -t multilingual_evaluation
```

Then you can run it and the notebooks will work

```
docker run -p 8888:8888 -v ${PWD}:/labs -it multilingual_evaluation
```

Examples of visualizations are in the `n_figures.ipynb` notebook