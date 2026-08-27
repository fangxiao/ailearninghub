import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify
from src.harness import CustomerServiceHarness

app = Flask(__name__, template_folder='templates', static_folder='static')

harness = CustomerServiceHarness()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '').strip()
    user_id = data.get('user_id', 'anonymous')

    if not user_input:
        return jsonify({'error': '消息不能为空'}), 400

    start_time = time.time()
    response = harness.chat(user_input, user_id)
    elapsed = (time.time() - start_time) * 1000

    status = harness.get_status()

    return jsonify({
        'response': response,
        'skill': status.get('last_skill', 'unknown'),
        'intent': status.get('last_intent', 'unknown'),
        'response_time_ms': round(elapsed, 1),
        'user_summary': status.get('user_summary', ''),
        'dialog_messages': status.get('dialog_messages', 0),
        'slots': status.get('dialog_slots', {}),
        'circuit_states': status.get('circuit_states', {})
    })


@app.route('/api/status', methods=['GET'])
def status():
    return jsonify(harness.get_status())


@app.route('/api/reset', methods=['POST'])
def reset():
    harness.reset()
    return jsonify({'ok': True, 'message': '对话已重置'})


@app.route('/api/skills', methods=['GET'])
def list_skills():
    return jsonify(harness.registry.list_skills_info())


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'bot': 'CustomerServiceHarness v2.0',
        'architecture': 'Harness+Skill',
        'skills_count': len(harness.registry.get_all_skills())
    })


if __name__ == '__main__':
    print("=" * 60)
    print("  客服Agent加强版 (Harness+Skill) Web界面已启动")
    print("  访问: http://127.0.0.1:5000")
    print("  按 Ctrl+C 停止")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
