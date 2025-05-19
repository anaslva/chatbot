from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/documents",  
    tags=["Documentos"]  
)

class DocumentUploadRequest(BaseModel):
    filename: str = Field(..., example="token_mtls.md", description="Nome do arquivo Markdown salvo na pasta 'docs'")
    topic: str = Field(..., example="token", description="Título ou identificador do conteúdo para busca futura")


@router.post("/upload", summary="Upload de novo documento de referência")
def upload_document(
    request: Request,
    file: UploadFile = File(..., description="Arquivo de documentação (.md)"),
    topic: str = Form(..., description="Título ou tópico associado ao documento")
):
    try:
        content = file.file.read().decode("utf-8")
        loader = request.app.state.doc_repo 
        loader.save_document(topic=topic, content=content)

        return {"message": f"Documento '{topic}' inserido com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
