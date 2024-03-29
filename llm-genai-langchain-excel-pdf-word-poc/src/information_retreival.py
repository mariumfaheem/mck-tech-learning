import os
from langchain.chat_models import ChatOpenAI
import streamlit as st
from information_extraction import extract_information_from_pdf,extract_information_from_word,extract_information_from_excel
from information_storage import chunks_vector_storage
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain


## os.environ["OPENAI_API_KEY"] =  "Enter your key"

llm = ChatOpenAI(temperature=0,model_name="gpt-4")
embeddings = OpenAIEmbeddings()

st.header("Please upload your files to query them")

with st.sidebar:
    uploaded_files = st.file_uploader("Please upload your files", accept_multiple_files=True, type=None)

    st.info("Please refresh the browser if you decide to upload more files to reset the session")

documents = []

if uploaded_files:

    st.write(f"Number of files uploaded: {len(uploaded_files)}")

    if "processed_data" not in st.session_state:

        if uploaded_files:
            for uploaded_file in uploaded_files:

                file_path = os.path.join(os.getcwd(), uploaded_file.name)
                print(file_path)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                if file_path.endswith((".pdf")):
                    print("processing pdf\n")
                    document_chunks = extract_information_from_pdf(file_path)

                if file_path.endswith((".docx", ".txt")):
                    print("processing docx\n")
                    document_chunks = extract_information_from_word(file_path)

                if file_path.endswith((".xlsx")):
                    print("processing xlsx\n")
                    document_chunks = extract_information_from_excel(file_path)
            documents.extend(document_chunks)

        vectorstore = chunks_vector_storage(documents,embeddings)

        # Store the processed data in session state for reuse
        st.session_state.processed_data = {
            "document_chunks": document_chunks,
            "vectorstore": vectorstore,
        }

    else:
        # If the processed data is already available, retrieve it from session state
        document_chunks = st.session_state.processed_data["document_chunks"]
        vectorstore = st.session_state.processed_data["vectorstore"]

    # Initialize Langchain's QA Chain with the vectorstore
    qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Message KMS..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query the assistant using the latest chat history
        result = qa({"question": prompt, "chat_history": [(message["role"], message["content"]) for message in st.session_state.messages]})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response = result["answer"]
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
        print(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    st.write("Please upload your files.")
