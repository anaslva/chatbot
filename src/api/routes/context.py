from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel, Field
router = APIRouter(
    prefix="/context",  
    tags=["Contexto"]  
)

class AddContextRequest(BaseModel):
    context: str = Field(..., description="Nome do contexto a ser adicionado")
    id: str = Field(..., example="pix", description="Identificador do contexto")
    description: str = Field(..., examples="Tudo sobre Pix, QR Code, callbacks", description="Descrição do contexto")

@router.post(path="/add", summary="Cadastro de novo contexto")
def add_context(
    request: Request,
    body: AddContextRequest
):
    try:
        
        loader = request.app.state.context_repo
        loader.save_document(description=body.description, context=body.context, context_id=body.id)

        return {"message": f"Contexto '{body.context}' inserido com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", summary="Listar todos os contextos")
def list_contexts(
    request: Request
):
    try:
        
        loader = request.app.state.context_repo
        contexts = loader.get_all_contexts()

        return contexts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{id}", summary="Consultar contexto por id")
def get_context_by_id(
    request: Request,
    id: str,
):
    try:
        
        loader = request.app.state.context_repo
        contexts = loader.get_context_by_id(id)

        return contexts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))