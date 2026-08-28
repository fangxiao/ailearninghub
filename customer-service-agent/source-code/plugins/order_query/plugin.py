import re
from typing import Dict, Optional

class OrderQueryPlugin:
    def __init__(self, db_connection=None):
        self.db = db_connection

    def query(self, user_input: str) -> Dict:
        order_id = self._extract_order_id(user_input)
        phone = self._extract_phone(user_input)

        if not order_id and not phone:
            return {
                "success": False,
                "need_more_info": True,
                "message": "请提供订单号或手机号，我帮您查询。"
            }

        orders = self._search_orders(order_id, phone)

        if not orders:
            return {
                "success": False,
                "message": "未找到相关订单，请确认信息是否正确。"
            }

        return {
            "success": True,
            "orders": orders,
            "formatted": self._format_orders(orders)
        }

    def _extract_order_id(self, text: str) -> Optional[str]:
        match = re.search(r'订单[号]?[:\s]*(\w{6,})', text)
        return match.group(1) if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        match = re.search(r'1[3-9]\d{9}', text)
        return match.group(0) if match else None

    def _search_orders(self, order_id, phone):
        # 实际项目中，这里会调用数据库或API
        # 简化示例
        return [
            {"order_id": "20240601001", "status": "配送中",
             "items": ["玫瑰花束"], "tracking": "SF123456"}
        ]

    def _format_orders(self, orders):
        parts = []
        for o in orders:
            parts.append(f"订单 {o['order_id']}：{o['status']}")
        return "\n".join(parts)
