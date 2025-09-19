import streamlit as st
import pdfplumber
import pandas as pd
import re
import subprocess
import unicodedata

def common_text_preprocessing(text):
    text = unicodedata.normalize('NFKD',text)
    text = re.sub(r'[^\x20-\x7E\n]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def extract_pdf(file):
    raw_text=''
    
    with pdfplumber.open(file) as pdf:
        page_texts=[]
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                page_texts.append(text)
        raw_text = "\n".join(page_texts)       
    lines =raw_text.splitlines()

    #header/footer
    unique_lines=[]
    seen_lines = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
    
        if lines.count(line) > 2:
            continue
        unique_lines.append(line)

    cleaned = common_text_preprocessing(" ".join(unique_lines))
    return cleaned
    
def extract_excel(file):
    
    df = pd.read_excel(file, header=0)
    df = df.fillna("")
    df.columns = [str(c).strip() for c in df.columns]
    df = df.astype(str).applymap(lambda x: x.strip())

    def clean_number(x):
        if re.match(r'^\d+\.0$', x):
            return x[:-2]
        return x
    df = df.applymap(clean_number)

    rows = []
    for _, row in df.iterrows():
        row_str = " | ".join(row.values)
        rows.append(row_str)

    cleaned_text = " ".join(rows)  
    return cleaned_text

def ask_ollama(prompt, model="mistral"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True,
        
    )
    return result.stdout.decode("utf-8").strip()
   


# Streamlit code

st.set_page_config(page_title="Financial Document Q&A Assistant", layout="wide")
st.title("Financial Document Q&A Assistant")

uploaded_file = st.file_uploader("Upload a financial document (PDF or Excel)", type=["pdf", "xlsx"],key="file_uploader_main")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if uploaded_file:
    st.success("File uploaded")

    with st.spinner("Extracting and cleaning text"):
        if uploaded_file.name.endswith(".pdf"):
            clean_text = extract_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            clean_text = extract_excel(uploaded_file)
        else:
            clean_text = ""

        st.session_state.document_text = clean_text

    st.subheader("Extracted Document Content (Preview)")
    st.text_area("Extracted & Cleaned Text", clean_text[:2000] + "...", height=200,key="preview_area")

if st.session_state.document_text:
    st.subheader("Ask Questions about the Document")

    user_input = st.text_input("Type your question:",key="user_question")

    if user_input:
        with st.spinner("Thinking..."):
            context = f"Here is a cleaned financial document:\n{st.session_state.document_text}\n\n"
            prompt = context + f"Answer the following question clearly and concisely:\nQ: {user_input}\nA:"
            answer = ask_ollama(prompt)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Assistant", answer))

    for speaker, text in st.session_state.chat_history:
        if speaker == "You":
            st.markdown(f"**{speaker}:** {text}")
        else:
            st.markdown(f"**{speaker}:** {text}")