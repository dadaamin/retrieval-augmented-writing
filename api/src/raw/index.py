import argparse
from pathlib import Path

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient, models


class Index:
    def __init__(self, qdrant_location: str, qdrant_collection: str):
        node_parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=32)
        Settings.embed_model = "local:BAAI/bge-small-en-v1.5"
        Settings.node_parser = node_parser

        client = QdrantClient(qdrant_location)
        vector_store = QdrantVectorStore(
            collection_name=qdrant_collection,
            client=client,
        )

        if Path('./storage').exists():
            # When using an external vectorDB, it is necessary to explicitly persist the document store to support updating: https://github.com/run-llama/llama_index/issues/8832
            storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir="./storage")
            index = load_index_from_storage(storage_context)
        else:
            index = VectorStoreIndex.from_vector_store(
                vector_store=vector_store,
            )


        self.client = client
        self.index = index
        self.collection_name = qdrant_collection

    def load_documents(self, data_path):
        docs = SimpleDirectoryReader(data_path, filename_as_id=True).load_data()
        for doc in docs:
            doc.metadata["patient_id"] = Path(doc.metadata["file_name"]).stem
        return docs

    def create_index(self, data_path):
        for doc in self.load_documents(data_path):
            self.index.insert(doc)
            print(doc.get_doc_id())

        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="metadata.patient_id",
            field_type=models.PayloadSchemaType.KEYWORD,
        )

        self.client.update_collection(
            collection_name=self.collection_name,
            hnsw_config=models.HnswConfigDiff(payload_m=16, m=0),
        )

        self.index.storage_context.persist(persist_dir="./storage")

    def update_index(self, data_path):
        docs = self.load_documents(data_path)
        updated = self.index.refresh_ref_docs(docs)
        for doc, is_new in zip(docs, updated):
            print(doc.get_doc_id(), f"Updated: {is_new}")

    def delete_index(self):
        self.client.delete_collection(collection_name=self.collection_name)


def main(args):
    index = Index(args.qdrant_location, args.qdrant_collection)

    if args.command == "create":
        index.create_index(args.data_path)
    elif args.command == "update":
        index.update_index(args.data_path)
    elif args.command == "delete":
        index.delete_index()
    else:
        raise ValueError(f"Invalid command {args.command}")


def arg_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "command",
        help="What operation to do on the index.",
        choices=['create', 'update', 'delete']
    )
    parser.add_argument(
        "--qdrant_location",
        default="http://localhost:6333/",
        help="Qdrant url.",
        required=False
    )
    parser.add_argument(
        "--qdrant_collection",
        help="Name of Qdrant collection",
        default="mtb_protocols",
        required=False
    )
    parser.add_argument(
        "--data_path",
        default="data/",
        help="Where to read documents from (pdf, txt, ...).",
        required=False
    )
    return parser.parse_args()


if __name__ == "__main__":
    main(arg_parser())
