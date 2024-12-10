import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore

DOCS_PATH = (
    Path(__file__).parent.parent
    / "langchain-docs"
    / "api.python.langchain.com"
    / "en"
    / "latest"
)
BASE_PATH_STR = str(DOCS_PATH.parent.parent.parent)
LOADER = ReadTheDocsLoader(DOCS_PATH)
EMBEDDING_MODEL = OllamaEmbeddings(model="llama3.2:1b")
TEXT_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)


def ingest_docs():
    raw_documents = LOADER.load()
    documents = TEXT_SPLITTER.split_documents(raw_documents)
    documents = [doc for doc in documents if doc.page_content.strip()]
    for doc in documents:
        source_url = doc.metadata["source"]
        new_url = source_url.replace(BASE_PATH_STR, "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Adding {len(documents)} into Pinecone")
    PineconeVectorStore.from_documents(
        documents=documents,
        embedding=EMBEDDING_MODEL,
        index_name=os.getenv("INDEX_NAME"),
    )


if __name__ == "__main__":
    ingest_docs()
