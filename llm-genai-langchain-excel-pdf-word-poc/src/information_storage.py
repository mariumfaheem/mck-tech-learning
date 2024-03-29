
from langchain_community.vectorstores import FAISS



def chunks_vector_storage(document_chunks, embeddings):
    vectorstore = FAISS.from_documents(document_chunks, embeddings)
    return vectorstore


