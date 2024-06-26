ARG BASE_IMAGE=ghcr.io/scaffoldly/base:latest
FROM ${BASE_IMAGE}

ENV BASE_IMAGE=${BASE_IMAGE}
ARG LOCALSTACK_MAJOR=3
ENV LOCALSTACK_MAJOR=${LOCALSTACK_MAJOR}
ARG LOCALSTACK_MINOR=1
ENV LOCALSTACK_MINOR=${LOCALSTACK_MINOR}
ARG LOCALSTACK_PATCH=0
ENV LOCALSTACK_PATCH=${LOCALSTACK_PATCH}

# AWS
RUN pip install --no-cache-dir amazon-kclpy
RUN pipx install awscli
RUN pipx install awscliv2
RUN pipx install awscli-local

# Localstack
RUN pipx install --include-deps localstack[full]==${LOCALSTACK_MAJOR}.${LOCALSTACK_MINOR}.${LOCALSTACK_PATCH}

COPY root /root
COPY bin /bin
COPY etc /etc
COPY opt /opt
COPY usr /usr
COPY var /var
COPY ./_root /

# Docker Env
ENV DOCKER_BUILDKIT=1

# Localstack Env
ENV ACTIVATE_PRO=0
ENV TEST_AWS_ACCOUNT_ID="000000000000"
ENV LOCALSTACK_PORT="4566"
ENV GATEWAY_LISTEN="0.0.0.0:${LOCALSTACK_PORT}"
ENV OVERRIDE_IN_DOCKER=1

# AWS Env
ENV AWS_SDK_JS_SUPPRESS_MAINTENANCE_MODE_MESSAGE=1

# Lambda Env
ENV PATH="/var/runtime:/var/task:/var/task/node_modules/.bin:${PATH}"
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.19/aws-lambda-rie; \
    elif [ "$ARCH" = "aarch64" ]; then \
        curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.19/aws-lambda-rie-arm64; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    chmod +x /usr/local/bin/aws-lambda-rie

# Runtime Env
ENV STAGE="local"
ENV LOCALSTACK="true"
# ENV POD_PATH="/var/lib/localstack/pod"