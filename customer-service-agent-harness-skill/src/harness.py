import os
import sys
import time
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_engine import LLMEngine
from src.skill_registry import SkillRegistry
from src.skill_router import SkillRouter
from src.circuit_breaker import CircuitBreaker
from src.rate_limiter import RateLimiter
from src.dialog_manager import DialogManager
from src.user_memory import UserMemory
from src.metrics import MetricsCollector
from skills.base import SkillResult

from skills.sentiment_skill import SentimentSkill
from skills.intent_skill import IntentRecognitionSkill
from skills.faq_skill import FAQSkill
from skills.order_skill import OrderSkill
from skills.complaint_skill import ComplaintSkill
from skills.handoff_skill import HandoffSkill
from skills.memory_skill import MemorySkill
from skills.slot_filling_skill import SlotFillingSkill
from skills.tool_use_skill import ToolUseSkill
from skills.greeting_skill import GreetingSkill
from skills.general_skill import GeneralSkill


class CustomerServiceHarness:
    """
    客服Harness - 统一编排层
    负责：Skill注册、路由决策、熔断保护、限流、监控
    """

    def __init__(self, config_path: str = "config/customer_service.yaml"):
        self.config = self._load_config(config_path)
        self.system_prompt = self._load_prompt()

        self.dialog = DialogManager()
        self.memory = UserMemory()
        self.metrics = MetricsCollector()

        self.llm = LLMEngine(self.config.get("llm", {}))
        self.registry = SkillRegistry()
        self.router = SkillRouter()
        self.breaker = CircuitBreaker()
        self.limiter = RateLimiter(max_requests=100, window_seconds=60.0)

        self._init_router()
        self._register_skills()

        self.current_user_id: Optional[str] = None
        self.last_skill: str = "unknown"
        self.last_intent: str = "unknown"

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_prompt(self) -> str:
        prompt_path = Path("config/prompts/system_prompt.md")
        if prompt_path.exists():
            return prompt_path.read_text(encoding="utf-8")
        return "你是一个客服助手。"

    def _init_router(self):
        self.router.set_fallback("general")
        self.router.add_intent_rule("faq_query", "faq")
        self.router.add_intent_rule("order_query", "order")
        self.router.add_intent_rule("order", "slot_filling")
        self.router.add_intent_rule("complaint", "complaint")
        self.router.add_intent_rule("human_handoff", "handoff")
        self.router.add_intent_rule("greeting", "greeting")
        self.router.add_intent_rule("thanks", "greeting")

    def _register_skills(self):
        self.registry.register(SentimentSkill(self.config))
        self.registry.register(IntentRecognitionSkill(self.config))
        self.registry.register(GreetingSkill(self.config, self.memory))
        self.registry.register(FAQSkill(self.config, self.llm))
        self.registry.register(OrderSkill(self.config))
        self.registry.register(ComplaintSkill(self.config))
        self.registry.register(HandoffSkill(self.config))
        self.registry.register(MemorySkill(self.config, self.memory))
        self.registry.register(SlotFillingSkill(self.config, self.dialog))
        self.registry.register(ToolUseSkill(self.config, self.llm))
        self.registry.register(GeneralSkill(self.config, self.llm))

    def chat(self, user_input: str, user_id: str = "anonymous") -> str:
        start_time = time.time()
        self.current_user_id = user_id

        self.dialog.add_message("user", user_input)

        if not self.limiter.is_allowed(user_id):
            wait_time = self.limiter.get_wait_time(user_id)
            return f"您的请求过于频繁，请{int(wait_time)}秒后再试。"

        context = self._build_context(user_input)

        pre_skills = self.registry.get_pre_skills()
        for pre_skill in pre_skills:
            try:
                result = pre_skill.execute(user_input, context)
                if result.need_handoff:
                    response = result.response
                    self._record(user_input, response, pre_skill.name, start_time,
                                 resolved=False, handoff=True)
                    self.dialog.add_message("assistant", response)
                    return response
                if result.data.get("sentiment_processed"):
                    context["sentiment"] = result.data.get("sentiment")
            except Exception as e:
                pass

        intent_skill = self.registry.get_skill("intent_recognition")
        if intent_skill:
            try:
                intent_result = intent_skill.execute(user_input, context)
                context["intent"] = intent_result.data.get("intent", "unknown")
                context["confidence"] = intent_result.data.get("confidence", 0.0)
                self.last_intent = context["intent"]
            except Exception:
                context["intent"] = "unknown"

        skill = self.router.route(user_input, context, self.registry.get_all_skills())

        if not skill:
            skill = self.registry.get_skill("general")

        skill_name = skill.name
        self.last_skill = skill_name
        if not self.breaker.can_execute(skill_name):
            fallback_skill = self.registry.get_skill("general")
            if fallback_skill and fallback_skill.name != skill_name:
                skill = fallback_skill
            else:
                return "抱歉，系统繁忙，请稍后再试。"

        try:
            skill_start = time.time()
            result = skill.execute(user_input, context)
            skill_duration = (time.time() - skill_start) * 1000

            if result.success:
                self.breaker.record_success(skill_name)
                self.metrics.log_skill_execution(skill_name, True, skill_duration)
            else:
                self.breaker.record_failure(skill_name)
                self.metrics.log_skill_execution(skill_name, False, skill_duration, result.error or "")

            response = result.response
            resolved = result.success and skill_name not in ("general",)
            handoff = result.need_handoff

        except Exception as e:
            self.breaker.record_failure(skill_name)
            self.metrics.log_skill_execution(skill_name, False,
                                             (time.time() - start_time) * 1000, str(e))
            fallback = self.registry.get_skill("general")
            if fallback:
                try:
                    fallback_result = fallback.execute(user_input, context)
                    response = fallback_result.response
                    resolved = False
                    handoff = False
                except Exception:
                    response = "抱歉，处理您的请求时出现了问题。"
                    resolved = False
                    handoff = False
            else:
                response = "抱歉，系统暂时不可用。"
                resolved = False
                handoff = False

        self.dialog.add_message("assistant", response)
        self.memory.record_interaction(user_id, context.get("intent", "unknown"),
                                       user_input, response)

        self._record(user_input, response, skill_name, start_time,
                     resolved=resolved, handoff=handoff,
                     intent=context.get("intent", "unknown"))

        return response

    def _build_context(self, user_input: str) -> Dict[str, Any]:
        return {
            "user_id": self.current_user_id,
            "dialog": self.dialog.get_context(),
            "history": self.dialog.get_messages_for_llm(),
            "user_summary": self.memory.get_user_summary(
                self.current_user_id or "anonymous"
            ),
            "slots": self.dialog.slots,
            "intent": None,
            "confidence": 0.0,
            "sentiment": None,
            "skills_available": self.registry.list_skills_info()
        }

    def _record(self, user_input: str, response: str,
                skill: str, start_time: float,
                resolved: bool = False, handoff: bool = False,
                intent: str = "unknown"):
        self.metrics.log_conversation({
            "user_id": self.current_user_id,
            "skill": skill,
            "intent": intent,
            "resolved": resolved,
            "handoff": handoff,
            "response_time_ms": (time.time() - start_time) * 1000
        })

    def get_status(self) -> Dict[str, Any]:
        dashboard = self.metrics.get_dashboard()
        return {
            "user_id": self.current_user_id,
            "dialog_messages": len(self.dialog.get_history()),
            "user_summary": self.memory.get_user_summary(
                self.current_user_id or "anonymous"
            ),
            "skills": self.registry.list_skills_info(),
            "circuit_states": {
                name: self.breaker.get_state(name)
                for name in [s.name for s in self.registry.get_all_skills()]
            },
            "dashboard": dashboard,
            "dialog_slots": self.dialog.slots,
            "dialog_state": self.dialog.state,
            "last_skill": self.last_skill,
            "last_intent": self.last_intent
        }

    def reset(self):
        self.dialog.clear()


if __name__ == "__main__":
    harness = CustomerServiceHarness()

    print("=" * 50)
    print("  客服Agent加强版 (Harness+Skill) 测试")
    print("=" * 50)

    print("\n1. 问候")
    print(harness.chat("你好", "user_001"))

    print("\n2. 订单查询")
    print(harness.chat("我的订单20240601001到哪了", "user_001"))

    print("\n3. FAQ")
    print(harness.chat("如何退款？", "user_001"))

    print("\n4. 多轮对话（订花）")
    print(harness.chat("我要订花", "user_001"))
    print(harness.chat("99朵", "user_001"))

    print("\n5. 情绪激动")
    print(harness.chat("你们的服务太差了！", "user_002"))

    print("\n6. 转人工")
    print(harness.chat("转人工", "user_001"))

    print("\n7. 状态总览")
    import json
    status = harness.get_status()
    print(f"  Skills: {len(status['skills'])}个")
    print(f"  对话轮数: {status['dialog_messages']}")
    print(f"  熔断状态: {status['circuit_states']}")
