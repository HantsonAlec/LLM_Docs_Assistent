import os
from typing import List, Dict, Any

from dotenv import load_dotenv
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_pinecone import PineconeVectorStore

load_dotenv()
EMBEDDING_MODEL = OllamaEmbeddings(model="llama3")
RETRIEVER = PineconeVectorStore(
    embedding=EMBEDDING_MODEL, index_name=os.getenv("INDEX_NAME")
)
LLM_MODEL = ChatOllama(model="llama3")
RETRIEVAL_QA_PROMPT = hub.pull("langchain-ai/retrieval-qa-chat")
REPHRASE_PROMPT = hub.pull("langchain-ai/chat-langchain-rephrase")
STUFF_DOCUMENT_CHAIN = create_stuff_documents_chain(LLM_MODEL, RETRIEVAL_QA_PROMPT)
HISTORY_RETRIEVER = create_history_aware_retriever(llm=LLM_MODEL, retriever=RETRIEVER.as_retriever(), prompt=REPHRASE_PROMPT)
QA_CHAIN = create_retrieval_chain(
    retriever=HISTORY_RETRIEVER, combine_docs_chain=STUFF_DOCUMENT_CHAIN
)


def run_llm(query: str, chat_history: List[Dict[str, Any]]):
    llm_result = QA_CHAIN.invoke(input={"input": query, "chat_history": chat_history})
    result = {
        "query": query,
        "result": llm_result["answer"],
        "source_documents": llm_result["context"],
    }
    return result


if __name__ == "__main__":
    res = run_llm(query="What is a langchain chain?")
    print(res["answer"])
