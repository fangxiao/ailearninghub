import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml

from src.dialog_manager import DialogManager
from src.user_memory import UserMemory
from src.evaluator import MetricsCollector
from plugins.intent_recognition.plugin import IntentRecognitionPlugin
from plugins.knowledge_base.plugin import KnowledgeBasePlugin
from plugins.sentiment_analysis.plugin import SentimentAnalysisPlugin
from plugins.order_query.plugin import OrderQueryPlugin
from plugins.vector_kb.plugin import VectorKBPlugin
from plugins.function_calling.plugin import FunctionCallingPlugin
from plugins.multi_agent.plugin import RouterAgent


class CustomerServiceBot:
    """生产级客服Bot - 整合所有模块"""

    def __init__(self, config_path: str = "config/customer_service.yaml"):
        self.config = self._load_config(config_path)
        self.system_prompt = self._load_prompt()

        self.dialog = DialogManager()
        self.memory = UserMemory()
        self.metrics = MetricsCollector()

        self.intent_plugin = IntentRecognitionPlugin()
        self.kb_plugin = KnowledgeBasePlugin()
        self.vector_kb_plugin = VectorKBPlugin()
        self.sentiment_plugin = SentimentAnalysisPlugin()
        self.order_plugin = OrderQueryPlugin()

        self.fc_plugin = FunctionCallingPlugin()
        self._register_default_tools()

        self.router = RouterAgent()

        self.current_user_id: Optional[str] = None

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_prompt(self) -> str:
        prompt_path = Path("config/prompts/system_prompt.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return "你是一个客服助手。"

    def _register_default_tools(self):
        self.fc_plugin.register_tool(
            name="query_order",
            description="查询订单状态、物流信息",
            parameters={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "订单号"},
                    "phone": {"type": "string", "description": "手机号"}
                }
            },
            handler=self.order_plugin.query
        )
        self.fc_plugin.register_tool(
            name="query_faq",
            description="查询常见问题解答",
            parameters={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "问题内容"}
                }
            },
            handler=lambda question: self.vector_kb_plugin.search(question, top_k=1)
        )

    def chat(self, user_input: str, user_id: str = "anonymous") -> str:
        start_time = time.time()
        self.current_user_id = user_id

        self.dialog.add_message("user", user_input)

        sentiment = self.sentiment_plugin.analyze(user_input)
        if sentiment.get("need_handoff"):
            response = "非常抱歉，我立即为您转人工客服。"
            self._record(user_input, response, "handoff", start_time)
            return response

        intent_result = self.intent_plugin.recognize(user_input)
        intent = intent_result.get("intent", "unknown")

        if intent == "unknown" and self.dialog.slots.get("intent") == "order":
            if re.search(r'\d+[朵枝束个]', user_input):
                intent = "order"
            elif any(p in user_input for p in ["玫瑰", "百合", "康乃馨", "向日葵", "郁金香", "花", "朵", "枝"]):
                intent = "order"
            elif self.dialog.slots.get("product"):
                intent = "order"

        if intent == "order_query":
            response = self._handle_order_query(user_input)
        elif intent == "complaint":
            response = self._handle_complaint(user_input)
        elif intent == "greeting":
            response = self.memory.get_personalized_greeting(user_id)
        elif intent in ("faq_query", "faq"):
            response = self._handle_faq(user_input)
        elif intent == "human_handoff":
            response = "正在为您转接人工客服，请稍候..."
        elif intent == "thanks":
            response = "不客气！还有什么可以帮您？"
        elif intent == "order":
            response = self._handle_order(user_input)
        else:
            response = self._handle_general(user_input)

        self.dialog.add_message("assistant", response)
        self.memory.record_interaction(user_id, intent, user_input, response)
        self._record(user_input, response, intent, start_time)

        return response

    def _handle_order_query(self, user_input: str) -> str:
        result = self.order_plugin.query(user_input)
        if result.get("need_more_info"):
            return result["message"]
        if result.get("success"):
            return result["formatted"]
        return result.get("message", "查询失败")

    def _handle_order(self, user_input: str) -> str:
        self.dialog.fill_slot("intent", "order")

        products = [
            ("玫瑰花", "玫瑰花束"),
            ("百合", "百合花束"),
            ("康乃馨", "康乃馨花束"),
            ("向日葵", "向日葵花束"),
            ("郁金香", "郁金香花束"),
            ("花束", "花束"),
            ("花", "鲜花")
        ]
        for keyword, name in products:
            if keyword in user_input:
                self.dialog.fill_slot("product", name)
                break

        qty_match = re.search(r'(\d+)(?:朵|枝|束|个)', user_input)
        if qty_match:
            self.dialog.fill_slot("quantity", qty_match.group(1) + "朵")

        slots = self.dialog.slots
        if "product" not in slots:
            return "好的，您想订购什么？请告诉我商品名称。"
        if "quantity" not in slots:
            return f"好的，{slots['product']}要多少？"
        return f"好的，已为您预订 {slots['quantity']} {slots['product']}。请告诉我配送地址。"

    def _handle_complaint(self, user_input: str) -> str:
        return "非常抱歉给您带来不好的体验。请告诉我具体情况，我会尽力帮您解决。"

    def _handle_faq(self, user_input: str) -> str:
        kb_results = self.kb_plugin.search(user_input)
        if kb_results:
            return kb_results[0]["faq"]["answer"]
        results = self.vector_kb_plugin.search_with_keyword_fallback(user_input)
        if results:
            return results[0]["answer"]
        return "抱歉，我暂时无法回答这个问题。您可以转人工客服咨询。"

    def _handle_general(self, user_input: str) -> str:
        if self.config.get('llm', {}).get('enabled', False):
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ]
            return self._call_llm(messages)
        else:
            return self._rule_based_reply(user_input)

    def _rule_based_reply(self, user_input: str) -> str:
        """规则回复（无需LLM）"""
        replies = {
            "订": "好的，您想订购什么？请告诉我商品名称和数量。",
            "退款": "关于退款问题，您可以在订单详情页点击「申请退款」，我们会在1-3个工作日处理。",
            "配送": "一般下单后2小时内送达，具体时间看配送地址。",
        }
        for keyword, reply in replies.items():
            if keyword in user_input:
                return reply
        return "我暂时还在学习中，您可以尝试描述您的问题，或转人工客服。"

    def _record(self, user_input: str, response: str,
               intent: str, start_time: float):
        self.metrics.log_conversation({
            "user_id": self.current_user_id,
            "messages": self.dialog.get_history(),
            "intent": intent,
            "resolved": intent not in ("unknown", "consult"),
            "handoff": intent == "handoff",
            "response_time_ms": (time.time() - start_time) * 1000
        })

    def _call_llm(self, messages: list) -> str:
        provider = self.config.get('llm', {}).get('provider', 'zhipu')
        model = self.config.get('llm', {}).get('model', 'glm-5.1-flash')

        if provider == 'zhipu':
            return self._call_zhipu(messages, model)
        elif provider == 'ollama':
            return self._call_ollama(messages, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _call_zhipu(self, messages: list, model: str) -> str:
        from zhipuai import ZhipuAI
        client = ZhipuAI()
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content

    def _call_ollama(self, messages: list, model: str) -> str:
        import ollama
        response = ollama.chat(model=model, messages=messages)
        return response['message']['content']

    def get_status(self) -> Dict:
        return {
            "user_id": self.current_user_id,
            "dialog_messages": len(self.dialog.get_history()),
            "user_summary": self.memory.get_user_summary(
                self.current_user_id or "anonymous"
            ),
            "metrics": self.metrics.logs[-1] if self.metrics.logs else {}
        }


if __name__ == "__main__":
    bot = CustomerServiceBot()

    print("=== 客服Bot测试 ===")

    print("\n1. 问候")
    print(bot.chat("你好", "user_001"))

    print("\n2. 订单查询")
    print(bot.chat("我的订单20240601001到哪了", "user_001"))

    print("\n3. FAQ")
    print(bot.chat("如何退款？", "user_001"))

    print("\n4. 多轮对话（订花）")
    print(bot.chat("我要订花", "user_001"))
    print(bot.chat("99朵", "user_001"))

    print("\n5. 情绪激动")
    print(bot.chat("你们的服务太差了！", "user_002"))

    print("\n6. 转人工")
    print(bot.chat("转人工", "user_001"))

    print("\n7. 状态")
    print(bot.get_status())
