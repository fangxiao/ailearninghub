import re
from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class SlotFillingSkill(BaseSkill):
    """槽位填充Skill - 处理多轮对话中的信息收集"""

    def __init__(self, config: Dict[str, Any], dialog: Any):
        self.config = config
        self.dialog = dialog

    @property
    def name(self) -> str:
        return "slot_filling"

    @property
    def description(self) -> str:
        return "槽位填充Skill - 多轮对话中收集订单所需信息"

    @property
    def triggers(self) -> List[str]:
        return ["订花", "买花", "订购", "下单", "订一束", "我要订", "购买"]

    @property
    def priority(self) -> int:
        return 8

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        score = super().can_handle(user_input, context)
        slots = context.get("slots", {})
        dialog_state = context.get("dialog", {}).get("state", "")
        
        if dialog_state == "ORDER_COMPLETE":
            return 0.0
        
        if context.get("intent") == "order":
            score = max(score, 0.9)
        if slots.get("intent") == "order" and not slots.get("address"):
            score = max(score, 0.95)
        return score

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        self.dialog.fill_slot("intent", "order")

        products = [
            ("玫瑰花", "玫瑰花束"), ("玫瑰", "玫瑰花束"),
            ("百合", "百合花束"),
            ("康乃馨", "康乃馨花束"),
            ("向日葵", "向日葵花束"),
            ("郁金香", "郁金香花束"),
            ("花束", "花束"), ("鲜花", "鲜花"),
            ("花", "鲜花")
        ]
        for keyword, name in products:
            if keyword in user_input:
                self.dialog.fill_slot("product", name)
                break

        qty_match = re.search(r'(\d+)(?:朵|枝|束|个|份)', user_input)
        if qty_match:
            self.dialog.fill_slot("quantity", qty_match.group(1) + "朵")

        addr_match = re.search(
            r'(?:送到|运往|发往|地址是)([\u4e00-\u9fa5]+[^\s，,。]{2,20})',
            user_input
        )
        if addr_match:
            self.dialog.fill_slot("address", addr_match.group(1))

        slots = self.dialog.slots
        missing = self.dialog.missing_slots(["product", "quantity", "address"])

        if not slots.get("product"):
            return SkillResult(
                success=True,
                response="好的，您想订购什么？请告诉我商品名称（如玫瑰花、百合花等）。",
                data={"missing": missing, "slots": slots},
                confidence=0.8
            )

        if not slots.get("quantity"):
            return SkillResult(
                success=True,
                response=f"好的，{slots['product']}要多少？（如99朵、52朵）",
                data={"missing": missing, "slots": slots},
                confidence=0.8
            )

        if not slots.get("address"):
            return SkillResult(
                success=True,
                response=f"好的，已为您预订 {slots['quantity']} {slots['product']}。请告诉我配送地址。",
                data={"missing": missing, "slots": slots},
                confidence=0.8
            )

        self.dialog.set_state("ORDER_COMPLETE")
        response_text = f"✅ 订单已确认：{slots['quantity']} {slots['product']}，配送地址：{slots['address']}。我们会尽快为您配送！"
        response_data = {"slots": dict(slots), "order_created": True}
        for key in ["product", "quantity", "address", "location", "intent"]:
            self.dialog.slots.pop(key, None)
        return SkillResult(
            success=True,
            response=response_text,
            data=response_data,
            confidence=1.0
        )
