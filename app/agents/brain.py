from google import genai
from app.schemas.lead import LeadEvaluation

class BrainAgent:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def evaluate(self, raw_text: str, icp: str, context: str) -> LeadEvaluation:
        # Prompt que genera el ICP Score y el análisis
        prompt = f"Analiza este perfil según el ICP: {icp}. Contexto previo: {context}. Datos: {raw_text}"
        
        # Generación de contenido estructurado
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        return LeadEvaluation.model_validate_json(response.text)