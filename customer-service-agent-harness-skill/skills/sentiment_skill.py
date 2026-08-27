import json
from pathlib import Path
from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class SentimentSkill(BaseSkill):
    """情感分析Skill - 前置Filter，识别用户情绪并触发相应策略"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sentiments = self._load_sentiments()
        self.keyword_map = self._build_keyword_map()

    def _load_sentiments(self) -> list:
        path = Path("data/sentiments.json")
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _build_keyword_map(self) -> Dict[str, int]:
        keyword_map = {}
        for sentiment in self.sentiments:
            for keyword in sentiment.get("keywords", []):
                keyword_map[keyword] = sentiment["level"]
        return keyword_map

    @property
    def name(self) -> str:
        return "sentiment"

    @property
    def description(self) -> str:
        return "情感分析Skill - 识别用户情绪，愤怒级自动触发转人工"

    @property
    def triggers(self) -> List[str]:
        return ["投诉", "太差", "生气", "愤怒", "满意", "感谢", "谢谢"]

    @property
    def priority(self) -> int:
        return 10

    @property
    def pre_skill(self) -> bool:
        return True

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        score = super().can_handle(user_input, context)
        level = self._keyword_match(user_input)
        if level >= 4:
            score = max(score, 0.8)
        return score

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        level = self._keyword_match(user_input)
        sentiment_info = self._get_sentiment_by_level(level)

        need_handoff = level >= 5

        if need_handoff:
            return SkillResult(
                success=True,
                response="非常抱歉给您带来不好的体验。我立即为您转接人工客服，稍后会有专人与您沟通。",
                data={
                    "sentiment_processed": True,
                    "sentiment": {
                        "level": level,
                        "name": sentiment_info.get("name", "愤怒"),
                        "need_handoff": True
                    }
                },
                need_handoff=True,
                confidence=1.0
            )

        return SkillResult(
            success=True,
            response="",
            data={
                "sentiment_processed": True,
                "sentiment": {
                    "level": level,
                    "name": sentiment_info.get("name", "中性"),
                    "need_handoff": False
                }
            },
            confidence=0.8
        )

    def _keyword_match(self, user_input: str) -> int:
        max_level = 0
        for keyword, level in self.keyword_map.items():
            if keyword in user_input:
                max_level = max(max_level, level)
        return max_level

    def _get_sentiment_by_level(self, level: int) -> Dict:
        for sentiment in self.sentiments:
            if sentiment["level"] == level:
                return sentiment
        return {"level": 2, "name": "中性", "response": "正常回复"}
