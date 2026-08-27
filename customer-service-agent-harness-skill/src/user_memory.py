import json
import time
import os
from typing import Dict, List, Optional


class UserMemory:
    """用户记忆系统 - 存储用户画像、历史交互、偏好"""

    def __init__(self, storage_file: str = "data/user_memory.json"):
        self.storage_file = storage_file
        self.users: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.users = {}

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_file) or '.', exist_ok=True)
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

    def get_user(self, user_id: str) -> Dict:
        if user_id not in self.users:
            self.users[user_id] = self._create_default_user(user_id)
            self._save()
        return self.users[user_id]

    def _create_default_user(self, user_id: str) -> Dict:
        return {
            "user_id": user_id,
            "created_at": time.time(),
            "profile": {
                "name": None,
                "phone": None,
                "level": "normal",
                "tags": []
            },
            "preferences": {
                "language": "zh-CN",
                "notification": True
            },
            "history": {
                "total_conversations": 0,
                "total_orders": 0,
                "last_interaction": None,
                "common_intents": []
            },
            "segments": [],
            "custom_data": {}
        }

    def update_profile(self, user_id: str, **kwargs):
        user = self.get_user(user_id)
        for key, value in kwargs.items():
            if key in user["profile"]:
                user["profile"][key] = value
        self._save()

    def add_tag(self, user_id: str, tag: str):
        user = self.get_user(user_id)
        if tag not in user["profile"]["tags"]:
            user["profile"]["tags"].append(tag)
            self._save()

    def record_interaction(self, user_id: str, intent: str,
                           user_input: str, bot_response: str):
        user = self.get_user(user_id)
        user["history"]["total_conversations"] += 1
        user["history"]["last_interaction"] = {
            "time": time.time(),
            "intent": intent,
            "user_input": user_input,
            "bot_response": bot_response
        }
        if intent not in user["history"]["common_intents"]:
            user["history"]["common_intents"].append(intent)
            user["history"]["common_intents"] = \
                user["history"]["common_intents"][-10:]
        self._save()

    def get_personalized_greeting(self, user_id: str) -> str:
        user = self.get_user(user_id)
        name = user["profile"]["name"]
        history = user["history"]
        if name:
            greeting = f"您好，{name}！"
        else:
            greeting = "您好！"
        if history["total_conversations"] == 0:
            greeting += "很高兴为您服务，有什么可以帮您？"
        elif history["total_orders"] > 5:
            greeting += "欢迎回来，尊贵的老客户！有什么可以帮您？"
        else:
            greeting += "有什么可以帮您？"
        return greeting

    def build_user_segment(self, user_id: str) -> str:
        user = self.get_user(user_id)
        score = 0
        if user["profile"]["level"] == "vip":
            score += 3
        elif user["profile"]["level"] == "premium":
            score += 2
        score += min(user["history"]["total_orders"] // 5, 3)
        if score >= 5:
            return "high_value"
        elif score >= 3:
            return "medium_value"
        return "normal"

    def get_user_summary(self, user_id: str) -> str:
        user = self.get_user(user_id)
        segment = self.build_user_segment(user_id)
        profile = user["profile"]
        history = user["history"]
        parts = []
        if profile["name"]:
            parts.append(f"用户：{profile['name']}")
        parts.append(f"等级：{profile['level']}")
        parts.append(f"分群：{segment}")
        parts.append(f"累计对话：{history['total_conversations']}次")
        parts.append(f"累计订单：{history['total_orders']}个")
        if history["last_interaction"]:
            last_time = time.strftime("%Y-%m-%d %H:%M",
                                     time.localtime(history["last_interaction"]["time"]))
            parts.append(f"上次交互：{last_time}")
        return " | ".join(parts)
