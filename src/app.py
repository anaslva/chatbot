from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.services.repositories import context_repository, base_repository, documents_repository
from src.api.routes import chatbot, documents, context

from src.services.embedding import Embedding
from src.services.bedrock import BedrockClient
from src.services.ask_question import AskQuestion

# Inicialização da aplicação
app = FastAPI(
    title="DocBot API",
    description="API para gerenciar documentos técnicos com embeddings no DynamoDB e integração com LLM",
    version="1.0.0"
)

# Middleware de CORS (pode restringir em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Altere para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas da API
app.include_router(documents.router)
app.include_router(chatbot.router)
app.include_router(context.router)


# Inicialização das dependências na startup
@app.on_event("startup")
def startup_event():
    embedding = Embedding()
    base_repo = base_repository.BaseDynamoRepository(endpoint_url="http://localhost:8000") 
    doc_repo = documents_repository.DocumentRepository(embedding=embedding, base_repo=base_repo)
    context_repo = context_repository.ContextRepository(base_repo=base_repo)

    bedrock = BedrockClient()
    ask = AskQuestion(dynamo=doc_repo, embedding=embedding, bedrock=bedrock)

    # Injeta no app.state
    app.state.embedding = embedding
    app.state.base_repo = base_repo
    app.state.doc_repo = doc_repo
    app.state.context_repo = context_repo
    app.state.bedrock = bedrock
    app.state.ask = ask