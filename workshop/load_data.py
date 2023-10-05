from PyPDF2 import PdfReader
import os
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import pickle

def process_text(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-mpnet-base-v2",
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': False}
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


if __name__ == "__main__":
    main()