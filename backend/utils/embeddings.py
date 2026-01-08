try:
    # Prefer the higher-level sentence-transformers package which is lighter
    # to import for this use-case. Avoid importing the full `transformers`
    # library at module import time to reduce startup overhead.
    from sentence_transformers import SentenceTransformer
    import numpy as np

    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    _s_model = SentenceTransformer(MODEL_NAME)

    def embed_text(text: str) -> list[float]:
        if not text or not text.strip():
            return [0.0] * _s_model.get_sentence_embedding_dimension()
        emb = _s_model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return emb.tolist()
except Exception as e:
    # If sentence-transformers (or its deps) are unavailable, use a safe
    # deterministic fallback so the app can still start in minimal environments.
    print("sentence-transformers not available, using fallback embedder:", e)

    DEFAULT_DIM = 384

    def embed_text(text: str) -> list[float]:
        return [0.0] * DEFAULT_DIM
