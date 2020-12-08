FROM ubuntu:20.04 as base
RUN apt-get update && apt-get install -y curl

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 --no-cache-dir install --upgrade \
    pip \
    setuptools

# Some TF tools expect a "python" binary
RUN ln -s $(which ${PYTHON}) /usr/local/bin/python

RUN pip3 install jupyter matplotlib
RUN pip3 install jupyter_http_over_ws
RUN pip3 install ipython==7.9.0
RUN jupyter serverextension enable --py jupyter_http_over_ws

RUN mkdir -p /labs && chmod -R a+rwx /labs/
WORKDIR /labs
RUN mkdir /.local && chmod a+rwx /.local

# jupyter
EXPOSE 8888
# tensorboard
EXPOSE 6006

RUN python3 -m ipykernel.kernelspec

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/labs --ip 0.0.0.0 --no-browser --allow-root"]
