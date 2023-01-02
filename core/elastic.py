import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decouple import config
from elasticsearch import Elasticsearch

from core.gpt import generate_names


class Elastic:
    def __init__(self):
        self.client = Elasticsearch(cloud_id=config("CLOUD_ID"), basic_auth=("elastic", config("ELASTIC_PASSWORD")))
        self.index = "search-gpt-names"
    
    def regenerate_documents(self):
        self.client.delete_by_query(index=self.index, query={"match_all": {}})

        actions = []
        for i, name in enumerate(generate_names()):
            action = {"index": {"_index": self.index, "_id": i}}
            doc = {**name, "role": "customer" if i%2 else "employee"}
            actions.append(action)
            actions.append(doc)

        self.client.bulk(index=self.index, operations=actions)
        self.client.indices.refresh(index=self.index)
    
    def search(self, query):
        response = self.client.search(index=self.index, query={"query_string": { "query": f"*{query}*" }})
        return [name["_source"] for name in response["hits"]["hits"]]
