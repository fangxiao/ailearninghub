from typing import List, Dict, Optional
import re


class DialogManager:
    """对话管理器 - 支持多轮对话、槽位填充、指代消解"""

    def __init__(self, max_history: int = 10):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.key_info: Dict = {}

        self.slots: Dict = {}
        self.state: str = "INIT"
        self.entities: List[Dict] = []

    def add_message(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content
        })

        self._extract_key_info(content)
        self._extract_entities(content)

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self) -> List[Dict]:
        return self.history

    def get_key_info(self) -> Dict:
        return self.key_info

    def _extract_key_info(self, content: str):
        order_pattern = r'订单[号]?[:\s]*(\w{6,})'
        match = re.search(order_pattern, content)
        if match:
            self.key_info["order_id"] = match.group(1)

        phone_pattern = r'1[3-9]\d{9}'
        match = re.search(phone_pattern, content)
        if match:
            self.key_info["phone"] = match.group(0)

    def _extract_entities(self, text: str):
        entities_to_find = [
            ("order_id", r'订单[号]?[:\s]*(\w{6,})'),
            ("phone", r'1[3-9]\d{9}'),
            ("date", r'(\d{4}[-/]\d{1,2}[-/]\d{1,2}|明天|后天|今天)'),
            ("location", r'(?:送到|运往|发往)([\u4e00-\u9fa5]+(?:市|区|路|号))'),
        ]
        for entity_type, pattern in entities_to_find:
            match = re.search(pattern, text)
            if match:
                entity = {
                    "type": entity_type,
                    "text": match.group(0),
                    "value": match.group(1) if match.lastindex else match.group(0),
                    "position": len(self.entities)
                }
                self.entities.append(entity)

    def resolve_reference(self, pronoun: str) -> Optional[Dict]:
        for entity in reversed(self.entities):
            if entity["text"] == pronoun:
                return entity
        return self.entities[-1] if self.entities else None

    def fill_slot(self, slot_name: str, value):
        self.slots[slot_name] = value

    def missing_slots(self, required_slots: List[str]) -> List[str]:
        return [s for s in required_slots if s not in self.slots]

    def get_context_for_llm(self) -> str:
        history_text = ""
        for msg in self.history[-5:]:
            role = "用户" if msg["role"] == "user" else "助手"
            history_text += f"{role}：{msg['content']}\n"
        if self.slots:
            history_text += f"\n已填充槽位：{self.slots}\n"
        if self.key_info:
            history_text += f"关键信息：{self.key_info}\n"
        return history_text

    def clear(self):
        self.history = []
        self.key_info = {}
        self.slots = {}
        self.state = "INIT"
        self.entities = []


if __name__ == "__main__":
    dm = DialogManager()

    print("测试多轮对话：")
    dm.add_message("user", "订一束花")
    dm.fill_slot("type", "玫瑰花")
    dm.fill_slot("quantity", 99)
    print(f"已填充槽位: {dm.slots}")
    print(f"缺失槽位: {dm.missing_slots(['type', 'quantity', 'address', 'time'])}")

    dm.add_message("user", "订单号20240601001到哪了")
    print(f"关键信息: {dm.get_key_info()}")
    print(f"实体列表: {dm.entities}")
