FROM python:3.13-slim

RUN adduser --system --no-create-home reverse-abl

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/ src/

RUN pip install --no-cache-dir . && rm -rf /root/.cache

USER reverse-abl

ENTRYPOINT ["reverse-abliterate"]
CMD ["--help"]
