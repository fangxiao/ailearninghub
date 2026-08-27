from typing import List, Dict, Any, Optional
from skills.base import BaseSkill, SkillResult


class SkillRegistry:
    """Skill注册中心 - 管理所有技能的生命周期"""

    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}
        self._pre_skills: List[BaseSkill] = []

    def register(self, skill: BaseSkill):
        """注册技能"""
        self._skills[skill.name] = skill
        if skill.pre_skill:
            self._pre_skills.append(skill)

    def unregister(self, name: str):
        """注销技能"""
        if name in self._skills:
            skill = self._skills[name]
            self._skills.pop(name)
            if skill.pre_skill and skill in self._pre_skills:
                self._pre_skills.remove(skill)

    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """获取技能"""
        return self._skills.get(name)

    def get_all_skills(self) -> List[BaseSkill]:
        """获取所有技能"""
        return list(self._skills.values())

    def get_pre_skills(self) -> List[BaseSkill]:
        """获取所有前置技能"""
        return self._pre_skills

    def find_by_intent(self, intent: str) -> Optional[BaseSkill]:
        """根据意图查找技能"""
        for skill in self._skills.values():
            if intent in skill.triggers:
                return skill
        return None

    def list_skills_info(self) -> List[Dict[str, Any]]:
        """列出所有技能信息"""
        return [skill.get_info() for skill in self._skills.values()]

    def clear(self):
        """清空所有技能"""
        self._skills.clear()
        self._pre_skills.clear()
