import os
import pickle

import streamlit as st
from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.extensions.langchain import LangChainInterface
from genai.schemas import GenerateParams
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader

load_dotenv()

creds = Credentials(
    api_key=os.environ["BAM_API_KEY"], api_endpoint="https://bam-api.res.ibm.com/v1"
)
params = GenerateParams(
    decoding_method="greedy", min_new_tokens=30, max_new_tokens=1024, temperature=0.5
)
model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}


def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )
    knowledge_base = FAISS.from_texts(chunks, embeddings)

    return knowledge_base


def main():
    if not os.path.isfile("knowledge_base.pkl"):
        pdf = "data/Ian Goodfellow, Yoshua Bengio, Aaron Courville - Deep Learning (2017, MIT).pdf"
        if pdf is not None:
            pdf_reader = PdfReader(pdf)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Create the knowledge base object
            knowledge_base = process_text(text)
            with open("knowledge_base.pkl", "wb") as file:
                pickle.dump(knowledge_base, file)
    else:
        with open("knowledge_base.pkl", "rb") as file:
            knowledge_base = pickle.load(file)

        st.title("Ask your Datascience wizard 🧙")
        query = st.text_input("Ask a question to the PDF")
        cancel_button = st.button("Cancel")

        if cancel_button:
            st.stop()

        if query:
            with st.spinner("Waiting for the answer... 🔎"):
                docs = knowledge_base.similarity_search(query)
                langchain_model = LangChainInterface(
                    model="google/flan-t5-xxl",
                    params=params,
                    credentials=creds,
                )
                chain = load_qa_chain(langchain_model, chain_type="stuff")
                response = chain.run(input_documents=docs, question=query)

            st.subheader("Answer:")
            st.write(response)


if __name__ == "__main__":
    main()
