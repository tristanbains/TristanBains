# # Stage 1:
FROM node:18-bookworm-slim AS builder

WORKDIR /app

COPY package.json ./

# RUN npm install -g npm
RUN npm install

COPY . .

# Stage 2:
FROM python:3.11-slim 

RUN apt-get update && apt-get install -y gcc
# RUN apk add --no-cache gcc

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir \
    # && find /root/.local -follow -type f ( \
    #     -name '*.a' -name '*.txt' -name '*.md' -name '*.png' \
    #     -name '*.jpg' -name '*.jpeg' -name '*.js.map' -name '*.pyc' \
    #     -name '*.c' -name '*.pxc' -name '*.pyd' \
    # ) -delete \
    && find /usr/local/lib/python3.11 -name '__pycache__' | xargs rm -r

COPY . .

# COPY --from=builder /app/node_modules /app/node_modules
# COPY --from=builder package.json /app/package.json

EXPOSE 5000 8888