from typing import List, Dict, Any, Optional
from skills.base import BaseSkill


class SkillRouter:
    """Skill路由器 - 根据用户输入选择最合适的Skill"""

    def __init__(self):
        self._intent_rules: Dict[str, str] = {}
        self._fallback_skill: Optional[str] = None

    def set_fallback(self, skill_name: str):
        """设置兜底技能"""
        self._fallback_skill = skill_name

    def add_intent_rule(self, intent: str, skill_name: str):
        """添加意图到技能的映射规则"""
        self._intent_rules[intent] = skill_name

    def route(self, user_input: str, context: Dict[str, Any],
              skills: List[BaseSkill]) -> Optional[BaseSkill]:
        """
        路由决策：选择最适合的Skill
        策略：
        1. 如果上下文中有明确的意图映射，优先使用
        2. 计算每个Skill的can_handle置信度
        3. 选择置信度最高的Skill
        4. 如果都不匹配，使用兜底Skill
        """
        explicit_intent = context.get("intent")
        if explicit_intent and explicit_intent in self._intent_rules:
            target_name = self._intent_rules[explicit_intent]
            for skill in skills:
                if skill.name == target_name:
                    return skill

        best_skill = None
        best_score = 0.0

        for skill in skills:
            if skill.pre_skill:
                continue
            score = skill.can_handle(user_input, context)
            if score > best_score:
                best_score = score
                best_skill = skill

        if best_skill and best_score > 0.3:
            return best_skill

        if self._fallback_skill:
            for skill in skills:
                if skill.name == self._fallback_skill:
                    return skill

        return None

    def get_routing_info(self) -> Dict[str, Any]:
        """获取路由配置信息"""
        return {
            "intent_rules": self._intent_rules,
            "fallback": self._fallback_skill
        }
