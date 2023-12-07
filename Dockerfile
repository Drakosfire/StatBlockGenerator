# Start from the Alpin image used due to smallness
FROM nvidia/cuda:12.3.0-devel-ubuntu22.04

# Set the working directory
WORKDIR /usr/src/app

COPY package.json ./

RUN apt-get update \
    && apt-get install -y python3 python3-pip \
    && pip install --upgrade pip \
    && apt install -y git \    
    && apt-get install wget

RUN mkdir /usr/local/nvm
# nvm environment variables
ENV NVM_DIR /root/.nvm
ENV NODE_VERSION 20.10.0

# install nvm
# https://github.com/creationix/nvm#install-script

RUN wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm use $NODE_VERSION \
    && nvm alias default $NODE_VERSION

# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# confirm installation
RUN node -v
RUN npm -v

RUN export NODE_ENV=local

RUN npm install 

# Bundle app source and build application
COPY . .


RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 

RUN pip3 install -r requirements.txt 

RUN pip install auto-gptq

RUN pip install flash-attn

RUN pip install memory-profiler

EXPOSE 8000
# CMD ["Python3", "main.py"]



