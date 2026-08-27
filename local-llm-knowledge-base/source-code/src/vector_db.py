import chromadb
from chromadb.config import Settings
from config.config import config
from src.utils import ensure_directory_exists

class VectorDB:
    def __init__(self, collection_name: str = "knowledge_base"):
        self.collection_name = collection_name
        self.client = None
        self.collection = None
    
    def connect(self):
        ensure_directory_exists(config.CHROMA_DB_PATH)
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_PATH,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(self.collection_name)
    
    def add_documents(self, documents: list, metadatas: list = None, ids: list = None):
        if self.collection is None:
            self.connect()
        
        if metadatas is None:
            metadatas = [{} for _ in documents]
        
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_texts: list, n_results: int = None) -> dict:
        if self.collection is None:
            self.connect()
        
        n_results = n_results or config.TOP_K_RESULTS
        
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        return results
    
    def get_collection_stats(self) -> dict:
        if self.collection is None:
            self.connect()
        
        return self.collection.count()
    
    def clear_collection(self):
        if self.client is not None:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(self.collection_name)

vector_db = VectorDB()