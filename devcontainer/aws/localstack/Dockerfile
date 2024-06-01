ARG BASE_IMAGE=jammy
FROM ubuntu:${BASE_IMAGE} as ensure-bins

RUN apt-get update && \
    apt-get install -y curl

RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        curl -sfL https://github.com/devcontainers-contrib/nanolayer/releases/download/v0.5.6/nanolayer-x86_64-unknown-linux-gnu.tgz | tar fxvz - -C /bin; \
    elif [ "$ARCH" = "aarch64" ]; then \
        curl -sfL https://github.com/devcontainers-contrib/nanolayer/releases/download/v0.5.6/nanolayer-aarch64-unknown-linux-gnu.tgz | tar fxvz - -C /bin; \
    else \
        echo "Unsupported architecture: $ARCH" && exit 1; \
    fi && \
    chmod +x /bin/nanolayer

FROM ubuntu:${BASE_IMAGE}

ENV BASE_IMAGE=${BASE_IMAGE}
ARG NODE_MAJOR=20
ENV NODE_MAJOR=${NODE_MAJOR}
ARG JAVA_MAJOR=17
ENV JAVA_MAJOR=${JAVA_MAJOR}
ARG PYTHON_MAJOR=3
ENV PYTHON_MAJOR=${PYTHON_MAJOR}
ARG PYTHON_MINOR=10
ENV PYTHON_MINOR=${PYTHON_MINOR}
ARG RUBY_MAJOR=3
ENV RUBY_MAJOR=${RUBY_MAJOR}
ARG RUBY_MINOR=1
ENV RUBY_MINOR=${RUBY_MINOR}
ARG HOMEBREW_MAJOR=4
ENV HOMEBREW_MAJOR=${HOMEBREW_MAJOR}
ARG HOMEBREW_MINOR=3
ENV HOMEBREW_MINOR=${HOMEBREW_MINOR}
ARG HOMEBREW_PATCH=0
ENV HOMEBREW_PATCH=${HOMEBREW_PATCH}
ARG LOCALSTACK_MAJOR=3
ENV LOCALSTACK_MAJOR=${LOCALSTACK_MAJOR}
ARG LOCALSTACK_MINOR=1
ENV LOCALSTACK_MINOR=${LOCALSTACK_MINOR}
ARG LOCALSTACK_PATCH=0
ENV LOCALSTACK_PATCH=${LOCALSTACK_PATCH}
ARG NPM_MAJOR=latest
ENV NPM_MAJOR=${NPM_MAJOR}

COPY --from=ensure-bins /bin/nanolayer /bin/nanolayer

RUN nanolayer install apt "ca-certificates curl gpg lsb-release"

# Repositories
RUN curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xF23C5A6CF475977595C89F51BA6932366A755776" | gpg --dearmor -o /etc/apt/keyrings/deadsnakes-ppa.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/deadsnakes-ppa.gpg] http://ppa.launchpad.net/deadsnakes/ppa/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/deadsnakes-ppa.list && \
    curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x9AB211A0296344E1A83AEFF0A579DF7F2B1186ED" | gpg --dearmor -o /etc/apt/keyrings/instructure-ruby.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/instructure-ruby.gpg] http://ppa.launchpad.net/instructure/ruby/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/instructure-ruby.list && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list

RUN nanolayer install apt "supervisor dnsutils netcat-openbsd"
RUN nanolayer install apt "docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-ce-rootless-extras docker-buildx-plugin"
RUN nanolayer install apt "libsasl2-dev libsnappy-dev"
RUN nanolayer install apt "nodejs"
RUN nanolayer install apt "python${PYTHON_MAJOR}.${PYTHON_MINOR} python${PYTHON_MAJOR}.${PYTHON_MINOR}-dev python${PYTHON_MAJOR}.${PYTHON_MINOR}-venv"
RUN nanolayer install apt "openjdk-${JAVA_MAJOR}-jdk openjdk-${JAVA_MAJOR}-jre"
RUN nanolayer install apt "ruby${RUBY_MAJOR}.${RUBY_MINOR} ruby${RUBY_MAJOR}.${RUBY_MINOR}-dev"

# # Nvidia Repository (Ref: https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
# RUN curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
#     && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
#     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
#     sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

# # Generic Tooling
# RUN apt-get update && \
#     apt-get install -y \
#     docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-ce-rootless-extras docker-buildx-plugin \
#     nvidia-container-toolkit \
#     ca-certificates software-properties-common \
#     libsasl2-dev libsnappy-dev \
#     gcc g++ make \
#     dnsmasq dnsutils netcat \
#     supervisor nginx \
#     nodejs \
#     openjdk-${JAVA_MAJOR}-jdk openjdk-${JAVA_MAJOR}-jre \
#     gh \
#     && rm -rf /var/lib/apt/lists/*

# # Python Core Tooling
# RUN add-apt-repository ppa:deadsnakes/ppa && \
#     apt-get update && \
#     apt-get install -y \
#     python${PYTHON_MAJOR}.${PYTHON_MINOR} python${PYTHON_MAJOR}.${PYTHON_MINOR}-dev python${PYTHON_MAJOR}.${PYTHON_MINOR}-venv \
#     && rm -rf /var/lib/apt/lists/*

# # Default Versions
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_MAJOR}.${PYTHON_MINOR} 1

# # Ruby Core Tooling
# RUN sudo add-apt-repository ppa:instructure/ruby && \
#     apt-get update && \
#     apt-get install -y \
#     ruby${RUBY_MAJOR}.${RUBY_MINOR} ruby${RUBY_MAJOR}.${RUBY_MINOR}-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Node Tools
# RUN npm install --global npm@${NPM_MAJOR} yarn nx
# # Skipped: cdktf-cli

# # Python Tools
# RUN curl -fsSL https://bootstrap.pypa.io/get-pip.py | python
# RUN pip install --no-cache-dir pipx supervisor supervisor_checks amazon-kclpy
# ENV PATH="${PATH}:/root/.local/bin"

# # Linuxbrew
# ENV BREWHOME="/root"
# ENV BREWPATH="${BREWHOME}/.linuxbrew"
# ENV PATH="${PATH}:${BREWPATH}/bin:${BREWPATH}/sbin"
# ENV XDG_CACHE_HOME="${BREWHOME}/.cache"
# ENV BREWGIT="${BREWPATH}/Homebrew"
# ENV HOMEBREW_NO_ANALYTICS=1
# ENV HOMEBREW_NO_AUTO_UPDATE=1

# RUN git clone https://github.com/Homebrew/brew.git --depth=1 ${BREWGIT}
# RUN git -C ${BREWGIT} fetch --depth 1 origin tag ${HOMEBREW_MAJOR}.${HOMEBREW_MINOR}.${HOMEBREW_PATCH}
# RUN git -C ${BREWGIT} checkout tags/${HOMEBREW_MAJOR}.${HOMEBREW_MINOR}.${HOMEBREW_PATCH}

# RUN mkdir -p \
#   ${BREWPATH}/bin \
#   ${BREWPATH}/etc \
#   ${BREWPATH}/include \
#   ${BREWPATH}/lib \
#   ${BREWPATH}/opt \
#   ${BREWPATH}/sbin \
#   ${BREWPATH}/share \
#   ${BREWPATH}/var/homebrew/linked \
#   ${BREWPATH}/Cellar \
#   && ln -s ${BREWGIT}/bin/brew ${BREWPATH}/bin/brew

# # RUN HOMEBREW_NO_ANALYTICS=1 HOMEBREW_NO_AUTO_UPDATE=1 brew tap --force homebrew/core \
# #   && gem install bundler -n /usr/bin \
# #   && brew install-bundler-gems --groups=all \
# #   && brew cleanup \
# #   && rm -rf ${XDG_CACHE_HOME}
# # WORKDIR /

# # AWS
# RUN pipx install awscli
# RUN pipx install awscliv2
# RUN pipx install awscli-local

# # Localstack
# RUN pipx install --include-deps localstack[full]==${LOCALSTACK_MAJOR}.${LOCALSTACK_MINOR}.${LOCALSTACK_PATCH}

# COPY root /root
# COPY bin /bin
# COPY etc /etc
# COPY opt /opt
# COPY usr /usr
# COPY var /var

# # Localstack Env
# ENV ACTIVATE_PRO=0
# ENV TEST_AWS_ACCOUNT_ID="000000000000"
# ENV LOCALSTACK_PORT="4566"
# ENV GATEWAY_LISTEN="0.0.0.0:${LOCALSTACK_PORT}"
# ENV OVERRIDE_IN_DOCKER=1

# # AWS Env
# ENV AWS_SDK_JS_SUPPRESS_MAINTENANCE_MODE_MESSAGE=1

# # Lambda Env
# ENV PATH="/var/runtime:/var/task:/var/task/node_modules/.bin:${PATH}"
# RUN ARCH=$(uname -m) && \
#     if [ "$ARCH" = "x86_64" ]; then \
#         curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.19/aws-lambda-rie; \
#     elif [ "$ARCH" = "aarch64" ]; then \
#         curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/download/v1.19/aws-lambda-rie-arm64; \
#     else \
#         echo "Unsupported architecture: $ARCH" && exit 1; \
#     fi && \
#     chmod +x /usr/local/bin/aws-lambda-rie

# # Runtime Env
# ENV STAGE="local"
# ENV LOCALSTACK="true"
# # ENV POD_PATH="/var/lib/localstack/pod"

# # Root FS
# COPY ./_root /
