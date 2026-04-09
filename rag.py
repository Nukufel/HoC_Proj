import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from openai.types import VectorStore


def create_vector_store():
    pages = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=25)
    chunks = splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(chunks, embeddings=embeddings, persist_directory="./schedule_db")
    return vector_store

def load_documents():
    pages: List[Document] = []

    for file in get_files():
        loader = PyPDFLoader(file_path=file)
        pages.extend(loader.load())

    return pages

def get_files():
    return os.listdir("resources/")

def search_schedule(vector_store: VectorStore, question: str):
    docs = vector_store.similarity_search(question)
    return "\n".join([d.page_content for d in docs])