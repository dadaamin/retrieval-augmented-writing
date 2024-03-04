import argparse
import os
from pathlib import Path

from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient, QdrantClient, models


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


def load_documents(data_path):
    docs = SimpleDirectoryReader(data_path, filename_as_id=True).load_data()
    for doc in docs:
        doc.metadata["patient_id"] = Path(doc.metadata["file_name"]).stem
    return docs


def create_index(data_path):
    index = get_index()
    client = index.vector_store.client
    collection_name = index.vector_store.collection_name

    for doc in load_documents(data_path):
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


def update_index(index, data_path):
    index = get_index()
    docs = load_documents(data_path)
    updated = index.refresh_ref_docs(docs)
    for doc, is_new in zip(docs, updated):
        print(doc.get_doc_id(), f"Updated: {is_new}")


def delete_index(index):
    index = get_index()
    client = index.vector_store.client
    collection_name = index.vector_store.collection_name
    client.delete_collection(collection_name=collection_name)


def main(args):
    if args.command == "create":
        create_index(args.data_path)
    elif args.command == "update":
        update_index(args.data_path)
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
