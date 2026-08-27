import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import config
from src.document_processor import document_processor
from src.rag import rag_system
from src.utils import list_files_in_directory, ensure_directory_exists

def load_documents_from_directory(docs_path: str) -> list:
    extensions = document_processor.supported_extensions
    files = list_files_in_directory(docs_path, extensions)
    
    documents = []
    metadatas = []
    
    for file_path in files:
        try:
            text = document_processor.load_document(file_path)
            chunks = document_processor.split_document(text)
            
            for chunk in chunks:
                documents.append(chunk)
                metadatas.append({
                    'source': os.path.basename(file_path),
                    'file_path': file_path
                })
            
            print(f"Loaded {len(chunks)} chunks from {file_path}")
        except Exception as e:
            print(f"Failed to load {file_path}: {e}")
    
    return documents, metadatas

def build_knowledge_base():
    ensure_directory_exists(config.DOCS_PATH)
    ensure_directory_exists(config.CHROMA_DB_PATH)
    
    print("Loading documents from directory...")
    documents, metadatas = load_documents_from_directory(config.DOCS_PATH)
    
    if not documents:
        print("No documents found. Please add documents to the data/docs directory.")
        return
    
    print(f"Building knowledge base with {len(documents)} chunks...")
    rag_system.build_knowledge_base(documents, metadatas)
    print("Knowledge base built successfully!")

def query_knowledge_base(query: str) -> dict:
    return rag_system.query(query)

def interactive_mode():
    print("\n=== Local LLM Knowledge Base ===")
    print("Type 'exit' to quit.\n")
    
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            print("Goodbye!")
            break
        
        result = query_knowledge_base(query)
        
        print(f"\nAI: {result['answer']}")
        
        if result['sources']:
            print("\nSources:")
            for source in result['sources']:
                print(f"  [{source['index']}] {source['content']}")

if __name__ == "__main__":
    build_knowledge_base()
    interactive_mode()