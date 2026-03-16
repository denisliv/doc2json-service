FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libgomp1 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# paddlex 3.4.1 uses deprecated langchain import paths that break with langchain-core 0.3.x
RUN find /usr/local/lib -name "base.py" \
    -path "*/paddlex/inference/pipelines/components/retriever/*" \
    -exec sed -i \
      -e 's/from langchain\.docstore\.document import Document/from langchain_core.documents import Document/g' \
      -e 's/from langchain\.text_splitter import RecursiveCharacterTextSplitter/from langchain_text_splitters import RecursiveCharacterTextSplitter/g' \
      {} + || true

COPY . .

RUN mkdir -p /app/storage /app/plugins

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
