import os
import sys
import json
import time
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify

from src.bot import CustomerServiceBot

app = Flask(__name__, template_folder='templates', static_folder='static')

bot = CustomerServiceBot()

sessions = {}


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
    response = bot.chat(user_input, user_id)
    elapsed = (time.time() - start_time) * 1000

    status = bot.get_status()

    return jsonify({
        'response': response,
        'intent': status.get('metrics', {}).get('intent', 'unknown'),
        'response_time_ms': round(elapsed, 1),
        'user_summary': status.get('user_summary', ''),
        'dialog_messages': status.get('dialog_messages', 0)
    })


@app.route('/api/status', methods=['GET'])
def status():
    return jsonify(bot.get_status())


@app.route('/api/reset', methods=['POST'])
def reset():
    bot.dialog.clear()
    return jsonify({'ok': True, 'message': '对话已重置'})


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'bot': 'CustomerServiceBot v1.0'})


if __name__ == '__main__':
    print("=" * 50)
    print("  客服Agent Web界面已启动")
    print("  访问: http://127.0.0.1:5000")
    print("  按 Ctrl+C 停止")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
