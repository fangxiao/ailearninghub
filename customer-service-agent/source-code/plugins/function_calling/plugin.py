import json
from typing import Dict, List, Callable, Any, Optional


class FunctionCallingPlugin:
    """Function Calling插件 - 让大模型自主决定调用哪些工具"""

    def __init__(self):
        self.tools: Dict[str, Dict] = {}
        self.handlers: Dict[str, Callable] = {}

    def register_tool(self, name: str, description: str,
                     parameters: Dict, handler: Callable):
        """注册一个工具"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": parameters
        }
        self.handlers[name] = handler

    def get_tools_schema(self) -> List[Dict]:
        """获取所有工具的JSON Schema"""
        return list(self.tools.values())

    def call_llm_with_tools(self, user_input: str,
                             llm_client: Any) -> Dict:
        """发送请求时带上tools参数，让大模型决定是否调用工具"""
        tools_schema = self.get_tools_schema()
        messages = [{"role": "user", "content": user_input}]

        response = llm_client.chat(
            model="gpt-4o",
            messages=messages,
            tools=tools_schema
        )
        return response

    def execute_tool(self, name: str, args: Dict) -> Dict:
        """执行指定工具"""
        if name not in self.handlers:
            return {"success": False, "error": f"未知工具: {name}"}
        try:
            result = self.handlers[name](**args)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def chat_with_tools(self, user_input: str, llm_client: Any) -> str:
        """完整的Function Calling流程"""
        messages = [{"role": "user", "content": user_input}]
        tools_schema = self.get_tools_schema()

        for _ in range(3):
            response = llm_client.chat(
                model="gpt-4o",
                messages=messages,
                tools=tools_schema
            )

            if not hasattr(response, 'tool_calls') or not response.tool_calls:
                return response.content

            messages.append({
                "role": "assistant",
                "content": response.content,
                "tool_calls": response.tool_calls
            })

            for tool_call in response.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                result = self.execute_tool(tool_name, tool_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        return "抱歉，我暂时无法处理您的请求。"


def call_llm_with_tools(user_input: str, tools: List[Dict]) -> Dict:
    """示例：发送请求时带上tools参数"""
    import requests

    response = requests.post(
        "https://api.example.com/v1/chat/completions",
        json={
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": user_input}],
            "tools": tools
        }
    )
    return response.json()["choices"][0]["message"]


def execute_tool(name: str, args: Dict) -> Dict:
    """示例：执行指定工具"""
    available_tools = {
        "query_order": lambda order_id: {"status": "配送中", "order_id": order_id},
        "query_faq": lambda question: {"answer": "请您提供订单号"},
    }
    if name in available_tools:
        return {"success": True, "result": available_tools[name](**args)}
    return {"success": False, "error": f"未知工具: {name}"}


def chat_with_tools(user_input: str, tools: List[Dict]) -> str:
    """示例：完整的Function Calling流程"""
    message = call_llm_with_tools(user_input, tools)

    if hasattr(message, "tool_calls") and message.tool_calls:
        for tool_call in message.tool_calls:
            tool_result = execute_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
        return f"已查询到结果：{tool_result}"

    return message.content


if __name__ == "__main__":
    tools = [
        {
            "type": "function",
            "function": {
                "name": "query_order",
                "description": "查询订单状态",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "订单号"
                        }
                    },
                    "required": ["order_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "query_faq",
                "description": "查询常见问题",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "问题内容"
                        }
                    },
                    "required": ["question"]
                }
            }
        }
    ]

    result = chat_with_tools("我的订单20240601001到哪了", tools)
    print(result)
