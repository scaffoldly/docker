FROM mcr.microsoft.com/devcontainers/base:jammy

ENV NODE_MAJOR=18
ENV JAVA_MAJOR=17
ENV PYTHON_MAJOR=3
ENV PYTHON_MINOR=11
ENV LOCALSTACK_MAJOR=2
ENV LOCALSTACK_MINOR=3
ENV LOCALSTACK_PATCH=2

# Generic Tooling
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    curl -fsSL https://get.docker.com | bash - && \
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
    apt-get install -y \
    python${PYTHON_MAJOR}.${PYTHON_MINOR} python${PYTHON_MAJOR}.${PYTHON_MINOR}-dev python${PYTHON_MAJOR}.${PYTHON_MINOR}-venv \
    && rm -rf /var/lib/apt/lists/*

# Primary Versions
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_MAJOR}.${PYTHON_MINOR} 1

# Node Core Tooling
RUN npm install --global npm yarn nx cdktf-cli

# Python Core Tooling
RUN curl -fsSL https://bootstrap.pypa.io/get-pip.py | python
RUN pip install --no-cache-dir pipx supervisor supervisor_checks amazon-kclpy
ENV PATH="${PATH}:/root/.local/bin"
RUN pipx install awscli 
RUN pipx install awscliv2
RUN pipx install awscli-local 
RUN pipx install --include-deps localstack[full]==${LOCALSTACK_MAJOR}.${LOCALSTACK_MINOR}.${LOCALSTACK_PATCH}

# Log Redirection
RUN mkdir -p /var/log/supervisor
RUN touch /var/log/supervisor/services.log
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

COPY bin /bin
COPY etc /etc
COPY usr /usr

# Localstack Proxy
EXPOSE 8080

# Localstack Env
ENV ACTIVATE_PRO=0
ENV TEST_AWS_ACCOUNT_ID="000000000000"
ENV GATEWAY_LISTEN="0.0.0.0:4566"
ENV OVERRIDE_IN_DOCKER=1

# AWS Env
ENV AWS_ENDPOINT_URL="http://localhost.localstack.cloud:4566"
ENV AWS_DEFAULT_REGION="us-east-1"
ENV AWS_ACCESS_KEY_ID=test
ENV AWS_SECRET_ACCESS_KEY=test
ENV AWS_SDK_JS_SUPPRESS_MAINTENANCE_MODE_MESSAGE=1

# Runtime Env
ENV STAGE="local"
ENV LOCALSTACK="true"
# ENV POD_PATH="/var/lib/localstack/pod"
