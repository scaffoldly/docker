ARG BASE_IMAGE=jammy
FROM mcr.microsoft.com/devcontainers/base:${BASE_IMAGE}

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -

RUN apt-get update && \
    apt-get install -y \
    libsasl2-dev gcc \
    dnsmasq dnsutils \
    supervisor nginx \
    python3.10 python3-venv python3-pip python3-dev \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

RUN npm install --global nx cdktf-cli
RUN pip install --no-cache-dir pipx supervisor supervisor_checks aiohttp aiodns fastapi "uvicorn[standard]"
RUN pipx install awscli 
RUN pipx install awscliv2
RUN pipx install awscli-local 
RUN pipx install --include-deps localstack[full]==2.0

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

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
ENV POD_PATH="/var/lib/localstack/pod"

# AWS Env
ENV AWS_DEFAULT_REGION="us-east-1"
ENV AWS_ENDPOINT_URL="http://localhost:8080"
