from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class HandoffSkill(BaseSkill):
    """转人工Skill - 处理用户转人工请求"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.handoff_config = config.get("human_handoff", {})

    @property
    def name(self) -> str:
        return "handoff"

    @property
    def description(self) -> str:
        return "转人工Skill - 转接人工客服"

    @property
    def triggers(self) -> List[str]:
        return ["转人工", "人工客服", "找人工", "人工服务", "客服电话"]

    @property
    def priority(self) -> int:
        return 10

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        score = super().can_handle(user_input, context)
        if context.get("intent") == "human_handoff":
            score = max(score, 0.95)
        return score

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        user_id = context.get("user_id", "anonymous")
        sentiment = context.get("sentiment", {})
        level = sentiment.get("level", 2)

        if level >= 5:
            response = "非常抱歉！我立即为您转接人工客服主管，请稍候..."
        elif level >= 4:
            response = "我已记录您的情况，正在为您转接人工客服，请稍候..."
        else:
            response = "正在为您转接人工客服，请稍候。工作时间：9:00-21:00。如需紧急联系，请拨打客服热线：400-xxx-xxxx"

        return SkillResult(
            success=True,
            response=response,
            need_handoff=True,
            data={
                "handoff_started": True,
                "user_id": user_id,
                "priority": "high" if level >= 4 else "normal"
            },
            confidence=1.0
        )
