from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class GreetingSkill(BaseSkill):
    """问候Skill - 处理打招呼、感谢等社交场景"""

    def __init__(self, config: Dict[str, Any], memory: Any):
        self.config = config
        self.memory = memory

    @property
    def name(self) -> str:
        return "greeting"

    @property
    def description(self) -> str:
        return "问候Skill - 处理用户打招呼、感谢"

    @property
    def triggers(self) -> List[str]:
        return ["你好", "您好", "hi", "hello", "在吗", "有人吗", "谢谢", "感谢", "好的", "不客气"]

    @property
    def priority(self) -> int:
        return 5

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        score = super().can_handle(user_input, context)
        return score

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        user_id = context.get("user_id", "anonymous")

        if any(t in user_input.lower() for t in ["谢谢", "感谢", "好的谢谢"]):
            response = "不客气！还有什么可以帮您？"
        elif any(t in user_input.lower() for t in ["好的", "不客气"]):
            response = "好的！祝您购物愉快。"
        else:
            response = self.memory.get_personalized_greeting(user_id)

        return SkillResult(
            success=True,
            response=response,
            confidence=0.9
        )
