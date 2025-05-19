from src.services.repositories.base_repository import BaseDynamoRepository
from src.services.embedding import Embedding


class ContextRepository:
    def __init__(self, base_repo: BaseDynamoRepository, table_name="docbot-contexts"):
        self.base_repo = base_repo
        self.table_name = table_name

    def get_all_contexts(self):
        return self.base_repo.get_all_items(self.table_name)

    def get_context_by_id(self, id: any):
        return self.base_repo.get_item_by_id(self.table_name, id)
    
    def save_context(self, context: str, description: str, context_id: str):

        item = {
            "context": context,
            "description": description, 
            "context_id": context_id
        }

        self.base_repo.put_item(self.table_name, item)
