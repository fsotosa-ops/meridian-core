from app.agents.search import SearchAgent
from app.agents.scraper import ScrapeAgent
from app.agents.brain import BrainAgent
from app.db.vector_store import MeridianVectorStore

class MeridianOrchestrator:
    def __init__(self, user):
        self.user = user
        self.searcher = SearchAgent()
        self.scraper = ScrapeAgent()
        self.memory = MeridianVectorStore(user['id'])

    async def process_prospect(self, request):
        # 1. Búsqueda pública (Search Agent)
        url = self.searcher.find_url(request.target, request.is_company)
        
        # 2. Extracción de datos (Scrape Agent)
        raw_text = self.scraper.get_public_data(url)
        
        # 3. Recuperación de Memoria (RAG)
        context = self.memory.get_context(raw_text)
        
        # 4. Evaluación de IA (Brain Agent)
        brain = BrainAgent(request.user_llm_key.get_secret_value())
        evaluation = brain.evaluate(raw_text, request.icp_criteria, context)
        
        return evaluation