from sentence_transformers import SentenceTransformer
from config.config import config

class EmbeddingModel:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or config.EMBEDDING_MODEL
        self.model = None
    
    def load_model(self):
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
    
    def encode(self, texts: list) -> list:
        if self.model is None:
            self.load_model()
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def get_dimension(self) -> int:
        if self.model is None:
            self.load_model()
        return self.model.get_sentence_embedding_dimension()

embedding_model = EmbeddingModel()