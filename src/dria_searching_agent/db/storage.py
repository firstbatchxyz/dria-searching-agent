from qdrant_client import QdrantClient
import random
class Storage:
    def __init__(self):
        self.client = QdrantClient(url="http://localhost:6333")
        if self.client.get_collection("pdf") is None:
            self.client.recreate_collection("pdf", vectors_config=self.client.get_fastembed_vector_params())

    def add(self, collection_name, documents, metadata, ids):
        self.client.add(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata,
            ids=ids
        )

    def add_chunks(self, chunks, collection_name="pdf"):

        docs = []
        metadata = []
        ids = []
        for chunk in chunks:
            docs.append(chunk["text"])
            metadata.append({"source": "pdf"})
            ids.append(chunk["id"])
        self.add(collection_name, docs, metadata, ids)

    def add_text_chunks(self, chunks, url, collection_name="pdf"):

        docs = []
        metadata = []
        ids = []
        for chunk in chunks:
            docs.append(chunk)
            metadata.append({"source": url})
            ids.append(random.randint(0, 100000))
        self.add(collection_name, docs, metadata, ids)

    def query(self, query_text, collection_name="pdf"):
        results = self.client.query(
            collection_name=collection_name,
            query_text=query_text,
            limit=10
       )
        return "\n".join([result.document for result in results])


def main():
    storage = Storage()
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
    storage.add_chunks(chunks)

    storage2 = Storage()
    print(storage2.query("quantum computing"))

