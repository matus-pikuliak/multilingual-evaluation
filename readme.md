# Installation

First build the docker image:

```
docker build . -t multieval
```

Then you can run it and the notebooks will work

```
docker run -p 8888:8888 -v %CD%:/labs -it multieval
```

# How to use this

Examples of visualizations are shown in `n_uriel` and `n_paper_bias` notebooks.