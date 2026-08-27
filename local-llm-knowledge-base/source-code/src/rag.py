import ollama
from config.config import config
from src.embedding import embedding_model
from src.vector_db import vector_db

class RAGSystem:
    def __init__(self):
        self.embedding_model = embedding_model
        self.vector_db = vector_db
    
    def build_knowledge_base(self, documents: list, metadatas: list = None):
        self.vector_db.connect()
        self.vector_db.add_documents(documents, metadatas)
    
    def retrieve(self, query: str, top_k: int = None) -> list:
        top_k = top_k or config.TOP_K_RESULTS
        results = self.vector_db.query([query], n_results=top_k)
        
        retrieved_docs = []
        for i in range(len(results['documents'][0])):
            doc = {
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            }
            if doc['distance'] < (1 - config.SIMILARITY_THRESHOLD):
                retrieved_docs.append(doc)
        
        return retrieved_docs
    
    def generate_answer(self, query: str, context_docs: list) -> str:
        context = "\n\n".join([doc['content'] for doc in context_docs])
        
        prompt = f"""
你是一个专业的知识库助手。请根据以下提供的上下文信息回答用户的问题。

上下文信息：
{context}

用户问题：
{query}

请遵循以下规则：
1. 优先使用上下文信息回答问题
2. 如果上下文中没有相关信息，请明确说明"根据现有知识库无法回答该问题"
3. 回答要简洁明了，避免冗长
4. 可以引用上下文内容，但要用自己的话重新组织
"""
        
        response = ollama.chat(
            model=config.OLLAMA_MODEL,
            messages=[{'role': 'user', 'content': prompt}]
        )
        
        return response['message']['content']
    
    def query(self, query: str) -> dict:
        retrieved_docs = self.retrieve(query)
        
        if not retrieved_docs:
            return {
                'answer': '根据现有知识库无法回答该问题',
                'sources': [],
                'retrieved_count': 0
            }
        
        answer = self.generate_answer(query, retrieved_docs)
        
        sources = []
        for i, doc in enumerate(retrieved_docs):
            source_info = {
                'index': i + 1,
                'content': doc['content'][:100] + '...' if len(doc['content']) > 100 else doc['content'],
                'metadata': doc.get('metadata', {})
            }
            sources.append(source_info)
        
        return {
            'answer': answer,
            'sources': sources,
            'retrieved_count': len(retrieved_docs)
        }

rag_system = RAGSystem()