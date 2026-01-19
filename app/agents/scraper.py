# app/agents/scraper.py
from playwright.async_api import async_playwright # Cambiado a async
from playwright_stealth import stealth_async      # Versión async de stealth
from app.core.config import settings

class ScrapeAgent:
    async def get_public_data(self, url: str) -> str | None: # Ahora es async
        """
        Extrae texto de una URL pública usando Playwright Async con modo stealth.
        """
        if not url:
            return None
        
        async with async_playwright() as p:
            # Lanzamos el navegador
            browser = await p.chromium.launch(headless=True)
            
            context_args = {}
            if settings.PROXY_URL:
                context_args["proxy"] = {"server": settings.PROXY_URL}
                
            context = await browser.new_context(**context_args)
            page = await context.new_page()
            
            # APLICAMOS STEALTH ASYNC
            await stealth_async(page)
            
            try:
                # Navegación asíncrona
                await page.goto(url, wait_until="networkidle", timeout=30000)
                
                # Buscamos contenido en 'main', si no existe, traemos el 'body'
                if await page.locator("main").count() > 0:
                    return await page.locator("main").inner_text()
                
                return await page.inner_text("body")
            
            except Exception as e:
                print(f"⚠️ Error en ScrapeAgent: {e}")
                return None
            finally:
                await browser.close()