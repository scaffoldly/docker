ARG NODE_MAJOR=20

FROM public.ecr.aws/lambda/nodejs:${NODE_MAJOR}

ARG NEXT_MAJOR=14
ENV NODE_MAJOR=${NODE_MAJOR}
ENV NEXT_MAJOR=${NEXT_MAJOR}

WORKDIR /opt

RUN npm install -g --prefix . next@${NEXT_MAJOR}

RUN node --version
RUN next --version
