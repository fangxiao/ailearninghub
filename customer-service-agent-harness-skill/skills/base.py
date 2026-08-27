from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class SkillResult:
    success: bool = True
    response: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    next_action: Optional[str] = None
    confidence: float = 0.0
    need_handoff: bool = False
    error: Optional[str] = None


class BaseSkill(ABC):
    """Skill标准接口 - 所有客服技能的抽象基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """技能名称"""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """技能描述"""
        ...

    @property
    def triggers(self) -> List[str]:
        """触发关键词/模式"""
        return []

    @property
    def priority(self) -> int:
        """优先级（数值越大越优先）"""
        return 1

    @property
    def pre_skill(self) -> bool:
        """是否为前置Skill（在主流程前执行）"""
        return False

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        """
        评估该技能处理用户输入的置信度
        返回 0.0 ~ 1.0
        """
        if not self.triggers:
            return 0.0
        score = 0.0
        for trigger in self.triggers:
            if trigger.lower() in user_input.lower():
                score = max(score, 0.6)
                if trigger == user_input:
                    score = max(score, 0.9)
        return score

    @abstractmethod
    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        """执行技能，返回SkillResult"""
        ...

    def on_error(self, error: Exception, context: Dict[str, Any]) -> SkillResult:
        """降级处理 - 技能执行失败时调用"""
        return SkillResult(
            success=False,
            response="抱歉，处理您的请求时出现了问题，请稍后再试。",
            error=str(error)
        )

    def get_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {
            "name": self.name,
            "description": self.description,
            "triggers": self.triggers,
            "priority": self.priority,
            "pre_skill": self.pre_skill,
        }
