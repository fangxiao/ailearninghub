import os
from pathlib import Path
import yaml

class CustomerServiceBot:
    """客服Bot核心类"""
    
    def __init__(self, config_path: str = "config/customer_service.yaml"):
        self.config = self._load_config(config_path)
        self.system_prompt = self._load_prompt()
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _load_prompt(self) -> str:
        """加载System Prompt"""
        prompt_path = Path("config/prompts/system_prompt.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return "你是一个客服助手。"
    
    def chat(self, user_input: str, history: list = None) -> str:
        """对话入口"""
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        if history:
            messages.extend(history)
        
        messages.append({"role": "user", "content": user_input})
        
        response = self._call_llm(messages)
        return response
    
    def _call_llm(self, messages: list) -> str:
        """调用大模型API"""
        provider = self.config.get('llm', {}).get('provider', 'zhipu')
        model = self.config.get('llm', {}).get('model', 'glm-5.1-flash')
        
        if provider == 'zhipu':
            return self._call_zhipu(messages, model)
        elif provider == 'ollama':
            return self._call_ollama(messages, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _call_zhipu(self, messages: list, model: str) -> str:
        """调用智谱AI"""
        from zhipuai import ZhipuAI
        client = ZhipuAI()
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    
    def _call_ollama(self, messages: list, model: str) -> str:
        """调用Ollama本地模型"""
        import ollama
        response = ollama.chat(model=model, messages=messages)
        return response['message']['content']


if __name__ == "__main__":
    bot = CustomerServiceBot()
    
    print("测试1：FAQ问题")
    print(bot.chat("如何修改密码？"))
    
    print("\n测试2：情绪激动")
    print(bot.chat("你们的服务太差了！我要投诉！"))
    
    print("\n测试3：无关问题")
    print(bot.chat("今天天气怎么样？"))