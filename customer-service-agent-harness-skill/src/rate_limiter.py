import time
import threading
from collections import defaultdict
from typing import Dict


class RateLimiter:
    """限流器 - 保护系统不被过量请求压垮"""

    def __init__(self, max_requests: int = 100, window_seconds: float = 60.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, key: str = "default") -> bool:
        """检查是否允许请求"""
        with self._lock:
            now = time.time()
            window_start = now - self.window_seconds

            self.requests[key] = [
                t for t in self.requests[key] if t > window_start
            ]

            if len(self.requests[key]) >= self.max_requests:
                return False

            self.requests[key].append(now)
            return True

    def get_wait_time(self, key: str = "default") -> float:
        """获取需要等待的时间（秒）"""
        with self._lock:
            if key not in self.requests or not self.requests[key]:
                return 0.0
            now = time.time()
            oldest = self.requests[key][0]
            wait_time = (oldest + self.window_seconds) - now
            return max(0.0, wait_time)

    def get_stats(self, key: str = "default") -> Dict:
        """获取限流统计"""
        with self._lock:
            now = time.time()
            window_start = now - self.window_seconds
            active = [t for t in self.requests.get(key, []) if t > window_start]
            return {
                "current_rate": len(active),
                "max_rate": self.max_requests,
                "window_seconds": self.window_seconds
            }
