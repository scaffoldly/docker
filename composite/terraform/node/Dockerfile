ARG TERRAFORM_TAG=latest
ARG NODE_TAG=slim
FROM hashicorp/terraform:${TERRAFORM_TAG} as terraform

FROM node:${NODE_TAG}

# Smoke Test
RUN node --version
RUN npm --version
RUN yarn --version
RUN npx --version

COPY --from=terraform /bin/terraform /bin/terraform

RUN apt-get update && \
    apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Smoke Test
RUN terraform -version
