from typing import List, Dict

class DialogManager:
    """对话管理器"""
    
    def __init__(self, max_history: int = 10):
        self.history: List[Dict] = []
        self.max_history = max_history
        self.key_info: Dict = {}
    
    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        self.history.append({
            "role": role,
            "content": content
        })
        
        self._extract_key_info(content)
        
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_history(self) -> List[Dict]:
        """获取对话历史"""
        return self.history
    
    def get_key_info(self) -> Dict:
        """获取关键信息"""
        return self.key_info
    
    def _extract_key_info(self, content: str):
        """提取关键信息（简化版）"""
        import re
        order_pattern = r'订单[号]?[:\s]*(\d+)'
        match = re.search(order_pattern, content)
        if match:
            self.key_info["order_id"] = match.group(1)
    
    def clear(self):
        """清空对话历史"""
        self.history = []
        self.key_info = {}


if __name__ == "__main__":
    dm = DialogManager()
    
    print("测试对话管理：")
    dm.add_message("user", "我的订单12345在哪")
    dm.add_message("assistant", "您的订单正在配送中")
    
    print(f"历史: {dm.get_history()}")
    print(f"关键信息: {dm.get_key_info()}")