import json
from typing import Dict, Any, List, Callable
from skills.base import BaseSkill, SkillResult


class ToolUseSkill(BaseSkill):
    """Function Calling Skill - 让LLM自主决定调用哪些工具"""

    def __init__(self, config: Dict[str, Any], llm: Any):
        self.config = config
        self.llm = llm
        self.tools: Dict[str, Dict] = {}
        self.handlers: Dict[str, Callable] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        self.register_tool(
            name="query_order",
            description="查询订单状态、物流信息",
            parameters={
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "订单号"},
                    "phone": {"type": "string", "description": "手机号"}
                }
            },
            handler=self._query_order_handler
        )
        self.register_tool(
            name="query_faq",
            description="查询常见问题解答",
            parameters={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "问题内容"}
                }
            },
            handler=self._query_faq_handler
        )
        self.register_tool(
            name="get_user_info",
            description="获取用户信息",
            parameters={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "用户ID"}
                }
            },
            handler=lambda user_id: {"level": "VIP", "orders": 12}
        )

    def register_tool(self, name: str, description: str,
                      parameters: Dict, handler: Callable):
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters
        }
        self.handlers[name] = handler

    def _query_order_handler(self, order_id: str = None, phone: str = None):
        return {
            "order_id": order_id or "20240601001",
            "status": "配送中",
            "estimated_delivery": "明天 18:00 前"
        }

    def _query_faq_handler(self, question: str):
        faqs = {
            "如何退款": "退款流程：1.进入我的订单 2.找到订单 3.点击申请退款",
            "配送多久": "一般下单后2小时内送达",
            "如何修改密码": "1.登录账户 2.账户设置 3.修改密码"
        }
        for keyword, answer in faqs.items():
            if keyword in question:
                return {"answer": answer}
        return {"answer": "抱歉，暂时无法回答这个问题"}

    @property
    def name(self) -> str:
        return "tool_use"

    @property
    def description(self) -> str:
        return "Function Calling Skill - LLM自主调用工具"

    @property
    def priority(self) -> int:
        return 6

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        if self.llm.is_available():
            return 0.3
        return 0.0

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        if not self.llm.is_available():
            return SkillResult(
                success=False,
                response="",
                confidence=0.0
            )

        messages = context.get("history", [])
        tools_schema = list(self.tools.values())

        for _ in range(3):
            result = self.llm.chat(messages, tools=tools_schema)

            if not result.get("tool_calls"):
                content = result.get("content", "")
                if content:
                    return SkillResult(
                        success=True,
                        response=content,
                        data={"source": "tool_use_llm"},
                        confidence=0.7
                    )
                break

            tool_calls = result.get("tool_calls", [])
            messages.append({
                "role": "assistant",
                "content": result.get("content", ""),
                "tool_calls": tool_calls
            })

            for tc in tool_calls:
                tool_name = tc.get("name", "")
                tool_args = tc.get("arguments", {})

                tool_result = self.execute_tool(tool_name, tool_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.get("id", "call_0"),
                    "content": json.dumps(tool_result, ensure_ascii=False)
                })

        return SkillResult(
            success=False,
            response="",
            confidence=0.0
        )

    def execute_tool(self, name: str, args: Dict) -> Dict:
        if name not in self.handlers:
            return {"success": False, "error": f"未知工具: {name}"}
        try:
            result = self.handlers[name](**args)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
