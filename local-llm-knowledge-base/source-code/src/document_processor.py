import os
import pdfplumber
from docx import Document
import markdown
from config.config import config
from src.utils import clean_text, get_file_extension

class DocumentProcessor:
    def __init__(self):
        self.supported_extensions = ['.txt', '.md', '.pdf', '.docx']
    
    def load_document(self, file_path: str) -> str:
        ext = get_file_extension(file_path)
        if ext == '.txt':
            return self._load_txt(file_path)
        elif ext == '.md':
            return self._load_md(file_path)
        elif ext == '.pdf':
            return self._load_pdf(file_path)
        elif ext == '.docx':
            return self._load_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _load_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            return clean_text(f.read())
    
    def _load_md(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            html_content = markdown.markdown(md_content)
            text_content = ''.join([c for c in html_content if c.isalnum() or c.isspace()])
            return clean_text(text_content)
    
    def _load_pdf(self, file_path: str) -> str:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return clean_text(text)
    
    def _load_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return clean_text(text)
    
    def split_document(self, text: str, chunk_size: int = None, chunk_overlap: int = None) -> list:
        chunk_size = chunk_size or config.MAX_DOC_LENGTH
        chunk_overlap = chunk_overlap or config.MAX_DOC_OVERLAP
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            chunk = text[start:end]
            
            if end < text_length:
                last_period = chunk.rfind('。')
                last_newline = chunk.rfind('\n')
                split_pos = max(last_period, last_newline)
                if split_pos > start + chunk_overlap:
                    end = split_pos + 1
                    chunk = text[start:end]
            
            if len(chunk.strip()) > 0:
                chunks.append(chunk.strip())
            
            start = end - chunk_overlap
        
        return chunks

document_processor = DocumentProcessor()