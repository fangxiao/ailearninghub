import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config.config import config
from src.rag import rag_system
from src.document_processor import document_processor
from src.utils import list_files_in_directory

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    result = rag_system.query(query)
    
    return jsonify({
        'answer': result['answer'],
        'sources': result['sources'],
        'retrieved_count': result['retrieved_count']
    })

@app.route('/api/documents', methods=['GET'])
def api_list_documents():
    extensions = document_processor.supported_extensions
    files = list_files_in_directory(config.DOCS_PATH, extensions)
    
    return jsonify({
        'documents': [os.path.basename(f) for f in files]
    })

@app.route('/api/rebuild', methods=['POST'])
def api_rebuild_knowledge_base():
    from src.main import build_knowledge_base
    
    try:
        build_knowledge_base()
        return jsonify({'message': 'Knowledge base rebuilt successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=True)