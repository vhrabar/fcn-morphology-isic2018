FROM nvidia/cuda:13.0.0-cudnn-runtime-ubuntu24.04


ENV DEBIAN_FRONTEND=noninteractive


RUN apt update && apt install -y \
    python3 python3-pip python3-dev \
    git wget curl


WORKDIR /workspace


COPY requirements.txt /workspace/requirements.txt
RUN pip3 install --break-system-packages -r requirements.txt


COPY data/download_dataset.sh /workspace/data/download_dataset.sh
RUN chmod +x /workspace/data/download_dataset.sh
RUN bash /workspace/data/download_dataset.sh


COPY . /workspace


CMD ["bash"]