import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

DB_PATH = "./rag_db"
RESOURCES_DIR = "resources/"

class RAG:
    def __init__(self):
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self._store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
        self._index_new_files()

    def _index_new_files(self):
        indexed = set(
            m["source"]
            for m in self._store.get(include=["metadatas"])["metadatas"]
            if m and "source" in m
        )

        pages: List[Document] = []
        for file in os.listdir(RESOURCES_DIR):
            path = f"{RESOURCES_DIR}{file}"
            if path not in indexed:
                pages.extend(PyPDFLoader(file_path=path).load())

        if pages:
            self._store.add_documents(self._splitter.split_documents(pages))

    def add_pdf(self, file_path: str):
        pages = PyPDFLoader(file_path=file_path).load()
        self._store.add_documents(self._splitter.split_documents(pages))

    def search(self, question: str) -> str:
        docs = self._store.similarity_search(question)
        return "\n".join([d.page_content for d in docs])

