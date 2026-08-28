import json
import math
from typing import List, Dict, Tuple, Optional


class VectorKBPlugin:
    """基于向量的知识库插件 - 支持语义检索"""

    def __init__(self, knowledge_file: str = "data/faq.json",
                 embedding_model: str = "text-embedding-3-small"):
        self.knowledge = self._load_knowledge(knowledge_file)
        self.embedding_model = embedding_model
        self.vectors: List[Dict] = []
        self._build_index()

    def _load_knowledge(self, filepath: str) -> List[Dict]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return [
                {"question": "如何下单？", "answer": "选择商品后加入购物车，点击结算即可下单。"},
                {"question": "配送时间？", "answer": "一般下单后2小时内送达，具体时间看配送地址。"},
                {"question": "如何退款？", "answer": "在订单详情页点击申请退款，我们会在1-3个工作日处理。"},
            ]

    def _get_embedding(self, text: str) -> List[float]:
        """获取文本的向量表示（简化版，实际应调用Embedding API）"""
        import hashlib
        hash_bytes = hashlib.md5(text.encode()).digest()
        vector = [b / 255.0 for b in hash_bytes]
        while len(vector) < 128:
            vector.append(0.0)
        return vector[:128]

    def _cosine_similarity(self, v1: List[float],
                           v2: List[float]) -> float:
        """计算两个向量的余弦相似度"""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def _build_index(self):
        """构建向量索引"""
        for item in self.knowledge:
            vector = self._get_embedding(item["question"])
            self.vectors.append({
                "id": len(self.vectors),
                "question": item["question"],
                "answer": item["answer"],
                "vector": vector
            })

    def search(self, query: str, top_k: int = 3,
               threshold: float = 0.3) -> List[Dict]:
        """语义检索，返回最相关的top_k条知识"""
        query_vector = self._get_embedding(query)

        results = []
        for item in self.vectors:
            similarity = self._cosine_similarity(query_vector, item["vector"])
            if similarity >= threshold:
                results.append({
                    "question": item["question"],
                    "answer": item["answer"],
                    "score": similarity
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def search_with_keyword_fallback(self, query: str,
                                     top_k: int = 3) -> List[Dict]:
        """混合检索：先向量检索，若无结果再关键词匹配"""
        results = self.search(query, top_k)
        if results:
            return results

        keyword_results = self._keyword_search(query, top_k)
        return keyword_results

    def _keyword_search(self, query: str, top_k: int) -> List[Dict]:
        """关键词匹配作为降级方案"""
        results = []
        for item in self.knowledge:
            score = 0
            if "keywords" in item:
                for kw in item["keywords"]:
                    if kw in query:
                        score += 1
            if item["question"] in query or query in item["question"]:
                score += 0.5
            if score > 0:
                results.append({
                    "question": item["question"],
                    "answer": item["answer"],
                    "score": score
                })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def add_knowledge(self, question: str, answer: str):
        """添加新的知识条目"""
        self.knowledge.append({"question": question, "answer": answer})
        vector = self._get_embedding(question)
        self.vectors.append({
            "id": len(self.vectors),
            "question": question,
            "answer": answer,
            "vector": vector
        })


if __name__ == "__main__":
    kb = VectorKBPlugin()

    print("测试语义检索：")
    results = kb.search("怎么买花")
    for r in results:
        print(f"  问题: {r['question']}, 答案: {r['answer']}, 得分: {r['score']:.3f}")

    print("\n测试混合检索：")
    results = kb.search_with_keyword_fallback("退款怎么办")
    for r in results:
        print(f"  问题: {r['question']}, 答案: {r['answer']}, 得分: {r['score']:.3f}")
