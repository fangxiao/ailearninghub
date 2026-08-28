import json
from pathlib import Path
from typing import List, Dict

class KnowledgeBasePlugin:
    """知识库插件"""
    
    def __init__(self, faq_file: str = "data/faq.json"):
        self.faqs = self._load_faqs(faq_file)
        self.keyword_index = self._build_keyword_index()
    
    def _load_faqs(self, faq_file: str) -> List[Dict]:
        """加载FAQ知识库"""
        path = Path(faq_file)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def _build_keyword_index(self) -> Dict[str, List[str]]:
        """构建关键词索引"""
        index = {}
        for faq in self.faqs:
            for keyword in faq.get("keywords", []):
                if keyword not in index:
                    index[keyword] = []
                index[keyword].append(faq["id"])
        return index
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """检索FAQ"""
        keyword_results = self._keyword_search(query)
        vector_results = self._vector_search(query)
        all_results = keyword_results + vector_results
        unique_results = self._deduplicate(all_results)
        return unique_results[:top_k]
    
    def _keyword_search(self, query: str) -> List[Dict]:
        """关键词检索"""
        results = []
        query_words = query.split()
        
        for word in query_words:
            if word in self.keyword_index:
                faq_ids = self.keyword_index[word]
                for faq_id in faq_ids:
                    faq = self._get_faq_by_id(faq_id)
                    if faq:
                        results.append({
                            "faq": faq,
                            "score": 1.0,
                            "source": "keyword"
                        })
        
        return results
    
    def _vector_search(self, query: str) -> List[Dict]:
        """向量检索（简化版）"""
        return []
    
    def _get_faq_by_id(self, faq_id: str) -> Dict:
        """根据ID获取FAQ"""
        for faq in self.faqs:
            if faq["id"] == faq_id:
                return faq
        return None
    
    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        """去重"""
        seen = set()
        unique = []
        for result in results:
            faq_id = result["faq"]["id"]
            if faq_id not in seen:
                seen.add(faq_id)
                unique.append(result)
        return unique


if __name__ == "__main__":
    kb = KnowledgeBasePlugin()
    
    print("测试知识库检索：")
    print(kb.search("如何修改密码"))
    print(kb.search("申请退款"))
    print(kb.search("配送多久"))