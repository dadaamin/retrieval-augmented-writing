# Backend (FastAPI / llama-index)

```sh
conda env update -f environment.yml
conda activate raw

pip install -r requirements-dev.txt
pip install -e .

# on macOS you may have to run this if you get "OMP Error #15: ..."
conda install nomkl
```

You will also need tesseract for indexing of documents (scans and PDFs with no text). For https://tesseract-ocr.github.io/tessdoc/Installation.html

```sh
brew install tesseract
```

## Development

Start services.

```sh
# Run vector store
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant:latest

# Configure URLs
# when changing these urls, please also change the urls in api/raw/main.py
export QDRANT_LOCATION=http://localhost:6333/
export QDRANT_COLLECTION=mtb_protocols
export OLLAMA_BASE_URL=https://mirage.kite.ume.de/ollama

# Insert seed data
python -m raw.engine create --data_path data/

# Run search API
uvicorn raw.main:app --reload
```

Data management. Can also manage collections in Qdrant dashboard: http://localhost:6333/dashboard#/

```sh
# Updating data
python -m raw.engine update --data_path data/

# Remove collection
python -m raw.engine delete
```

## Development Tools

```sh
make format
make lint
make test
```
