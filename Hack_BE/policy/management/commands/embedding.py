from django.core.management.base import BaseCommand
import os
from decouple import config

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

from langchain_text_splitters import RecursiveCharacterTextSplitter
from .policy_loader import PolicyLoader
from policy.models import Policy

class Command(BaseCommand):
    def handle(self, *args, **options):
        # LangSmith
        os.environ["LANGSMITH_TRACING"] = "true"
        os.environ["LANGSMITH_API_KEY"] = config('langsmith')

        # embedding model
        embeddings = HuggingFaceEmbeddings(
            model_name="hgan/ko-sbert-nli",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
            )
        
        #vector store
        user = config('DJANGO_DB_USER')
        pwd = config('DJANGO_DB_PASSWORD')
        host = config('DJANGO_DB_HOST')
        port = config('DJANGO_DB_PORT')
        db_name = config('DJANGO_DB_NAME')

        vector_store = PGVector(
            embeddings=embeddings,
            collection_name="my_docs",
            connection = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db_name}"
        )

        qs = Policy.objects.all()
        docs = PolicyLoader(qs).load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        all_splits = text_splitter.split_documents(docs)

        try:
            vector_store.delete_collection()  # 없으면 ValueError 가능
        except ValueError:
            pass
        vector_store.create_collection() 
        vector_store.add_documents(all_splits)