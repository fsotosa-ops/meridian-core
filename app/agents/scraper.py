from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from app.core.config import settings

class ScrapeAgent:
    def get_public_data(self, url: str):
        if not url: return None
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            # Configuración de proxy opcional para escalabilidad
            context_args = {}
            if settings.PROXY_URL:
                context_args["proxy"] = {"server": settings.PROXY_URL}
                
            context = browser.new_context(**context_args)
            page = context.new_page()
            Stealth().apply_stealth_sync(page)
            
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                # Extraemos el contenido principal visible
                return page.locator("main").inner_text()
            except Exception as e:
                print(f"Error en ScrapeAgent: {e}")
                return None
            finally:
                browser.close()