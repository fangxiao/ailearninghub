import json
from pathlib import Path
from typing import Dict

class SentimentAnalysisPlugin:
    """情感分析插件"""
    
    def __init__(self, sentiment_file: str = "data/sentiments.json"):
        self.sentiments = self._load_sentiments(sentiment_file)
        self.keyword_map = self._build_keyword_map()
    
    def _load_sentiments(self, sentiment_file: str) -> list:
        """加载情感定义"""
        path = Path(sentiment_file)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _build_keyword_map(self) -> Dict[str, int]:
        """构建关键词映射表"""
        keyword_map = {}
        for sentiment in self.sentiments:
            for keyword in sentiment.get("keywords", []):
                keyword_map[keyword] = sentiment["level"]
        return keyword_map
    
    def analyze(self, user_input: str) -> Dict:
        """分析用户情感"""
        sentiment_level = self._keyword_match(user_input)
        
        if sentiment_level == 0:
            sentiment_level = self._llm_analyze(user_input)
        
        sentiment = self._get_sentiment_by_level(sentiment_level)
        
        return {
            "level": sentiment_level,
            "name": sentiment.get("name", "未知"),
            "response_strategy": sentiment.get("response", "正常回复"),
            "need_handoff": sentiment_level >= 4
        }
    
    def _keyword_match(self, user_input: str) -> int:
        """关键词匹配 - 支持子串匹配"""
        max_level = 0
        for keyword, level in self.keyword_map.items():
            if keyword in user_input:
                max_level = max(max_level, level)
        return max_level
    
    def _llm_analyze(self, user_input: str) -> int:
        """大模型分析（简化版）"""
        return 2
    
    def _get_sentiment_by_level(self, level: int) -> Dict:
        """根据等级获取情感信息"""
        for sentiment in self.sentiments:
            if sentiment["level"] == level:
                return sentiment
        return {"level": 2, "name": "中性", "response": "正常回复"}


if __name__ == "__main__":
    plugin = SentimentAnalysisPlugin()
    
    print("测试情感分析：")
    print(plugin.analyze("谢谢"))
    print(plugin.analyze("你好"))
    print(plugin.analyze("太慢了"))
    print(plugin.analyze("我要投诉"))