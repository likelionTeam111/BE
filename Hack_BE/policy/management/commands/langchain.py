from django.core.management.base import BaseCommand

import os
from decouple import config
from langchain.chat_models import init_chat_model
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

from langchain import hub
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph

# LangSmith
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = config('langsmith')


# chat bot
api_key = config('gpt_api_key')
llm = init_chat_model("gpt-4o-mini", api_key = api_key)

# embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-m3",
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

prompt = hub.pull("rlm/rag-prompt", api_url="https://api.smith.langchain.com")

example_messages = prompt.invoke(
    {"context": "(context goes here)", "question": "(question goes here)"}
).to_messages()

# LangGraph
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    # 기본값: k=4
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

class Command(BaseCommand):
    def handle(self, *args, **options):
        result = graph.invoke({"question": "월세관련된 정책이 뭐가 있을까"})

        print(f"Context: {result['context']}\n\n")
        print(f"Answer: {result['answer']}")