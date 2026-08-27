import re
from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class GeneralSkill(BaseSkill):
    """通用Skill - 兜底处理，支持LLM和规则回复"""

    def __init__(self, config: Dict[str, Any], llm: Any):
        self.config = config
        self.llm = llm

    @property
    def name(self) -> str:
        return "general"

    @property
    def description(self) -> str:
        return "通用Skill - 兜底处理所有未匹配的用户输入"

    @property
    def triggers(self) -> List[str]:
        return []

    @property
    def priority(self) -> int:
        return 1

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        return 0.2

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        if self.llm.is_available():
            response = self._llm_reply(user_input, context)
            if response and response.strip():
                return SkillResult(
                    success=True,
                    response=response,
                    data={"source": "llm"},
                    confidence=0.7
                )

        response = self._rule_based_reply(user_input)
        return SkillResult(
            success=True,
            response=response,
            data={"source": "rule_based"},
            confidence=0.5
        )

    def _llm_reply(self, user_input: str, context: Dict[str, Any]) -> str:
        system_prompt = (
            "你是一个专业、友好的客服助手。"
            "回答要简洁、专业、有礼貌。"
            "如果用户的问题与客服无关，请礼貌地说明并引导用户转人工客服。"
        )
        messages = context.get("history", [])
        if not messages:
            messages = [{"role": "user", "content": user_input}]
        result = self.llm.chat(messages, system_prompt=system_prompt)
        return result.get("content", "")

    def _rule_based_reply(self, user_input: str) -> str:
        replies = {
            "订": "好的，您想订购什么？请告诉我商品名称和数量。",
            "退款": "关于退款问题，您可以在订单详情页点击「申请退款」，我们会在1-3个工作日处理。",
            "配送": "一般下单后2小时内送达，具体时间看配送地址。",
            "支付": "我们支持支付宝、微信支付、银行卡、信用卡等多种支付方式。",
            "转人工": "正在为您转接人工客服，请稍候。",
        }
        for keyword, reply in replies.items():
            if keyword in user_input:
                return reply
        return "我暂时还在学习中，您可以尝试描述您的问题，或转人工客服。"
