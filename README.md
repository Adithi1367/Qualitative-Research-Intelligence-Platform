# Interview Transcript Insight Engine

## Overview

Interview Transcript Insight Engine is an AI-powered qualitative research analytics platform designed to analyze large collections of Focus Group Discussions (FGDs), In-Depth Interviews (IDIs), and other qualitative research transcripts.

The system enables researchers to ask natural language questions and receive evidence-backed answers generated directly from interview transcripts. It combines Hybrid Retrieval (BM25 + FAISS), semantic search, Retrieval-Augmented Generation (RAG), and Large Language Models to support qualitative data analysis at scale.

The application is built using Streamlit, LangChain, FAISS, Sentence Transformers, and Groq LLMs.

---

## Features

### Semantic Search

Retrieves conceptually relevant transcript segments using vector embeddings.

### Keyword Search

Uses BM25 retrieval to identify exact keyword matches.

### Hybrid Retrieval

Combines BM25 and FAISS retrieval to improve search relevance and coverage.

### Evidence-Based Question Answering

Generates answers using only retrieved transcript evidence.

### Source Citations

Provides transcript-level citations for transparency and explainability.

Example:

```text
High treatment costs and social stigma were identified as major barriers [1][2].

[1] FGD_07.pdf Page 4
[2] IDI_11.pdf Page 2
```

### Supporting Quotes

Displays the original transcript excerpts used to generate answers.

### Streamlit Dashboard

Interactive web application for transcript exploration and qualitative analysis.

### Streaming Responses

Answers are streamed in real time using Groq LLMs for a responsive user experience.

---

## Architecture

```text
PDF Transcripts
       │
       ▼
PyPDFLoader
       │
       ▼
Text Chunking
       │
       ▼
Sentence Embeddings
       │
       ▼
FAISS Vector Database
       │
       ├────────► BM25 Retrieval
       │
       ▼
Hybrid Retrieval
(BM25 + FAISS)
       │
       ▼
Groq LLM
(Llama 3.3 70B)
       │
       ▼
Answer Generation
       │
       ▼
Citations + Evidence Quotes
       │
       ▼
Streamlit Dashboard
```

---

## Tech Stack

### Frontend

* Streamlit

### NLP & Retrieval

* LangChain
* FAISS
* BM25 Retriever
* Sentence Transformers

### LLM

* Groq
* Llama 3.3 70B Versatile

### Document Processing

* PyPDFLoader
* pypdf

---

## Transcript Dataset

**Transcript files are NOT included in this repository.**

Users must provide their own PDF interview transcripts and place them inside the `transcripts/` directory before building the vector index.

Expected structure:

```text
transcripts/

├── FGD_01.pdf
├── FGD_02.pdf
├── FGD_03.pdf
├── ...
├── IDI_01.pdf
├── IDI_02.pdf
```

Supported document types:

* Focus Group Discussions (FGDs)
* In-Depth Interviews (IDIs)
* Qualitative research interviews
* Research transcripts stored as PDF files

After adding transcripts, generate the vector index by running:

```bash
python build_index.py
```

**Note:** This repository does not provide transcript datasets. Users are responsible for obtaining, creating, or generating their own interview transcripts while ensuring compliance with applicable privacy, ethical, and data-use requirements.

---

## Project Structure

```text
Transcript-Intelligence/

│
├── transcripts/          # User-provided PDF transcripts (not included)
│
├── build_index.py        # Creates FAISS index from transcripts
├── app.py                # Streamlit application
├── chunks.pkl            # Stored chunk metadata
│
├── faiss_index/
│     index.faiss
│     index.pkl
│
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>

cd Transcript-Intelligence
```

### Create Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root directory.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Building the Vector Index

Place all transcript PDFs inside the `transcripts/` folder.

Example:

```text
transcripts/

├── FGD_01.pdf
├── FGD_02.pdf
├── IDI_01.pdf
├── IDI_02.pdf
```

Generate the FAISS index:

```bash
python build_index.py
```

This process:

* Loads all transcript PDFs
* Extracts text
* Splits documents into chunks
* Generates embeddings
* Creates a FAISS vector database
* Stores metadata for retrieval

Generated files:

```text
faiss_index/
│
├── index.faiss
└── index.pkl

chunks.pkl
```

These files are required before running the Streamlit application.

---

## Running the Application

Launch the Streamlit interface:

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## Example Questions

### Theme Discovery

```text
What are the major barriers to treatment?
```

### Evidence Retrieval

```text
Show quotes supporting efficacy concerns.
```

### Participant Experiences

```text
What negative experiences were reported?
```

### Topic Exploration

```text
What themes emerge across all interviews?
```

### Comparative Analysis

```text
How do urban and rural participants differ in their treatment experiences?
```

### Sentiment Investigation

```text
What concerns were expressed regarding healthcare access?
```

---

## Example Output

```text
Answer:

Cost, stigma, and lack of specialist availability emerged as the most commonly reported barriers to treatment [1][2][3].

Citations:

[1] FGD_07.pdf Page 4
[2] IDI_11.pdf Page 2
[3] FGD_03.pdf Page 5
```

Supporting evidence:

```text
"The consultation fees alone are more than I can afford."

"I delayed treatment because I was worried about how people would react."

"There are very few specialists available in my area."
```

---

## Use Cases

### Healthcare Research

* Patient journey analysis
* Treatment barrier identification
* Adherence research
* Patient experience studies

### Pharmaceutical Research

* Drug perception analysis
* Treatment efficacy concerns
* Side effect monitoring

### Market Research

* Consumer feedback analysis
* Product perception studies
* Brand sentiment analysis

### Social Science Research

* Qualitative interview analysis
* Focus group interpretation
* Policy research

### Public Health

* Vaccine hesitancy studies
* Mental health research
* Access-to-care investigations

---

## Future Enhancements

Planned improvements include:

* Theme extraction dashboard
* BERTopic integration
* Interactive transcript explorer
* PDF report generation
* Conversation history
* Retrieval score visualization
* Speaker-level analysis
* Export to Excel and PDF
* Multi-user authentication
* Cloud deployment

---
## License

This project is intended for educational, research, and portfolio purposes.
