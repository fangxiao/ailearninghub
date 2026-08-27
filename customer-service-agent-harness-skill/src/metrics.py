import json
import time
import os
from typing import Dict, List, Any


class MetricsCollector:
    """指标收集器 - 收集客服对话的各项指标"""

    def __init__(self, log_file: str = "data/metrics_log.json"):
        self.log_file = log_file
        self.logs: List[Dict] = []
        self._load()

    def _load(self):
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.logs = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.logs = []

    def _save(self):
        os.makedirs(os.path.dirname(self.log_file) or '.', exist_ok=True)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)

    def log_conversation(self, conversation: Dict):
        log_entry = {
            "timestamp": time.time(),
            "user_id": conversation.get("user_id", "anonymous"),
            "skill": conversation.get("skill", "unknown"),
            "intent": conversation.get("intent", "unknown"),
            "resolved": conversation.get("resolved", False),
            "handoff": conversation.get("handoff", False),
            "response_time_ms": conversation.get("response_time_ms", 0),
            "tokens_used": conversation.get("tokens_used", 0),
            "success": conversation.get("success", True)
        }
        self.logs.append(log_entry)
        self._save()

    def log_skill_execution(self, skill_name: str, success: bool,
                            duration_ms: float, error: str = ""):
        self.logs.append({
            "timestamp": time.time(),
            "type": "skill_execution",
            "skill": skill_name,
            "success": success,
            "duration_ms": duration_ms,
            "error": error
        })
        self._save()

    def get_dashboard(self) -> Dict[str, Any]:
        conv_logs = [l for l in self.logs if "resolved" in l]
        skill_logs = [l for l in self.logs if l.get("type") == "skill_execution"]

        total = len(conv_logs)
        resolved = sum(1 for l in conv_logs if l.get("resolved"))
        handoffs = sum(1 for l in conv_logs if l.get("handoff"))
        response_times = [l.get("response_time_ms", 0) for l in conv_logs if l.get("response_time_ms", 0) > 0]

        skill_stats: Dict[str, Dict] = {}
        for sl in skill_logs:
            name = sl.get("skill", "unknown")
            if name not in skill_stats:
                skill_stats[name] = {"total": 0, "success": 0, "total_time": 0}
            skill_stats[name]["total"] += 1
            if sl.get("success"):
                skill_stats[name]["success"] += 1
            skill_stats[name]["total_time"] += sl.get("duration_ms", 0)

        for name in skill_stats:
            s = skill_stats[name]
            s["avg_time_ms"] = round(s["total_time"] / s["total"], 1) if s["total"] > 0 else 0
            s["success_rate"] = round(s["success"] / s["total"], 3) if s["total"] > 0 else 0

        return {
            "total_conversations": total,
            "resolved_rate": round(resolved / total, 3) if total > 0 else 0,
            "handoff_rate": round(handoffs / total, 3) if total > 0 else 0,
            "avg_response_time_ms": round(sum(response_times) / len(response_times), 1) if response_times else 0,
            "skill_stats": skill_stats
        }
