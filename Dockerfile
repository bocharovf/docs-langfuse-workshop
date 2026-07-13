FROM python:3.12-slim

WORKDIR /workspace

RUN python -m pip install --upgrade pip \
    && pip install mkdocs mkdocs-glightbox

CMD ["sh", "-lc", "mkdocs serve -a 0.0.0.0:8000"]
