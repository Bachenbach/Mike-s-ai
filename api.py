# app/routes/api.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel

router = APIRouter()

class Query(BaseModel):
    text: str
    context: Optional[dict] = None
    options: Optional[dict] = None

@router.post("/process")
async def process_query(query: Query):
    """Process a text query and return comprehensive response"""
    try:
        # NLP Analysis
        nlp_analysis = await language_processor.process_text(query.text)
        
        # Get AI response
        ai_response = await api_orchestrator.process_query(query.text)
        
        # Update context
        context = await context_manager.update_context(
            query.text,
            ai_response,
            nlp_analysis
        )
        
        return {
            "status": "success",
            "response": ai_response,
            "analysis": nlp_analysis,
            "context": context
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/context/{session_id}")
async def get_context(session_id: str):
    """Get current context for a session"""
    try:
        return context_manager.get_current_context()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/analyze")
async def analyze_text(query: Query):
    """Perform detailed text analysis"""
    try:
        analysis = await language_processor.process_text(
            query.text,
            tasks=['syntax', 'semantics', 'sentiment', 'entities']
        )
        return {"status": "success", "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
