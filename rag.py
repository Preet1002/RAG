from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
import requests
from langchain_community.vectorstores import FAISS
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-embedding-2"

class GeminiEmbeddings(Embeddings):
    def _embed(self, texts):
        url = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:batchEmbedContents?key={GOOGLE_API_KEY}"
        requests_body = {
            "requests": [
                {"model": f"models/{MODEL}", "content": {"parts": [{"text": t}]}}
                for t in texts
            ]
        }
        response = requests.post(url, json=requests_body)
        response.raise_for_status()
        return [e["values"] for e in response.json()["embeddings"]]

    def embed_documents(self, texts):
        return self._embed(texts)

    def embed_query(self, text):
        return self._embed([text])[0]

embeddings = GeminiEmbeddings()
def load_pdf(pdf_path):
    loader= PyPDFLoader(pdf_path)
    documents=loader.load()
    return documents

def extract_text(pdf_path):
    docs=load_pdf(pdf_path)
    text=""
    for doc in docs:
        text+=doc.page_content+"\n"
    return text

def split_documents(docs):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    chunks=text_splitter.split_documents(docs)
    return chunks

def create_vector_store(chunks):
    vector_store=FAISS.from_documents(chunks,embeddings)
    vector_store.save_local("vectorstore")
    return vector_store

def load_vector_store():
    vector_store=FAISS.load_local("vectorstore",embeddings,allow_dangerous_deserialization=True)
    return vector_store