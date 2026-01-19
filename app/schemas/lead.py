from pydantic import BaseModel, Field, SecretStr

class ProspectRequest(BaseModel):
    target: str
    is_company: bool = False
    icp_criteria: str
    user_llm_key: SecretStr # La key del usuario para la IA

class LeadEvaluation(BaseModel):
    name: str | None
    icp_score: int = Field(..., ge=0, le=100) # El score para el Sheet
    status_label: str # 🔥 Prioritario, etc.
    reason: str
    is_qualified: bool