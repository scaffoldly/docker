FROM public.ecr.aws/lambda/provided:al2023

ARG NODE_MAJOR=20
ENV NODE_MAJOR=${NODE_MAJOR}
ARG NEXT_MAJOR=14
ENV NEXT_MAJOR=${NEXT_MAJOR}

WORKDIR /opt

ENV PATH="/opt/nodejs/bin:${PATH}"

RUN dnf install -y tar xz jq

RUN NODE_EXACT_VERSION=$(curl -s https://nodejs.org/dist/index.json | jq -r --arg MAJOR_VERSION "$NODE_MAJOR" '[.[] | select(.version | startswith("v" + $MAJOR_VERSION + "."))][0].version') && \
    ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        ARCH="x64"; \
    elif [ "$ARCH" = "aarch64" ]; then \
        ARCH="arm64"; \
    else \
        echo "Unsupported architecture: $ARCH"; exit 1; \
    fi && \
    NODE_FILENAME="node-${NODE_EXACT_VERSION}-linux-${ARCH}" && \
    curl -O "https://nodejs.org/dist/${NODE_EXACT_VERSION}/${NODE_FILENAME}.tar.xz" && \
    tar -xvf "${NODE_FILENAME}.tar.xz" && \
    rm "${NODE_FILENAME}.tar.xz" && \
    mv "${NODE_FILENAME}" nodejs && \
    npm install -g next@${NEXT_MAJOR}

RUN node --version
RUN next --version
