# Stage 1: Node and NPM setup
FROM ubuntu:22.04 as node-setup

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 20.10.0

# Install dependencies and Node.js
RUN mkdir -p /usr/local/nvm \
    && apt-get update  \
    && apt-get remove -y nodejs \
    && apt-get autoremove -y  \
    && rm -rf /var/lib/apt/lists/*
# Bundle app source and build application
RUN apt-get update \
    && apt-get install git -y\
    && apt-get install npm -y \
    && apt-get install -y python3 python3-pip \
    && apt install -y git \ 
    # && pip install --upgrade pip \
    && apt-get install wget --assume-yes \
    && wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm use $NODE_VERSION \
    && nvm alias default $NODE_VERSION \ 
    && node --version \
    && nvm --version  

FROM ubuntu:22.04 as python-env

# Install Python and dependencies
COPY requirements.txt /tmp/
RUN apt-get update && \
    apt install -y git && \
    apt-get install -y python3 python3-pip && \
    pip3 install -r /tmp/requirements.txt && \
    pip install auto-gptq && \    
    rm /tmp/requirements.txt


# Stage 3: Final image based on NVIDIA CUDA base
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

RUN useradd -m -u 1000 user
# Copy over the node_modules from the previous stage

COPY --from=node-setup /usr/local/nvm /usr/local/nvm

# Copy Python environment from python-env stage
COPY --from=python-env /usr/local /usr/local

# Set up environment variables for Node and Python
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 20.10.0
ENV NODE_PATH $NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

#Copy Homebrewery css dependencies
COPY dependencies /home/user/app


# Set working directory and user
WORKDIR /home/user/app

# Additional setup, must make .cache to bypass an exllama build bug, make sure user can access, then mk dir for app, and steps to install flash-attn which must be done AFTER everything else is built and in this stage to access CUDA
RUN mkdir -p /home/user/.cache && \  
    chmod 777 /home/user/.cache && \  
    apt-get update && \
    apt install -y git && \
    apt-get install -y python3-pip && \
    pip install flash-attn && \
    git clone -b experimentalCommandLineBrewProcess https://github.com/G-Ambatte/homebrewery.git && \
    cd homebrewery && \
    npm install && \
    chown -R user:user /home/user/app/ && \
    chown -R user:user /home/user/app/homebrewery 

   


USER user


# Set the entrypoint
EXPOSE 8000
ENTRYPOINT ["/usr/bin/python3", "main.py"]


