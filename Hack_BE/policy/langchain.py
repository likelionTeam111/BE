# import os
# from decouple import config
# from langchain_openai import ChatOpenAI 
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_postgres import PGVector

# #chains
# from langchain_core.tools import tool
# from langgraph.graph import MessagesState, StateGraph
# from langchain_core.messages import SystemMessage
# from langgraph.prebuilt import ToolNode
# from langgraph.graph import END
# from langgraph.prebuilt import ToolNode, tools_condition
# from langgraph.checkpoint.memory import MemorySaver

# # LangSmith
# os.environ["LANGSMITH_TRACING"] = "true"
# os.environ["LANGSMITH_API_KEY"] = config('langsmith')


# # chat bot
# api_key = config('gpt_api_key')
# llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

# embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sbert-nli",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
    )

# #vector store
# user = config('DJANGO_DB_USER')
# pwd = config('DJANGO_DB_PASSWORD')
# host = config('DJANGO_DB_HOST')
# port = config('DJANGO_DB_PORT')
# db_name = config('DJANGO_DB_NAME')

# vector_store = PGVector(
#     embeddings=embeddings,
#     collection_name="my_docs",
#     connection = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db_name}"
# )

# graph_builder = StateGraph(MessagesState)

# @tool(response_format="content_and_artifact")
# def retrieve(query: str):
#     """Retrieve information related to a query."""
#     retrieved_docs = vector_store.similarity_search(query, k=3)
#     serialized = "\n".join(
#         (f"Source: {doc.metadata}\nContent: {doc.page_content}")
#         for doc in retrieved_docs
#     )
#     return serialized, retrieved_docs

# # Step 1: Generate an AIMessage that may include a tool-call to be sent.
# def query_or_respond(state: MessagesState):
#     """Generate tool call for retrieval or respond."""
#     llm_with_tools = llm.bind_tools([retrieve])
#     response = llm_with_tools.invoke(state["messages"])
#     # MessagesState appends messages to state instead of overwriting
#     return {"messages": [response]}

# # Step 2: Execute the retrieval.
# tools = ToolNode([retrieve])

# # Step 3: Generate a response using the retrieved content.
# def generate(state: MessagesState):
#     """Generate answer."""
#     # Get generated ToolMessages
#     recent_tool_messages = []
#     for message in reversed(state["messages"]):
#         if message.type == "tool":
#             recent_tool_messages.append(message)
#         else:
#             break
#     tool_messages = recent_tool_messages[::-1]

#     # Format into prompt
#     docs_content = "\n".join(doc.content for doc in tool_messages)
#     system_message_content = (
#         "You are an assistant for question-answering tasks. "
#         "Use the following pieces of retrieved context to answer "
#         "the question. If you don't know the answer, say that you "
#         "don't know. Use three sentences maximum and keep the "
#         "answer concise."
#         f"{docs_content}"
#     )
#     conversation_messages = [
#         message
#         for message in state["messages"]
#         if message.type in ("human", "system")
#         or (message.type == "ai" and not message.tool_calls)
#     ]
#     prompt = [SystemMessage(system_message_content)] + conversation_messages

#     # Run
#     response = llm.invoke(prompt)
#     return {"messages": [response]}

# graph_builder.add_node(query_or_respond)
# graph_builder.add_node(tools)
# graph_builder.add_node(generate)

# graph_builder.set_entry_point("query_or_respond")
# graph_builder.add_conditional_edges(
#     "query_or_respond",
#     tools_condition,
#     {END: END, "tools": "tools"},
# )
# graph_builder.add_edge("tools", "generate")
# graph_builder.add_edge("generate", END)

# # MemorySaver
# memory = MemorySaver()
# graph = graph_builder.compile(checkpointer=memory)

# def _to_text(content):
#     if isinstance(content, str):
#         return content
#     if isinstance(content, list):
#         # LangChain 메시지 블록 리스트 처리
#         return "".join(
#             (p.get("text","") if isinstance(p, dict) else getattr(p, "text", ""))
#             for p in content
#         )
#     return str(content or "")

# def ai_chat(message: str, thread_id: str):
#     state = graph.invoke(
#         {"messages": [{"role": "user", "content": message}]},
#         config={"configurable": {"thread_id": thread_id}},
#     )
#     last_ai = next((m for m in reversed(state["messages"]) if m.type == "ai"), None)
#     return _to_text(getattr(last_ai, "content", "")) if last_ai else ""