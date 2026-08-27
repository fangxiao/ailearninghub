import re
from typing import List, Dict, Optional


class DialogManager:
    """对话管理器 - 支持多轮对话、槽位填充、上下文管理"""

    def __init__(self, max_history: int = 20):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.slots: Dict[str, str] = {}
        self.state: str = "INIT"
        self.entities: List[Dict] = []

    def add_message(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": len(self.history)
        })
        self._extract_entities(content)
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def get_history(self) -> List[Dict]:
        return self.history

    def get_messages_for_llm(self) -> List[Dict[str, str]]:
        """获取用于LLM的消息列表"""
        messages = []
        for msg in self.history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        return messages

    def _extract_entities(self, text: str):
        patterns = [
            ("order_id", r'订单[号]?[:\s]*([a-zA-Z0-9]{6,})'),
            ("phone", r'1[3-9]\d{9}'),
            ("date", r'(\d{4}[-/]\d{1,2}[-/]\d{1,2}|明天|后天|今天)'),
            ("location", r'(?:送到|运往|发往|地址是)([\u4e00-\u9fa5]+(?:市|区|路|号|小区|栋))'),
            ("quantity", r'(\d+)(?:朵|枝|束|个|份)'),
            ("product", r'(玫瑰|百合|康乃馨|向日葵|郁金香|花束|鲜花)'),
        ]
        for entity_type, pattern in patterns:
            match = re.search(pattern, text)
            if match:
                value = match.group(1) if match.lastindex else match.group(0)
                self.entities.append({
                    "type": entity_type,
                    "value": value,
                    "text": match.group(0)
                })

    def fill_slot(self, slot_name: str, value: str):
        self.slots[slot_name] = value

    def get_slot(self, slot_name: str) -> Optional[str]:
        return self.slots.get(slot_name)

    def missing_slots(self, required: List[str]) -> List[str]:
        return [s for s in required if s not in self.slots]

    def get_context(self) -> Dict:
        return {
            "history": self.history,
            "slots": self.slots,
            "entities": self.entities,
            "state": self.state
        }

    def set_state(self, state: str):
        self.state = state

    def clear(self):
        self.history = []
        self.slots = {}
        self.state = "INIT"
        self.entities = []
