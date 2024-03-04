# Backend (FastAPI / llama-index)

```sh
conda create -n raw python=3.12 pip
conda activate raw

pip install -r requirements.txt

# on macOS you may have to run this if you get "OMP Error #15: ..."
conda install nomkl
```

## Development

Start services.

```sh
# Run vector store
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant:latest

# Insert seed data
python -m raw.index create --data_path data/

# Run search API
export QDRANT_LOCATION=http://localhost:6333/
export QDRANT_COLLECTION=mtb_protocols
uvicorn raw.main:app --reload
```

Data management

```sh
# Updating data
python -m raw.index update --data_path data/

# Remove collection
python -m raw.index delete

# List all collections
curl -X GET http://localhost:6333/collections

# Remove existing collection
curl -X DELETE http://localhost:6333/collections/<collection_name>
```

## Development Tools

```sh
make format
make lint
make test
```
