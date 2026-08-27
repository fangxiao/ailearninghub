import json
import math
import hashlib
from pathlib import Path
from typing import Dict, Any, List
from skills.base import BaseSkill, SkillResult


class FAQSkill(BaseSkill):
    """FAQ Skill - 基于知识库回答用户问题，支持向量+关键词混合检索"""

    def __init__(self, config: Dict[str, Any], llm: Any):
        self.config = config
        self.llm = llm
        self.knowledge = self._load_knowledge()
        self.keyword_index = self._build_keyword_index()
        self.vectors: List[Dict] = []
        self._build_vector_index()

    def _load_knowledge(self) -> List[Dict]:
        path = Path("data/faq.json")
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _build_keyword_index(self) -> Dict[str, List[str]]:
        index = {}
        for faq in self.knowledge:
            for keyword in faq.get("keywords", []):
                if keyword not in index:
                    index[keyword] = []
                index[keyword].append(faq["id"])
        return index

    def _get_embedding(self, text: str) -> List[float]:
        hash_bytes = hashlib.md5(text.encode()).digest()
        vector = [b / 255.0 for b in hash_bytes]
        while len(vector) < 128:
            vector.append(0.0)
        return vector[:128]

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def _build_vector_index(self):
        for item in self.knowledge:
            vector = self._get_embedding(item["question"])
            self.vectors.append({
                "id": item["id"],
                "question": item["question"],
                "answer": item["answer"],
                "vector": vector
            })

    @property
    def name(self) -> str:
        return "faq"

    @property
    def description(self) -> str:
        return "FAQ Skill - 基于知识库回答用户常见问题"

    @property
    def triggers(self) -> List[str]:
        return ["密码", "退款", "配送", "支付", "发货", "怎么", "如何", "多久", "修改", "申请"]

    @property
    def priority(self) -> int:
        return 7

    def can_handle(self, user_input: str, context: Dict[str, Any]) -> float:
        score = super().can_handle(user_input, context)
        if context.get("intent") in ("faq_query", "faq"):
            score = max(score, 0.85)
        elif context.get("intent") != "faq_query":
            score = min(score, 0.25)
        return score

    def execute(self, user_input: str, context: Dict[str, Any]) -> SkillResult:
        results = self._hybrid_search(user_input)

        if results:
            return SkillResult(
                success=True,
                response=results[0]["answer"],
                data={"faq_results": results},
                confidence=results[0].get("score", 0.5)
            )

        if self.llm.is_available():
            llm_response = self._llm_fallback(user_input)
            if llm_response:
                return SkillResult(
                    success=True,
                    response=llm_response,
                    data={"source": "llm_fallback"},
                    confidence=0.6
                )

        return SkillResult(
            success=False,
            response="抱歉，暂时无法回答这个问题。您可以转人工客服咨询。",
            confidence=0.2
        )

    def _hybrid_search(self, query: str) -> List[Dict]:
        keyword_results = self._keyword_search(query)
        vector_results = self._vector_search(query)

        all_results = keyword_results + vector_results
        seen = set()
        unique = []
        for r in all_results:
            if r["id"] not in seen:
                seen.add(r["id"])
                unique.append(r)
        unique.sort(key=lambda x: x.get("score", 0), reverse=True)
        return unique[:3]

    def _keyword_search(self, query: str) -> List[Dict]:
        results = []
        for keyword, faq_ids in self.keyword_index.items():
            if keyword in query:
                for faq_id in faq_ids:
                    faq = self._get_faq_by_id(faq_id)
                    if faq:
                        results.append({
                            "id": faq["id"],
                            "question": faq["question"],
                            "answer": faq["answer"],
                            "score": 1.0,
                            "source": "keyword"
                        })
        return results

    def _vector_search(self, query: str) -> List[Dict]:
        query_vector = self._get_embedding(query)
        results = []
        for item in self.vectors:
            similarity = self._cosine_similarity(query_vector, item["vector"])
            if similarity >= 0.3:
                results.append({
                    "id": item["id"],
                    "question": item["question"],
                    "answer": item["answer"],
                    "score": similarity,
                    "source": "vector"
                })
        return results

    def _get_faq_by_id(self, faq_id: str) -> Dict:
        for faq in self.knowledge:
            if faq["id"] == faq_id:
                return faq
        return None

    def _llm_fallback(self, user_input: str) -> str:
        knowledge_text = "\n".join(
            f"问题：{item['question']}\n答案：{item['answer']}"
            for item in self.knowledge
        )
        messages = [
            {"role": "user", "content": user_input}
        ]
        system = f"""你是客服助手。请基于以下知识库回答用户问题。
如果知识库中没有相关信息，请说"抱歉，暂时无法回答这个问题"。

知识库：
{knowledge_text}"""
        result = self.llm.chat(messages, system_prompt=system)
        return result.get("content", "")

    def add_knowledge(self, question: str, answer: str, keywords: List[str] = None):
        item = {"id": f"faq_{len(self.knowledge) + 1}", "question": question, "answer": answer}
        if keywords:
            item["keywords"] = keywords
        self.knowledge.append(item)
        if keywords:
            for kw in keywords:
                if kw not in self.keyword_index:
                    self.keyword_index[kw] = []
                self.keyword_index[kw].append(item["id"])
        vector = self._get_embedding(question)
        self.vectors.append({
            "id": item["id"], "question": question,
            "answer": answer, "vector": vector
        })
