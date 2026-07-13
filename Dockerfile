FROM python:3.12-slim AS builder

WORKDIR /workspace

RUN python -m pip install --upgrade pip \
    && pip install mkdocs mkdocs-glightbox

COPY . /workspace

RUN mkdocs build --clean

FROM nginx:alpine

COPY --from=builder /workspace/site /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
