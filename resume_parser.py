from pypdf import PdfReader
from docx import Document


def extract_text(file):
    """Read a PDF or DOCX resume (a Streamlit uploaded file) and return its text."""
    if file.name.lower().endswith(".pdf"):
        # PDF: read every page and join the text
        return "\n".join(page.extract_text() or "" for page in PdfReader(file).pages)
    # DOCX: read every paragraph
    return "\n".join(p.text for p in Document(file).paragraphs)
