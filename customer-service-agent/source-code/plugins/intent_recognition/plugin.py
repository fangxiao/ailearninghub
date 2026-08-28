import json
import re
from pathlib import Path
from typing import Dict, List


class IntentRecognitionPlugin:
    """意图识别插件 - 支持关键词+正则匹配"""

    def __init__(self, intents_file: str = "data/intents.json"):
        self.intents = self._load_intents(intents_file)
        self.rules = self._build_rules()

    def _load_intents(self, intents_file: str) -> List[Dict]:
        path = Path(intents_file)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _build_rules(self) -> List[Dict]:
        rules = []
        for intent in self.intents:
            name = intent["name"]
            examples = intent.get("examples", [])

            patterns = list(examples)

            for ex in examples:
                chars = [c for c in ex if c.strip()]
                for i in range(len(chars)):
                    for j in range(i + 3, min(i + 6, len(chars) + 1)):
                        patterns.append(''.join(chars[i:j]))

            rules.append({
                "name": name,
                "patterns": list(set(patterns)),
                "priority": self._get_priority(name)
            })

        rules.sort(key=lambda r: -r["priority"])
        return rules

    def _get_priority(self, intent_name: str) -> int:
        priorities = {
            "order_query": 10,
            "complaint": 9,
            "human_handoff": 8,
            "faq_query": 7,
            "greeting": 5,
            "thanks": 3,
            "unknown": 0
        }
        return priorities.get(intent_name, 1)

    def recognize(self, user_input: str) -> Dict:
        intent = self._match(user_input)
        return {
            "intent": intent,
            "confidence": 0.9,
            "original_input": user_input
        }

    def _match(self, user_input: str) -> str:
        best_match = None
        best_len = 0
        for rule in self.rules:
            for pattern in rule["patterns"]:
                if len(pattern) >= 2 and pattern in user_input:
                    if len(pattern) > best_len:
                        best_match = rule["name"]
                        best_len = len(pattern)
                    elif len(pattern) == best_len and rule["priority"] > self._get_priority(best_match):
                        best_match = rule["name"]
        return best_match or "unknown"


if __name__ == "__main__":
    plugin = IntentRecognitionPlugin()

    print("测试意图识别：")
    tests = [
        "你好",
        "我的订单20240601001到哪了",
        "查一下订单状态",
        "我要投诉",
        "服务太差了",
        "如何修改密码",
        "今天天气怎么样",
        "转人工",
    ]
    for t in tests:
        result = plugin.recognize(t)
        print(f"  '{t}' -> {result['intent']}")
