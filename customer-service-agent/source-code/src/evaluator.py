import json
import time
from typing import Dict, List, Optional


class MetricsCollector:
    """指标收集器 - 收集客服对话的各项指标"""

    def __init__(self, log_file: str = "data/metrics_log.json"):
        self.log_file = log_file
        self.logs: List[Dict] = []
        self._load()

    def _load(self):
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.logs = json.load(f)
        except FileNotFoundError:
            self.logs = []

    def _save(self):
        import os
        os.makedirs(os.path.dirname(self.log_file) or '.', exist_ok=True)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)

    def log_conversation(self, conversation: Dict):
        """记录一次完整对话的指标"""
        log_entry = {
            "timestamp": time.time(),
            "user_id": conversation.get("user_id", "anonymous"),
            "messages": conversation.get("messages", []),
            "intent": conversation.get("intent", "unknown"),
            "intent_correct": conversation.get("intent_correct", False),
            "resolved": conversation.get("resolved", False),
            "handoff": conversation.get("handoff", False),
            "response_time_ms": conversation.get("response_time_ms", 0),
            "user_satisfaction": conversation.get("user_satisfaction", None),
            "tokens_used": conversation.get("tokens_used", 0)
        }
        self.logs.append(log_entry)
        self._save()

    def log_intent_recognition(self, user_input: str,
                               predicted: str,
                               actual: str):
        """记录意图识别结果（用于离线评估）"""
        self.logs.append({
            "timestamp": time.time(),
            "type": "intent_recognition",
            "user_input": user_input,
            "predicted": predicted,
            "actual": actual,
            "correct": predicted == actual
        })
        self._save()

    def log_response_time(self, stage: str, duration_ms: float):
        """记录各阶段响应时间"""
        self.logs.append({
            "timestamp": time.time(),
            "type": "response_time",
            "stage": stage,
            "duration_ms": duration_ms
        })
        self._save()


class Evaluator:
    """效果评估器 - 计算核心指标"""

    def __init__(self, metrics: MetricsCollector):
        self.metrics = metrics

    def compute_intent_accuracy(self) -> float:
        """计算意图识别准确率"""
        intent_logs = [l for l in self.metrics.logs
                      if l.get("type") == "intent_recognition"]
        if not intent_logs:
            return 0.0
        correct = sum(1 for l in intent_logs if l.get("correct"))
        return correct / len(intent_logs)

    def compute_resolution_rate(self) -> float:
        """计算问题解决率"""
        conv_logs = [l for l in self.metrics.logs
                     if "resolved" in l]
        if not conv_logs:
            return 0.0
        resolved = sum(1 for l in conv_logs if l.get("resolved"))
        return resolved / len(conv_logs)

    def compute_handoff_rate(self) -> float:
        """计算转人工率"""
        conv_logs = [l for l in self.metrics.logs
                     if "handoff" in l]
        if not conv_logs:
            return 0.0
        handoff = sum(1 for l in conv_logs if l.get("handoff"))
        return handoff / len(conv_logs)

    def compute_avg_response_time(self) -> float:
        """计算平均响应时间"""
        times = [l.get("response_time_ms", 0)
                 for l in self.metrics.logs
                 if "response_time_ms" in l and l.get("response_time_ms", 0) > 0]
        if not times:
            return 0.0
        return sum(times) / len(times)

    def compute_user_satisfaction(self) -> float:
        """计算用户满意度（1-5分）"""
        scores = [l.get("user_satisfaction", 0)
                  for l in self.metrics.logs
                  if l.get("user_satisfaction")]
        if not scores:
            return 0.0
        return sum(scores) / len(scores)

    def get_dashboard(self) -> Dict:
        """获取完整的评估仪表盘"""
        return {
            "total_conversations": len([l for l in self.metrics.logs
                                        if "resolved" in l]),
            "intent_accuracy": round(self.compute_intent_accuracy(), 3),
            "resolution_rate": round(self.compute_resolution_rate(), 3),
            "handoff_rate": round(self.compute_handoff_rate(), 3),
            "avg_response_time_ms": round(self.compute_avg_response_time(), 1),
            "user_satisfaction": round(self.compute_user_satisfaction(), 2)
        }

    def compare_versions(self, v1_logs: List[Dict],
                         v2_logs: List[Dict]) -> Dict:
        """对比两个版本的指标"""
        def calc(logs):
            if not logs:
                return {}
            correct = sum(1 for l in logs if l.get("correct"))
            resolved = sum(1 for l in logs if l.get("resolved"))
            total = len(logs)
            return {
                "accuracy": correct / total if total else 0,
                "resolution_rate": resolved / total if total else 0,
                "sample_size": total
            }

        v1 = calc(v1_logs)
        v2 = calc(v2_logs)

        return {
            "v1": v1,
            "v2": v2,
            "accuracy_delta": v2.get("accuracy", 0) - v1.get("accuracy", 0),
            "resolution_delta": v2.get("resolution_rate", 0) - v1.get("resolution_rate", 0)
        }


if __name__ == "__main__":
    metrics = MetricsCollector()

    metrics.log_intent_recognition("我的订单到哪了", "order_query", "order_query")
    metrics.log_intent_recognition("怎么退款", "refund", "refund")
    metrics.log_intent_recognition("你好", "greeting", "consult")

    metrics.log_conversation({
        "user_id": "user_001",
        "messages": 5,
        "intent": "order_query",
        "intent_correct": True,
        "resolved": True,
        "handoff": False,
        "response_time_ms": 850,
        "user_satisfaction": 5
    })

    evaluator = Evaluator(metrics)
    dashboard = evaluator.get_dashboard()
    print("评估仪表盘：")
    for key, value in dashboard.items():
        print(f"  {key}: {value}")
