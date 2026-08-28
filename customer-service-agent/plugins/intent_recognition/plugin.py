import json
from pathlib import Path
from typing import Dict, List

class IntentRecognitionPlugin:
    """意图识别插件"""
    
    def __init__(self, intents_file: str = "data/intents.json"):
        self.intents = self._load_intents(intents_file)
        self.keyword_map = self._build_keyword_map()
    
    def _load_intents(self, intents_file: str) -> List[Dict]:
        """加载意图定义"""
        path = Path(intents_file)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _build_keyword_map(self) -> Dict[str, str]:
        """构建关键词映射表"""
        keyword_map = {}
        for intent in self.intents:
            for example in intent.get("examples", []):
                keywords = example.split()
                for kw in keywords:
                    if kw not in keyword_map:
                        keyword_map[kw] = intent["name"]
        return keyword_map
    
    def recognize(self, user_input: str) -> Dict:
        """识别用户意图"""
        intent = self._keyword_match(user_input)
        
        if intent == "unknown":
            intent = self._llm_recognize(user_input)
        
        return {
            "intent": intent,
            "confidence": 0.9,
            "original_input": user_input
        }
    
    def _keyword_match(self, user_input: str) -> str:
        """关键词匹配"""
        words = user_input.split()
        for word in words:
            if word in self.keyword_map:
                return self.keyword_map[word]
        return "unknown"
    
    def _llm_recognize(self, user_input: str) -> str:
        """大模型识别（简化版）"""
        return "unknown"


if __name__ == "__main__":
    plugin = IntentRecognitionPlugin()
    
    print("测试意图识别：")
    print(plugin.recognize("如何修改密码"))
    print(plugin.recognize("我的订单在哪"))
    print(plugin.recognize("我要投诉"))
    print(plugin.recognize("你好"))
    print(plugin.recognize("今天天气怎么样"))