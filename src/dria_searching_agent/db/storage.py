from qdrant_client import QdrantClient


class Storage:
    def __init__(self):
        self.client = QdrantClient(":memory:")

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
            metadata.append({"source": "arxiv"})
            ids.append(chunk["id"])
        self.add(collection_name, docs, metadata, ids)

    def query(self, query_text, collection_name="pdf"):
        return self.client.query(
            collection_name=collection_name,
            query_text=query_text,
            limit=5
       )

