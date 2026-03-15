FROM node:22-slim AS builder

ENV PNPM_HOME="/pnpm" \
    PATH="/pnpm:$PATH"

RUN corepack enable

WORKDIR /app

COPY package.json pnpm-lock.yaml* pnpm-workspace.yaml* ./
RUN pnpm install --frozen-lockfile

COPY . .

ARG NUXT_PUBLIC_WS_URL
ENV NUXT_PUBLIC_WS_URL=${NUXT_PUBLIC_WS_URL}

RUN pnpm build


FROM node:22-slim

WORKDIR /app

COPY --from=builder /app/.output ./

EXPOSE 3000

CMD ["node", "server/index.mjs"]
