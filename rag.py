from langchain_community.document_loaders import PyPDFLoader

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