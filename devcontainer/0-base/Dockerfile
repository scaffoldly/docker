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
ARG NPM_MAJOR=latest
ENV NPM_MAJOR=${NPM_MAJOR}

# Repositories
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable" > /etc/apt/sources.list.d/docker.list && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_${NODE_MAJOR}.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list

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

# Python Core Tooling
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python${PYTHON_MAJOR}.${PYTHON_MINOR} python${PYTHON_MAJOR}.${PYTHON_MINOR}-dev python${PYTHON_MAJOR}.${PYTHON_MINOR}-venv \
    && rm -rf /var/lib/apt/lists/*

# Default Versions
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_MAJOR}.${PYTHON_MINOR} 1

# Ruby Core Tooling
RUN sudo add-apt-repository ppa:instructure/ruby && \
    apt-get update && \
    apt-get install -y \
    ruby${RUBY_MAJOR}.${RUBY_MINOR} ruby${RUBY_MAJOR}.${RUBY_MINOR}-dev \
    && rm -rf /var/lib/apt/lists/*

# Node Tools
RUN npm install --global npm@${NPM_MAJOR} yarn nx

# Python Tools
RUN curl -fsSL https://bootstrap.pypa.io/get-pip.py | python
RUN pip install --no-cache-dir pipx supervisor supervisor_checks
ENV PATH="${PATH}:/root/.local/bin"

# Linuxbrew
ENV BREWHOME="/root"
ENV BREWPATH="${BREWHOME}/.linuxbrew"
ENV PATH="${PATH}:${BREWPATH}/bin:${BREWPATH}/sbin"
ENV XDG_CACHE_HOME="${BREWHOME}/.cache"
ENV BREWGIT="${BREWPATH}/Homebrew"
ENV HOMEBREW_NO_ANALYTICS=1
ENV HOMEBREW_NO_AUTO_UPDATE=1

RUN git clone https://github.com/Homebrew/brew.git --depth=1 ${BREWGIT}
RUN git -C ${BREWGIT} fetch --depth 1 origin tag ${HOMEBREW_MAJOR}.${HOMEBREW_MINOR}.${HOMEBREW_PATCH}
RUN git -C ${BREWGIT} checkout tags/${HOMEBREW_MAJOR}.${HOMEBREW_MINOR}.${HOMEBREW_PATCH}

RUN mkdir -p \
  ${BREWPATH}/bin \
  ${BREWPATH}/etc \
  ${BREWPATH}/include \
  ${BREWPATH}/lib \
  ${BREWPATH}/opt \
  ${BREWPATH}/sbin \
  ${BREWPATH}/share \
  ${BREWPATH}/var/homebrew/linked \
  ${BREWPATH}/Cellar \
  && ln -s ${BREWGIT}/bin/brew ${BREWPATH}/bin/brew

# Files
COPY root /root
COPY bin /bin
COPY etc /etc
COPY opt /opt
COPY usr /usr
COPY var /var
COPY ./_root /
