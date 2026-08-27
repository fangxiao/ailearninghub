import re
from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class OrderSkill(BaseSkill):
    """订单Skill - 查询订单状态、物流信息"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @property
    def name(self) -> str:
        return "order"

    @property
    def description(self) -> str:
        return "订单Skill - 查询订单状态、物流信息"

    @property
    def triggers(self) -> List[str]:
        return ["订单", "物流", "发货", "配送", "快递", "到哪", "状态", "查单"]

    @property
    def priority(self) -> int:
        return 9

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        score = super().can_handle(user_input, context)
        if context.get("intent") == "order_query":
            score = max(score, 0.9)
        return score

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        order_id = self._extract_order_id(user_input)
        phone = self._extract_phone(user_input)

        if not order_id and not phone:
            slots = context.get("slots", {})
            if slots.get("order_id"):
                order_id = slots["order_id"]
            else:
                return SkillResult(
                    success=False,
                    response="请提供订单号或手机号，我帮您查询。",
                    confidence=0.5
                )

        orders = self._search_orders(order_id, phone)

        if not orders:
            return SkillResult(
                success=False,
                response="未找到相关订单，请确认信息是否正确。",
                confidence=0.6
            )

        response = self._format_orders(orders)
        return SkillResult(
            success=True,
            response=response,
            data={"orders": orders},
            confidence=0.9
        )

    def _extract_order_id(self, text: str) -> str:
        match = re.search(r'订单[号]?[:\s]*([a-zA-Z0-9]{6,})', text)
        return match.group(1) if match else None

    def _extract_phone(self, text: str) -> str:
        match = re.search(r'1[3-9]\d{9}', text)
        return match.group(0) if match else None

    def _search_orders(self, order_id: str = None, phone: str = None) -> List[Dict]:
        return [
            {
                "order_id": order_id or "20240601001",
                "status": "配送中",
                "items": ["玫瑰花束"],
                "tracking": "SF123456",
                "estimated_delivery": "明天 18:00 前"
            }
        ]

    def _format_orders(self, orders: List[Dict]) -> str:
        parts = []
        for o in orders:
            items_str = "、".join(o["items"])
            part = f"您的订单 {o['order_id']}：{o['status']}"
            if items_str:
                part += f"（{items_str}）"
            if o.get("estimated_delivery"):
                part += f"，预计 {o['estimated_delivery']} 送达"
            if o.get("tracking"):
                part += f"，物流单号：{o['tracking']}"
            parts.append(part)
        return "\n".join(parts)
