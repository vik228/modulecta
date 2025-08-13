from typing import Optional

import fitz


class PDFProcessor:
    def __init__(self, pdf_path: str) -> None:
        self.pdf_path = pdf_path
        self.doc = fitz.open(pdf_path)

    def extract_text(self) -> str:
        text = ""
        for page in self.doc:
            text += page.get_text()
        return text
