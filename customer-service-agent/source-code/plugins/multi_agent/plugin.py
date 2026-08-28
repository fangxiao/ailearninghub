import re
from typing import Dict


class SubAgent:
    """子Agent基类"""
    def handle(self, user_input: str) -> str:
        return "您好，我是子Agent，正在为您服务。"


class ChatAgent(SubAgent):
    """闲聊Agent"""
    def handle(self, user_input: str) -> str:
        greetings = ["你好", "您好", "hi", "hello", "在吗"]
        for g in greetings:
            if g in user_input.lower():
                return "您好！很高兴为您服务，有什么可以帮您？"
        return "嗯，我在听，请继续说。"


class OrderAgent(SubAgent):
    """订单Agent"""
    def handle(self, user_input: str) -> str:
        match = re.search(r'订单[号]?[:\s]*(\w{6,})', user_input)
        if match:
            return f"您的订单 {match.group(1)} 正在配送中，预计明天送达。"
        return "请提供您的订单号，我帮您查询。"


class ComplaintAgent(SubAgent):
    """投诉Agent"""
    def handle(self, user_input: str) -> str:
        return "非常抱歉给您带来不好的体验。请告诉我具体情况，我会尽力帮您解决。"


class ConsultAgent(SubAgent):
    """咨询Agent"""
    def handle(self, user_input: str) -> str:
        return "关于您的问题，我已记录。您可以查看帮助中心或等待人工客服回复。"


class RouterAgent:
    """路由Agent - 根据用户意图分发到不同的子Agent"""

    def __init__(self):
        self.agents: Dict[str, SubAgent] = {
            "chat": ChatAgent(),
            "order": OrderAgent(),
            "complaint": ComplaintAgent(),
            "consult": ConsultAgent(),
        }

    def route(self, user_input: str) -> str:
        target = self._decide_target(user_input)
        agent = self.agents.get(target, self.agents["consult"])
        return agent.handle(user_input)

    def _decide_target(self, user_input: str) -> str:
        rules = [
            (r'你好|您好|hi|hello|在吗', "chat"),
            (r'订单|物流|发货|配送', "order"),
            (r'投诉|差评|太差|生气|愤怒', "complaint"),
            (r'咨询|介绍|推荐|怎么', "consult"),
        ]
        for pattern, target in rules:
            if re.search(pattern, user_input, re.IGNORECASE):
                return target
        return "consult"


if __name__ == "__main__":
    router = RouterAgent()

    print("多Agent路由测试：")
    test_cases = [
        "你好",
        "我的订单到哪了",
        "你们服务太差了！",
        "推荐一款花束",
    ]
    for case in test_cases:
        result = router.route(case)
        print(f"  用户: {case}")
        print(f"  Bot: {result}\n")
