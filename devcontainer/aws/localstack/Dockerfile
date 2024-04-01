ARG BASE_IMAGE=jammy
ARG JAVA_MAJOR=17
ARG PYTHON_MAJOR=3
ARG PYTHON_MINOR=10
ARG LOCALSTACK_MAJOR=3
ARG LOCALSTACK_MINOR=1
ARG LOCALSTACK_PATCH=0

### Calculate package sums for conditional cache busting
FROM mcr.microsoft.com/devcontainers/base:${BASE_IMAGE} as pkgsum

RUN apt-get update && \
    apt-get upgrade && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get install -y \
            debsums \
    && rm -rf /var/lib/apt/lists/*

RUN debsums --silent --all --generate=missing

# Setup cache busting
RUN cat /var/lib/dpkg/info/*.md5sums | sha256sum | cut -d' ' -f1 > /var/lib/dpkg/sha256sum

### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###
### The actual devcontainer starts here... ###
### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ###
FROM mcr.microsoft.com/devcontainers/base:${BASE_IMAGE}

# Cache busting on OS package upgrades
COPY --from=pkgsum /var/lib/dpkg/sha256sum /var/lib/dpkg/sha256sum

# OS Update
RUN apt-get update && \
    apt-get upgrade && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get install -y \
            debsums \
    && rm -rf /var/lib/apt/lists/*

ENV NODE_MAJOR=${NODE_MAJOR}
ENV JAVA_MAJOR=${JAVA_MAJOR}
ENV PYTHON_MAJOR=${PYTHON_MAJOR}
ENV PYTHON_MINOR=${PYTHON_MINOR}
ENV LOCALSTACK_MAJOR=${LOCALSTACK_MAJOR}
ENV LOCALSTACK_MINOR=${LOCALSTACK_MINOR}
ENV LOCALSTACK_PATCH=${LOCALSTACK_PATCH}

# Generic Tooling
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    curl -fsSL https://get.docker.com | bash - && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get install -y \
            ca-certificates software-properties-common \
            libsasl2-dev libsnappy-dev \
            gcc g++ make \
            dnsmasq dnsutils \
            supervisor nginx \
            nodejs \
            openjdk-${JAVA_MAJOR}-jdk openjdk-${JAVA_MAJOR}-jre \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get install -y \
            python${PYTHON_MAJOR}.${PYTHON_MINOR} \
            python${PYTHON_MAJOR}.${PYTHON_MINOR}-dev \
            python${PYTHON_MAJOR}.${PYTHON_MINOR}-venv \
    && rm -rf /var/lib/apt/lists/*

# Primary Versions
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_MAJOR}.${PYTHON_MINOR} 1

# Node Core Tooling
RUN npm install --global \
    npm \
    yarn \
    nx \
    prettier \
    eslint \
    typescript

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
ENV GATEWAY_LISTEN="0.0.0.0:4566"
ENV LOCALSTACK_ENDPOINT="http://localhost.localstack.cloud:4566"
ENV OVERRIDE_IN_DOCKER=1

# AWS Env
ENV AWS_SDK_JS_SUPPRESS_MAINTENANCE_MODE_MESSAGE=1

# Runtime Env
ENV STAGE="local"
ENV LOCALSTACK="true"
# ENV POD_PATH="/var/lib/localstack/pod"
