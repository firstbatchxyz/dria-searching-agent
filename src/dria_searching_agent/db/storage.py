from qdrant_client import QdrantClient
import random
from src.dria_searching_agent.config import config

class Storage:
    def __init__(self, col_name="scrape"):
        self.client = QdrantClient(url=config.QDRANT_URL())
        self.col_name = col_name

    def delete_collection(self):
        self.client.delete_collection(self.col_name)

    def add(self, collection_name, documents, metadata, ids):
        self.client.add(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata,
            ids=ids
        )

    def add_chunks(self, chunks):

        docs = []
        metadata = []
        ids = []
        for chunk in chunks:
            docs.append(chunk["text"])
            metadata.append({"source": "scrape"})
            ids.append(chunk["id"])
        self.add(self.col_name, docs, metadata, ids)

    def add_text_chunks(self, chunks, url):

        docs = []
        metadata = []
        ids = []
        for chunk in chunks:
            docs.append(chunk)
            metadata.append({"source": url})
            ids.append(random.randint(0, 100000))
        self.add(self.col_name, docs, metadata, ids)

    def query(self, query_text):
        results = self.client.query(
            collection_name=self.col_name,
            query_text=query_text,
            limit=20
       )

        for res in results:
            print(res)
            print("\n")
        return "\n".join([result.document for result in results if result.score > 0.79])


def main():
    storage = Storage()
    #storage.delete_collection()
    chunks = [
        {
            "id": 1,
            "text": "Quantum computing is a field that applies the principles of quantum mechanics to computing devices."
        },
        {
            "id": 2,
            "text": "Quantum computing is the use of quantum-mechanical phenomena such as superposition and entanglement to perform computation."
        },
        {
            "id": 3,
            "text": "Quantum computing is the study of quantum-mechanical phenomena to perform computation such as superposition and entanglement."
        }
    ]
    #storage.add_chunks(chunks)

    #storage2 = Storage()
    d = storage.query("Apple Inc. risk factors")
    #print(d)

