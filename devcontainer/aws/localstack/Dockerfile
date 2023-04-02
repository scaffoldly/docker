ARG BASE_IMAGE=jammy
FROM mcr.microsoft.com/devcontainers/base:${BASE_IMAGE}}

RUN apt-get update && \
    apt-get install -y \
    libsasl2-dev gcc \
    supervisor \
    nginx \
    python3.10 python3-venv python3-pip python3-dev \
    && pip install --no-cache-dir pipx supervisor supervisor_checks aiohttp aiodns fastapi "uvicorn[standard]" \
    && pipx install --include-deps localstack[full]==1.4 \
    && pipx install awscli-local \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Log Redirection
RUN mkdir -p /var/log/supervisor
RUN touch /var/log/supervisor/services.log
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

COPY etc /etc
COPY usr /usr
COPY start.sh /

# Health
EXPOSE 9000
# Localstack
EXPOSE 4566
# API Gateway Proxy (TODO Figure Out API Gateway IDs)
EXPOSE 8080
# CloudFront Proxy (TODO)
EXPOSE 3000

ENV TEST_AWS_ACCOUNT_ID="000000000000"
ENV DEFAULT_REGION="us-east-1"
ENV EDGE_BIND_HOST="0.0.0.0"
