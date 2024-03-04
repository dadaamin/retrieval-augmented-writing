from llama_index.core import Settings
from llama_index.core.node_parser import SimpleNodeParser

from raw.ollama import Ollama
from raw.index import get_index


def init_settings():
    Settings.llm = Ollama(
        model="mixtral:latest",
        base_url="https://mirage.kite.ume.de/ollama",
        request_timeout=240,
        temperature=0,
    )

    node_parser = SimpleNodeParser.from_defaults(chunk_size=512, chunk_overlap=32)
    Settings.embed_model = "local:BAAI/bge-small-en-v1.5"
    Settings.node_parser = node_parser


def get_llm():
    return Settings.llm


def get_chat_engine():
    return get_index().as_chat_engine(
        similarity_top_k=3, chat_mode="condense_plus_context", use_async=True
    )
