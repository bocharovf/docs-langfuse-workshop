FROM python:3.12-slim AS builder

WORKDIR /workspace

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /workspace

RUN mkdocs build --clean \
    && python tools/check_images.py docs site

FROM nginx:alpine

COPY --from=builder /workspace/site /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
