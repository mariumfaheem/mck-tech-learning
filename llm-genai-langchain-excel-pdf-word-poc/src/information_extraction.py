from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader


def extract_information_from_pdf(file_path):
    loader = UnstructuredFileLoader(file_path, mode="single")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
    document_chunks = text_splitter.split_documents(documents)
    return document_chunks


def extract_information_from_excel(file_path):
    loader = UnstructuredExcelLoader(file_path, mode="single")
    loaded_documents = loader.load()
    return loaded_documents


def extract_information_from_word(file_path):
    loader = UnstructuredWordDocumentLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=150)
    document_chunks = text_splitter.split_documents(documents)
    return document_chunks
