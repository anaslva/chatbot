import boto3

class BaseDynamoRepository:
    def __init__(self, region="us-east-1", endpoint_url=None):
        self.dynamodb = boto3.resource("dynamodb", region_name=region, endpoint_url=endpoint_url)

    def get_table(self, table_name: str):
        return self.dynamodb.Table(table_name)

    def get_all_items(self, table_name: str):
        table = self.get_table(table_name)
        response = table.scan()
        return response.get("Items", [])

    def put_item(self, table_name: str, item: dict):
        table = self.get_table(table_name)
        table.put_item(Item=item)
        
    def get_item_by_id(self, table_name: str, id_key: str, id_value: any):
        table = self.get_table(table_name)
        response = table.get_item(Key={id_key: id_value})
        return response.get("Item") 
        
