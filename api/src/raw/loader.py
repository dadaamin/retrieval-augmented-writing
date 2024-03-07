from pathlib import Path
from typing import Dict, List, Optional

import fitz
import pytesseract
from fsspec import AbstractFileSystem
from llama_index.core.readers.base import BaseReader
from llama_index.core.readers.file.base import get_default_fs
from llama_index.core.schema import Document
from PIL import Image


class TesseractReader(BaseReader):
    """Docx parser."""

    # pylint: disable=W0221
    def load_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:
        fs = fs or get_default_fs()
        with fs.open(file, "rb") as fin:
            img = Image.open(fin)
            text = pytesseract.image_to_string(img, lang="deu")

        metadata = {"file_name": file.name}
        if extra_info is not None:
            metadata.update(extra_info)

        return [Document(text=text, metadata=metadata or {})]


class PDFReaderPlus(BaseReader):
    """
    PDF parser with a fallback to OCR (tesseract) if a page does not contain text.

    Based on:
    - PDFReader: llama_index.readers.file.docs.base.PDFReader https://github.com/run-llama/llama_index/blob/main/llama-index-integrations/readers/llama-index-readers-file/llama_index/readers/file/docs/base.py#L21
    - fitz: https://pymupdf.readthedocs.io/en/latest/installation.html
    - PyTesseract: https://pypi.org/project/pytesseract/
    """

    def __init__(
        self, return_full_document: Optional[bool] = False, language: str = "eng"
    ) -> None:
        self.return_full_document = return_full_document
        self.language = language

    def text_or_ocr(self, page):
        text = page.get_text()
        if len(text) == 0:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang=self.language)
        return text

    # pylint: disable=W0221
    def load_data(
        self,
        file: Path,
        extra_info: Optional[Dict] = None,
        fs: Optional[AbstractFileSystem] = None,
    ) -> List[Document]:

        fs = fs or get_default_fs()

        with fs.open(file, "rb") as fp:
            pdf = fitz.open(fp)
            num_pages = len(pdf)

            docs = []
            if self.return_full_document:
                text = ""
                metadata = {"file_name": fp.name}
                for page in range(num_pages):
                    text += self.text_or_ocr(pdf[page])
                docs.append(Document(text=text, metadata=metadata))

            else:
                for page in range(num_pages):
                    text = self.text_or_ocr(pdf[page])
                    page_label = str(page)

                    metadata = {"page_label": page_label, "file_name": fp.name}
                    if extra_info is not None:
                        metadata.update(extra_info)

                    docs.append(Document(text=text, metadata=metadata))

            return docs
