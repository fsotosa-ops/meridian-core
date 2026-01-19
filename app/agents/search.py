import requests
from app.core.config import settings

class SearchAgent:
    def find_url(self, target: str, is_company: bool = False):
        domain = "site:linkedin.com/company/" if is_company else "site:linkedin.com/in/"
        query = f'{domain} "{target}"'
        headers = {"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"}
        payload = {"q": query, "num": 1}
        
        try:
            res = requests.post("https://google.serper.dev/search", headers=headers, json=payload)
            results = res.json().get("organic", [])
            return results[0].get("link") if results else None
        except Exception as e:
            print(f"Error en SearchAgent: {e}")
            return None