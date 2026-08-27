import os
import sys
import time
import json
from typing import List, Dict, Any, Optional


class LLMEngine:
    """共享LLM引擎 - 所有Skill共用统一的大模型调用层"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("provider", "zhipu")
        self.model = config.get("model", "glm-5.1-flash")
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("base_url", "")
        self.enabled = config.get("enabled", False)

        self._client = None
        self._init_client()

    def _init_client(self):
        if not self.enabled:
            return
        try:
            if self.provider == "zhipu":
                from zhipuai import ZhipuAI
                self._client = ZhipuAI()
            elif self.provider == "ollama":
                import ollama
                self._client = ollama
            elif self.provider == "deepseek":
                from zhipuai import ZhipuAI
                self._client = ZhipuAI()
        except ImportError:
            pass

    def chat(self, messages: List[Dict[str, str]],
             tools: Optional[List[Dict]] = None,
             system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        统一的聊天接口
        返回: {"content": str, "tool_calls": list}
        """
        if not self.enabled or not self._client:
            return {"content": "", "tool_calls": []}

        try:
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)

            if self.provider == "zhipu":
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=full_messages,
                    tools=tools
                )
                result = {"content": response.choices[0].message.content}
                if hasattr(response.choices[0].message, 'tool_calls') and response.choices[0].message.tool_calls:
                    result["tool_calls"] = [
                        {
                            "id": tc.id,
                            "name": tc.function.name,
                            "arguments": json.loads(tc.function.arguments)
                        }
                        for tc in response.choices[0].message.tool_calls
                    ]
                return result

            elif self.provider == "ollama":
                response = self._client.chat(
                    model=self.model,
                    messages=full_messages,
                    tools=tools
                )
                return {
                    "content": response['message']['content'],
                    "tool_calls": response.get('message', {}).get('tool_calls', [])
                }

        except Exception as e:
            return {"content": f"", "error": str(e)}

        return {"content": "", "tool_calls": []}

    def chat_stream(self, messages: List[Dict[str, str]],
                    system_prompt: Optional[str] = None):
        """流式对话接口"""
        if not self.enabled or not self._client:
            yield ""
            return

        try:
            full_messages = []
            if system_prompt:
                full_messages.append({"role": "system", "content": system_prompt})
            full_messages.extend(messages)

            if self.provider == "zhipu":
                response = self._client.chat.completions.create(
                    model=self.model,
                    messages=full_messages,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
            elif self.provider == "ollama":
                response = self._client.chat(
                    model=self.model,
                    messages=full_messages,
                    stream=True
                )
                for chunk in response:
                    if 'message' in chunk and 'content' in chunk['message']:
                        yield chunk['message']['content']
        except Exception:
            yield ""

    def is_available(self) -> bool:
        return self.enabled and self._client is not None
