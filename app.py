import pickle
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# --------------------------------
# PAGE CONFIG
# --------------------------------
load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
st.set_page_config(
    page_title="Interview Transcript Insight Engine",
    layout="wide"
)

st.title("Interview Transcript Insight Engine")

# --------------------------------
# LOAD EMBEDDINGS
# --------------------------------

@st.cache_resource
def load_resources():

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)

    bm25 = BM25Retriever.from_documents(
        chunks
    )

    bm25.k = 5

    faiss_retriever = db.as_retriever(
        search_kwargs={"k": 5}
    )

    hybrid = EnsembleRetriever(
        retrievers=[
            bm25,
            faiss_retriever
        ],
        weights=[0.5, 0.5]
    )

    return hybrid, chunks

hybrid_retriever, chunks = load_resources()

# --------------------------------
# CORPUS STATS
# --------------------------------

with st.sidebar:

    st.header("Corpus Statistics")

    total_chunks = len(chunks)

    total_words = sum(
        len(chunk.page_content.split())
        for chunk in chunks
    )

    st.metric(
        "Chunks",
        f"{total_chunks:,}"
    )

    st.metric(
        "Words",
        f"{total_words:,}"
    )

# --------------------------------
# GROQ
# --------------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

# --------------------------------
# PROMPT
# --------------------------------

prompt_template = """
You are an expert qualitative research analyst.

Answer ONLY using the provided transcript evidence.

Rules:

1. Identify themes.
2. Cite supporting evidence.
3. Be concise.
4. Do not hallucinate.

Context:

{context}

Question:

{question}

Answer:
"""

question = st.text_input(
    "Ask a question about your transcripts"
)

# --------------------------------
# QUERY
# --------------------------------

if st.button("Analyze") and question:

    docs = hybrid_retriever.invoke(
        question
    )

    citations = []

    context_parts = []

    unique = set()

    for i, doc in enumerate(docs, start=1):

        source = doc.metadata.get(
            "source_file",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        key = (source, page)

        if key in unique:
            continue

        unique.add(key)

        citations.append(
            f"[{len(citations)+1}] {source} Page {page}"
        )

        context_parts.append(
            f"""
SOURCE [{len(citations)}]
FILE: {source}
PAGE: {page}

TEXT:
{doc.page_content}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    final_prompt = prompt_template.format(
        context=context,
        question=question
    )

    st.subheader("Answer")

    placeholder = st.empty()

    response_text = ""

    for chunk in llm.stream(
        final_prompt
    ):

        if chunk.content:

            response_text += chunk.content

            placeholder.markdown(
                response_text
            )

    st.divider()

    st.subheader("Citations")

    for citation in citations:

        st.write(citation)

    st.divider()

    st.subheader(
        "Supporting Evidence"
    )

    for i, doc in enumerate(
        docs,
        start=1
    ):

        source = doc.metadata.get(
            "source_file",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )

        with st.expander(
            f"[{i}] {source} Page {page}"
        ):

            st.write(
                doc.page_content
            )