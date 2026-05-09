from typing import List, Dict, Any
from utils.supabase_client import supabase
from loguru import logger

class KnowledgeBase:
    def __init__(self):
        self.table_name = "knowledge_documents"

    async def search(self, query: str, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Performs a robust keyword search against the knowledge documents.
        Prioritizes Title matches over Content matches.
        """
        try:
            # 1. Extract significant keywords
            stop_words = ["what", "where", "how", "the", "are", "you", "tell", "show", "me", "is", "of", "about", "your", "name"]
            # Clean punctuation that breaks Supabase OR queries
            clean_query = query.replace("?", "").replace("!", "").replace(",", "").replace(".", "")
            words = [k.strip().lower() for k in clean_query.split()]
            keywords = [w for w in words if len(w) > 3 and w not in stop_words]
            
            if not keywords:
                keywords = [words[0]] if words else [query]

            # 2. First pass: Search Titles (High priority)
            title_condition = ",".join([f"title.ilike.%{k}%" for k in keywords])
            title_resp = supabase.table(self.table_name).select("*").or_(title_condition).limit(limit).execute()
            
            # 3. Second pass: Search Content (Low priority)
            content_condition = ",".join([f"content.ilike.%{k}%" for k in keywords])
            content_resp = supabase.table(self.table_name).select("*").or_(content_condition).limit(limit).execute()
            
            # 4. Merge results (Titles first)
            seen_ids = set()
            results = []
            
            for doc in title_resp.data + content_resp.data:
                if doc["id"] not in seen_ids:
                    results.append(doc)
                    seen_ids.add(doc["id"])
            
            return results[:limit]
        except Exception as e:
            logger.error(f"Knowledge search failed: {e}")
            return []

kb = KnowledgeBase()
