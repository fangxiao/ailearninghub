import json
import re
from pathlib import Path
from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class IntentRecognitionSkill(BaseSkill):
    """意图识别Skill - 识别用户意图，供路由决策"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.intents = self._load_intents()
        self.rules = self._build_rules()

    def _load_intents(self) -> List[Dict]:
        path = Path("data/intents.json")
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
            "order_query": 10, "complaint": 9, "human_handoff": 8,
            "faq_query": 7, "greeting": 5, "thanks": 3, "order": 6,
            "unknown": 0
        }
        return priorities.get(intent_name, 1)

    @property
    def name(self) -> str:
        return "intent_recognition"

    @property
    def description(self) -> str:
        return "意图识别Skill - 识别用户输入的意图"

    @property
    def pre_skill(self) -> bool:
        return True

    @property
    def priority(self) -> int:
        return 8

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        return 0.85

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        intent = self._match(user_input)

        if intent == "unknown":
            if context.get("slots", {}).get("intent") == "order":
                if re.search(r'\d+[朵枝束个]', user_input) or \
                   any(p in user_input for p in ["玫瑰", "百合", "康乃馨", "向日葵", "郁金香", "花", "朵", "枝"]):
                    intent = "order"
                elif context.get("slots", {}).get("product"):
                    intent = "order"

        confidence = 0.9 if intent != "unknown" else 0.3

        return SkillResult(
            success=True,
            response="",
            data={
                "intent": intent,
                "confidence": confidence,
                "original_input": user_input
            },
            confidence=confidence
        )

    def _match(self, user_input: str) -> str:
        best_match = None
        best_len = 0
        for rule in self.rules:
            for pattern in rule["patterns"]:
                if len(pattern) >= 2 and pattern in user_input:
                    if len(pattern) > best_len:
                        best_match = rule["name"]
                        best_len = len(pattern)
                    elif len(pattern) == best_len and rule["priority"] > \
                            self._get_priority(best_match or "unknown"):
                        best_match = rule["name"]
        return best_match or "unknown"
