#  Financial Document Q&A Assistant

A lightweight Streamlit app that lets you upload **financial documents (PDF or Excel)**, extracts the text, cleans it up, and lets you **ask questions** using an Ollama LLM (default model: `mistral`).

---

##  Features
- Upload PDF or Excel files
- Text extraction + cleaning 
- Preview of the cleaned document
- Simple Q&A interface powered by Ollama

---

## Setup

1. Clone the repo (or just download the files):

   ```bash
   git clone https://github.com/itsmeaj18/Financial-Document-Q-A-Assistant.git
   cd Financial-Document-Q-A-Assistant

   ```

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate    # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install [Ollama](https://ollama.ai/download) if you haven’t already.

5. Pull the Mistral model:

   ```bash
   ollama pull mistral
   ```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

- Upload a PDF or Excel file  
- Check the extracted content preview  
- Type your question and get an answer 🎯  

---

## Project Structure

```
financial-doc-qa/
│
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
└── README.md           # This file
---



