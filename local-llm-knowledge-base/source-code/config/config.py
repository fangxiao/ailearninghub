import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3:8b")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    DOCS_PATH = os.getenv("DOCS_PATH", "./data/docs")
    MAX_DOC_LENGTH = int(os.getenv("MAX_DOC_LENGTH", 500))
    MAX_DOC_OVERLAP = int(os.getenv("MAX_DOC_OVERLAP", 50))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 3))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", 0.7))
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

config = Config()