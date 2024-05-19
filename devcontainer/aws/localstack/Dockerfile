ARG BASE_IMAGE=jammy
FROM mcr.microsoft.com/devcontainers/base:${BASE_IMAGE}

ENV BASE_IMAGE=${BASE_IMAGE}
ARG NODE_MAJOR=20
ENV NODE_MAJOR=${NODE_MAJOR}
ARG JAVA_MAJOR=17
ENV JAVA_MAJOR=${JAVA_MAJOR}
ARG PYTHON_MAJOR=3
ENV PYTHON_MAJOR=${PYTHON_MAJOR}
ARG PYTHON_MINOR=10
ENV PYTHON_MINOR=${PYTHON_MINOR}
ARG LOCALSTACK_MAJOR=3
ENV LOCALSTACK_MAJOR=${LOCALSTACK_MAJOR}
ARG LOCALSTACK_MINOR=1
ENV LOCALSTACK_MINOR=${LOCALSTACK_MINOR}
ARG LOCALSTACK_PATCH=0
ENV LOCALSTACK_PATCH=${LOCALSTACK_PATCH}
ARG NPM_MAJOR=latest
ENV NPM_MAJOR=${NPM_MAJOR}

# Repositories
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable" > /etc/apt/sources.list.d/docker.list && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list \

# Nvidia Repository (Ref: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# Generic Tooling
RUN apt-get update && \
    apt-get install -y \
    docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-ce-rootless-extras docker-buildx-plugin \
    nvidia-container-toolkit \
    ca-certificates software-properties-common \
    libsasl2-dev libsnappy-dev \
    gcc g++ make \
    dnsmasq dnsutils netcat \
    supervisor nginx \
    nodejs \
    openjdk-${JAVA_MAJOR}-jdk openjdk-${JAVA_MAJOR}-jre \
    gh \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python${PYTHON_MAJOR}.${PYTHON_MINOR} python${PYTHON_MAJOR}.${PYTHON_MINOR}-dev python${PYTHON_MAJOR}.${PYTHON_MINOR}-venv \
    && rm -rf /var/lib/apt/lists/*

# Primary Versions
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_MAJOR}.${PYTHON_MINOR} 1

# Node Core Tooling
RUN npm install --global npm@${NPM_MAJOR} yarn nx
# Skipped: cdktf-cli

# Python Core Tooling
RUN curl -fsSL https://bootstrap.pypa.io/get-pip.py | python
RUN pip install --no-cache-dir pipx supervisor supervisor_checks amazon-kclpy
ENV PATH="${PATH}:/root/.local/bin"
RUN pipx install awscli 
RUN pipx install awscliv2
RUN pipx install awscli-local 
RUN pipx install --include-deps localstack[full]==${LOCALSTACK_MAJOR}.${LOCALSTACK_MINOR}.${LOCALSTACK_PATCH}

COPY root /root
COPY bin /bin
COPY etc /etc
COPY usr /usr

# Localstack Env
ENV ACTIVATE_PRO=0
ENV TEST_AWS_ACCOUNT_ID="000000000000"
ENV LOCALSTACK_PORT="4566"
ENV GATEWAY_LISTEN="0.0.0.0:${LOCALSTACK_PORT}"
ENV OVERRIDE_IN_DOCKER=1

# AWS Env
ENV AWS_SDK_JS_SUPPRESS_MAINTENANCE_MODE_MESSAGE=1

# Runtime Env
ENV STAGE="local"
ENV LOCALSTACK="true"
# ENV POD_PATH="/var/lib/localstack/pod"