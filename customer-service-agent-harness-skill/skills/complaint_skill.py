from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class ComplaintSkill(BaseSkill):
    """投诉Skill - 处理用户投诉和不满"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @property
    def name(self) -> str:
        return "complaint"

    @property
    def description(self) -> str:
        return "投诉Skill - 处理用户投诉、不满情绪"

    @property
    def triggers(self) -> List[str]:
        return ["投诉", "差评", "不满意", "太差", "生气", "愤怒", "垃圾", "骗子"]

    @property
    def priority(self) -> int:
        return 8

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        score = super().can_handle(user_input, context)
        sentiment = context.get("sentiment") or {}
        if sentiment.get("level", 0) >= 4:
            score = max(score, 0.9)
        if context.get("intent") == "complaint":
            score = max(score, 0.85)
        return score

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        sentiment = context.get("sentiment", {})
        level = sentiment.get("level", 2)

        if level >= 5:
            response = "非常抱歉给您带来如此糟糕的体验。我立即为您转接资深客服主管，他/她会优先处理您的问题。"
            return SkillResult(
                success=True,
                response=response,
                need_handoff=True,
                data={"escalated": True},
                confidence=1.0
            )

        if level >= 4:
            response = "非常抱歉给您带来不好的体验。请告诉我具体情况，我会尽力帮您解决。如果需要，我也可以为您转接人工客服。"
        else:
            response = "非常抱歉给您带来不便。请告诉我具体情况，我会尽力帮您解决。"

        return SkillResult(
            success=True,
            response=response,
            data={"complaint_handled": True},
            confidence=0.8
        )
