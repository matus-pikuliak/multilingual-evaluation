FROM ubuntu:20.04 as base
RUN apt-get update && apt-get install -y curl && apt -y upgrade

# See http://bugs.python.org/issue19846
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    unzip \
    wget && rm -rf /var/lib/apt/lists/*

RUN pip3 --no-cache-dir install --upgrade \
    pip \
    setuptools

RUN pip3 install jupyterlab jupyter_http_over_ws

RUN jupyter serverextension enable --py jupyter_http_over_ws

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager
RUN jupyter lab build

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir -p /labs && chmod -R a+rwx /labs/
WORKDIR /labs
RUN mkdir /.local && chmod a+rwx /.local

RUN wget https://github.com/cldf-datasets/wals/archive/refs/tags/v2020.3.zip
RUN unzip v2020.3.zip

# jupyter
EXPOSE 8888

RUN python3 -m ipykernel.kernelspec

CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter lab --notebook-dir=/labs --ip 0.0.0.0 --no-browser --allow-root"]
