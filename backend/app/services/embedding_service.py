import os
import asyncio
import hashlib
from typing import List
from app.config import settings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"


class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    def _get_model(self):
        if self._model is None:
            try:
                import torch
                torch.set_num_threads(1)
                torch.set_num_interop_threads(1)
            except Exception:
                pass

            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(settings.EMBEDDING_MODEL)
            except Exception as e:
                print(f"Warning: Falling back to lightweight hash embeddings: {e}")
                self._model = "fallback"
        return self._model

    def _fallback_embed(self, text: str) -> List[float]:
        # Fast, zero-RAM 384-dimensional deterministic feature embedding
        vec = [0.0] * 384
        for i, word in enumerate(text.lower().split()):
            h = int(hashlib.md5(word.encode()).hexdigest(), 16)
            idx = h % 384
            vec[idx] += 1.0 / (1 + i * 0.1)
        norm = sum(x * x for x in vec) ** 0.5 or 1.0
        return [x / norm for x in vec]

    async def get_embedding(self, text: str) -> List[float]:
        model = self._get_model()
        if model == "fallback":
            return self._fallback_embed(text)
        try:
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(None, model.encode, text)
            return embedding.tolist()
        except Exception:
            return self._fallback_embed(text)

    async def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        return [await self.get_embedding(t) for t in texts]