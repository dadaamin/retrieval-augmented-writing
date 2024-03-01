# Backend (FastAPI / llama-index)

```sh
conda create -n raw python=3.12 pip
conda activate raw

pip install -r requirements.txt

# on macOS you may have to run this if you get "OMP Error #15: ..."
conda install nomkl
```

## Development

```sh
make run
```

Tools

```sh
make format
make lint
make test
```

Qdrant management

```sh
# Start
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant:latest

# List all collections
curl -X GET http://localhost:6333/collections

# Remove existing collection
curl -X DELETE http://localhost:6333/collections/<collection_name>
```
