from fastapi import APIRouter, Depends
from app.schemas.lead import ProspectRequest, LeadEvaluation
from app.services.orchestrator import MeridianOrchestrator
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/enrich", response_model=LeadEvaluation)
async def enrich_lead(request: ProspectRequest, user=Depends(get_current_user)):
    # La ruta solo valida la entrada y llama al servicio
    service = MeridianOrchestrator(user)
    return await service.process_prospect(request)