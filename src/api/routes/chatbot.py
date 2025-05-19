from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/chatbot",  
    tags=["Chatbot"]  
)

class AskRequest(BaseModel):
    question: str = Field(..., example="Como autenticar via mTLS?", description="Pergunta a ser respondida pela IA")
    

@router.post("/ask", summary="Faça uma pergunta")
def ask_question(request: Request, body: AskRequest):
    try:
        ask = request.app.state.ask
        resposta = ask.ask_question_to_model(body.question)
        return resposta
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))