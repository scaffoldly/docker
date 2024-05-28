ARG BASE_IMAGE=nodejs
ARG NODE_MAJOR=20

FROM public.ecr.aws/lambda/${BASE_IMAGE}:${NODE_MAJOR}

ENV BASE_IMAGE=${BASE_IMAGE}
ENV NODE_MAJOR=${NODE_MAJOR}
ARG NEXT_MAJOR=14
ENV NEXT_MAJOR=${NEXT_MAJOR}

WORKDIR /opt

RUN npm install -g --prefix . next@${NEXT_MAJOR}

RUN node --version
RUN next --version
