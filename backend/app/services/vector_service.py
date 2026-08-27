import os
import chromadb
from typing import List, Dict, Any, Optional

from app.config import settings

os.environ["ANONYMIZED_TELEMETRY"] = "False"


class VectorService:
    _instance = None
    _client = None
    _collection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorService, cls).__new__(cls)
            cls._client = chromadb.PersistentClient(path="./chroma_db")
            cls._collection = cls._client.get_or_create_collection(
                name=settings.CHROMA_COLLECTION
            )
        return cls._instance

    @property
    def client(self):
        return self._client

    @property
    def collection(self):
        return self._collection

    async def add_memory(
        self,
        vector_id: str,
        embedding: List[float],
        content: str,
        user_id: int,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        meta = {"user_id": str(user_id)}

        if metadata:
            meta.update(metadata)

        self.collection.add(
            ids=[vector_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[meta],
        )

        return vector_id

    async def update_memory(
        self,
        vector_id: str,
        embedding: List[float],
        content: str,
        user_id: int,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        meta = {"user_id": str(user_id)}

        if metadata:
            meta.update(metadata)

        self.collection.update(
            ids=[vector_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[meta],
        )

    async def delete_memory(self, vector_id: str):
        self.collection.delete(ids=[vector_id])

    async def search(
        self,
        query_embedding: List[float],
        user_id: int,
        limit: int = 5,
        score_threshold: float = 0.0,
        include_metadata: bool = False,
    ):
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where={"user_id": str(user_id)},
            include=["documents", "metadatas", "distances"],
        )

        memories = []

        if results["ids"] and results["ids"][0]:
            for i, vector_id in enumerate(results["ids"][0]):

                score = 1 / (1 + results["distances"][0][i])

                if score >= score_threshold:

                    item = {
                        "id": vector_id,
                        "document": results["documents"][0][i],
                        "score": score,
                    }

                    if include_metadata:
                        item["metadata"] = results["metadatas"][0][i]

                    memories.append(item)

        return memories