ARG BASE_IMAGE=jammy
FROM mcr.microsoft.com/devcontainers/base:${BASE_IMAGE}

ENV NODE_MAJOR=16

ENV LOCALSTACK_MAJOR=2
ENV LOCALSTACK_MINOR=2

ENV PYTHON_MAJOR=3
ENV PYTHON_MINOR=10

# Generic Tooling
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    curl -fsSL https://get.docker.com | bash - && \
    apt-get install -y \
    libsasl2-dev gcc \
    dnsmasq dnsutils \
    supervisor nginx \
    python${PYTHON_MAJOR}.${PYTHON_MINOR} python${PYTHON_MAJOR}-venv python${PYTHON_MAJOR}-pip python${PYTHON_MAJOR}-dev \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN npm install --global nx cdktf-cli yarn
RUN pip install --no-cache-dir pipx supervisor supervisor_checks aiohttp aiodns fastapi "uvicorn[standard]"
RUN pipx install awscli 
RUN pipx install awscliv2
RUN pipx install awscli-local 
RUN pipx install --include-deps localstack[full]==${LOCALSTACK_MAJOR}.${LOCALSTACK_MINOR}

RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_MAJOR}.${PYTHON_MINOR} 1

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
ENV GATEWAY_LISTEN="0.0.0.0"

# AWS Env
ENV AWS_DEFAULT_REGION="us-east-1"
ENV AWS_ENDPOINT_URL="http://localhost:4566"

# Runtime Env
ENV STAGE="local"
ENV LOCALSTACK="true"
ENV POD_PATH="/var/lib/localstack/pod"
