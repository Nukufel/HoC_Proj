from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

def create_vector_store():
    loader = PyPDFLoader("resources/schedule.pdf")
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=25)
    chunks = splitter.split_documents(pages)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = Chroma.from_documents(chunks, embeddings=embeddings)
    return vector_store