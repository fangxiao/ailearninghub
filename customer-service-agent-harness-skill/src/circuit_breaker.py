import time
import threading
from collections import defaultdict
from typing import Dict, Optional


class CircuitBreaker:
    """熔断器 - 保护Harness免受故障Skill的影响"""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(self, failure_threshold: int = 5,
                 recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.states: Dict[str, Dict] = {}
        self._lock = threading.Lock()

    def can_execute(self, skill_name: str) -> bool:
        """检查技能是否可以执行"""
        with self._lock:
            if skill_name not in self.states:
                self.states[skill_name] = {
                    "state": self.CLOSED,
                    "failures": 0,
                    "last_failure_time": 0
                }
                return True

            state = self.states[skill_name]

            if state["state"] == self.OPEN:
                if time.time() - state["last_failure_time"] > self.recovery_timeout:
                    state["state"] = self.HALF_OPEN
                    return True
                return False

            return True

    def record_success(self, skill_name: str):
        """记录成功"""
        with self._lock:
            if skill_name in self.states:
                self.states[skill_name]["state"] = self.CLOSED
                self.states[skill_name]["failures"] = 0

    def record_failure(self, skill_name: str):
        """记录失败"""
        with self._lock:
            if skill_name not in self.states:
                self.states[skill_name] = {
                    "state": self.CLOSED,
                    "failures": 0,
                    "last_failure_time": 0
                }
            state = self.states[skill_name]
            state["failures"] += 1
            state["last_failure_time"] = time.time()
            if state["failures"] >= self.failure_threshold:
                state["state"] = self.OPEN

    def get_state(self, skill_name: str) -> str:
        """获取熔断器状态"""
        with self._lock:
            if skill_name not in self.states:
                return self.CLOSED
            return self.states[skill_name]["state"]

    def reset(self, skill_name: str):
        """重置熔断器"""
        with self._lock:
            if skill_name in self.states:
                self.states[skill_name] = {
                    "state": self.CLOSED,
                    "failures": 0,
                    "last_failure_time": 0
                }
