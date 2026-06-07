import os
import pickle

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

TRANSCRIPT_FOLDER = "transcripts"

documents = []

print("Loading PDFs...")

for file in os.listdir(TRANSCRIPT_FOLDER):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(
            TRANSCRIPT_FOLDER,
            file
        )

        loader = PyPDFLoader(pdf_path)

        pages = loader.load()

        for page in pages:

            page.metadata["source_file"] = file

        documents.extend(pages)

print(f"Pages loaded: {len(documents)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Chunks: {len(chunks)}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(
    chunks,
    embeddings
)

db.save_local("faiss_index")

with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("Index saved.")