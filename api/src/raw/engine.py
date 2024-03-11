import argparse
import os
from pathlib import Path
from typing import List

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import Document
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient, QdrantClient, models

from raw.ollama import Ollama


def get_index():
    vector_store = QdrantVectorStore(
        collection_name=os.environ["QDRANT_COLLECTION"],
        client=QdrantClient(os.environ["QDRANT_LOCATION"]),
        aclient=AsyncQdrantClient(os.environ["QDRANT_LOCATION"]),
    )

    if Path("./storage").exists():
        # This is necessary to support updating: https://github.com/run-llama/llama_index/issues/8832
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store, persist_dir="./storage"
        )
        index = load_index_from_storage(storage_context)
    else:
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
        )

    return index


def init_settings():
    Settings.llm = Ollama(
        model="mixtral:latest",
        base_url=os.environ["OLLAMA_BASE_URL"],
        request_timeout=240,
        temperature=0,
    )

    node_parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=32)
    Settings.embed_model = "local:BAAI/bge-small-en-v1.5"
    Settings.node_parser = node_parser


def get_llm():
    return Settings.llm


def load_documents(data_path) -> List[Document]:
    docs = SimpleDirectoryReader(data_path, filename_as_id=True).load_data()
    for doc in docs:
        doc.metadata["patient_id"] = Path(doc.metadata["file_name"]).stem
    return docs


def create_index(documents: List[Document]):
    index = get_index()
    client = index.vector_store.client
    collection_name = index.vector_store.collection_name

    for doc in documents:
        index.insert(doc)
        print(doc.get_doc_id())

    index.vector_store.client.create_payload_index(
        collection_name=collection_name,
        field_name="metadata.patient_id",
        field_type=models.PayloadSchemaType.KEYWORD,
    )

    client.update_collection(
        collection_name=collection_name,
        hnsw_config=models.HnswConfigDiff(payload_m=16, m=0),
    )

    index.storage_context.persist(persist_dir="./storage")


def update_index(documents: List[Document]):
    index = get_index()
    updated = index.refresh_ref_docs(documents)
    for doc, is_new in zip(documents, updated):
        print(doc.get_doc_id(), f"Updated: {is_new}")
    index.storage_context.persist(persist_dir="./storage")


def delete_index():
    index = get_index()
    client = index.vector_store.client
    collection_name = index.vector_store.collection_name
    client.delete_collection(collection_name=collection_name)


def main(args):
    init_settings()

    if args.command == "create":
        documents = load_documents(args.data_path)
        create_index(documents)
    elif args.command == "update":
        documents = load_documents(args.data_path)
        update_index(documents)
    elif args.command == "delete":
        delete_index()
    else:
        raise ValueError(f"Invalid command {args.command}")


def arg_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "command",
        help="What operation to do on the index.",
        choices=["create", "update", "delete"],
    )
    parser.add_argument(
        "--data_path",
        default="data/",
        help="Where to read documents from (pdf, txt, ...).",
        required=False,
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(arg_parser())
