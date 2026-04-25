import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from openai.types import VectorStore

def get_files():
    return os.listdir("resources/")

def load_documents():
    pages: List[Document] = []

    for file in get_files():
        loader = PyPDFLoader(file_path=f"resources/{file}")
        pages.extend(loader.load())

    return pages

def create_or_get_vector_store():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    if os.path.exists("./schedule_db"):
        return Chroma(
            persist_directory="./schedule_db",
            embedding_function=embeddings,
        )

    pages = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=25)
    chunks = splitter.split_documents(pages)

    vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory="./schedule_db")
    return vector_store

def search_schedule(vector_store: VectorStore, question: str):
    docs = vector_store.similarity_search(question)
    return "\n".join([d.page_content for d in docs])