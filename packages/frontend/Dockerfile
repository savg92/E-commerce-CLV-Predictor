FROM oven/bun:1 AS builder
WORKDIR /app
COPY packages/frontend/package.json .
COPY bun.lock .
RUN bun install
COPY packages/frontend/src ./src
COPY packages/frontend/index.html .
COPY packages/frontend/tsconfig.json .
COPY packages/frontend/vite.config.ts .
RUN bun run build

FROM nginx:alpine AS runner
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
