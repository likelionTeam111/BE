# rag/store.py
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

PG_CONN_STR = os.getenv("PG_CONN_STR")
COLLECTION = os.getenv("PGVECTOR_COLLECTION", "policy_v1")

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
    model_kwargs={"device": "cuda"},              # GPU 없으면 지우기/ "cpu"
    encode_kwargs={"normalize_embeddings": True}, # cosine 유사도 안정화
)

vectorstore = PGVector(
    connection=PG_CONN_STR,
    collection_name=COLLECTION,
    embedding_function=embeddings,
    use_jsonb=True,
)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
