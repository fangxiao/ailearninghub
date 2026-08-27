from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class MemorySkill(BaseSkill):
    """记忆Skill - 查询和更新用户画像"""

    def __init__(self, config: Dict[str, Any], memory: Any):
        self.config = config
        self.memory = memory

    @property
    def name(self) -> str:
        return "memory"

    @property
    def description(self) -> str:
        return "记忆Skill - 查询用户信息、更新用户画像"

    @property
    def triggers(self) -> List[str]:
        return ["我的信息", "我的资料", "我的等级", "会员", "个人信息"]

    @property
    def priority(self) -> int:
        return 4

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        return super().can_handle(user_input, context)

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        user_id = context.get("user_id", "anonymous")
        user_summary = self.memory.get_user_summary(user_id)
        segment = self.memory.build_user_segment(user_id)

        return SkillResult(
            success=True,
            response=f"您的账户信息：{user_summary}",
            data={
                "user_summary": user_summary,
                "segment": segment
            },
            confidence=0.9
        )
