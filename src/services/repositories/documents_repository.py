import uuid
from src.services.embedding import Embedding
from src.services.repositories.base_repository import BaseDynamoRepository

class DocumentRepository:
    def __init__(self, embedding: Embedding, base_repo: BaseDynamoRepository, table_name="docbot-texts"):
        self.embedding = embedding
        self.base_repo = base_repo
        self.table_name = table_name

    def get_all_documents(self):
        return self.base_repo.get_all_items(self.table_name)

    def save_document(self, topic: str, content: any):
        embedding_str = self.embedding.encode_content(content)

        item = {
            "topic": topic,
            "content": content,
            "embedding": embedding_str,
            "document_id": str(uuid.uuid4())
        }

        self.base_repo.put_item(self.table_name, item)
