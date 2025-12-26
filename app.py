import os
import re
import streamlit as st
import whisper
import yt_dlp

from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_community.embeddings import FastEmbedEmbeddings

# =========================
# CONFIG
# =========================
EMBED_MODEL = "nomic-ai/nomic-embed-text-v1.5"

GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-70b-versatile",
    "mixtral-8x7b-32768",
]

# =========================
# LOAD MODELS (CACHED)
# =========================
@st.cache_resource
def load_embedder():
    """Load FastEmbed through LangChain wrapper for FAISS compatibility"""
    return FastEmbedEmbeddings(model_name=EMBED_MODEL)

@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

embedder = load_embedder()
whisper_model = load_whisper()

# =========================
# HELPERS
# =========================
def clean_answer(text: str) -> str:
    """Remove thinking tags from LLM output"""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

def download_audio(url: str) -> str:
    """Download audio from URL (YouTube, direct links, etc.)"""
    output = "temp_audio.mp3"
    
    # Clean up any existing temp files
    for ext in [".mp3", ".m4a", ".wav", ".webm"]:
        if os.path.exists(f"temp_audio{ext}"):
            os.remove(f"temp_audio{ext}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "temp_audio.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise RuntimeError(f"Audio download failed: {str(e)}")

    if not os.path.exists(output) or os.path.getsize(output) == 0:
        raise RuntimeError("Audio download failed or file is empty.")

    return output

def audio_to_text(path: str) -> str:
    """Transcribe audio file using Whisper"""
    try:
        result = whisper_model.transcribe(path, fp16=False, verbose=False)
        text = result.get("text", "").strip()
        
        if not text:
            raise RuntimeError("No speech detected in audio.")
        return text
    finally:
        # Always clean up the audio file
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

# =========================
# INPUT PROCESSING
# =========================
def process_input(input_type, input_data):
    """Process various input types and return a vector store"""
    
    if not input_data:
        raise ValueError("No input data provided")

    if input_type == "Link":
        if not input_data.startswith(("http://", "https://")):
            raise ValueError("Please enter a valid URL starting with http:// or https://")
            
        # Check if it's audio/video content
        if any(x in input_data for x in ["youtube.com", "youtu.be", ".mp3", ".wav", ".m4a"]):
            st.info("Downloading and transcribing audio...")
            audio = download_audio(input_data)
            text = audio_to_text(audio)
        else:
            # Web scraping
            loader = WebBaseLoader(input_data)
            docs = loader.load()
            text = "\n".join(d.page_content for d in docs)

    elif input_type == "PDF":
        pdf = PdfReader(BytesIO(input_data.read()))
        text = "\n".join(p.extract_text() or "" for p in pdf.pages)

    elif input_type == "DOCX":
        doc = Document(BytesIO(input_data.read()))
        text = "\n".join(p.text for p in doc.paragraphs)

    elif input_type == "TXT":
        text = input_data.read().decode("utf-8")

    elif input_type == "Text":
        text = input_data

    else:
        raise ValueError("Unsupported input type")

    # Validate extracted text
    text = text.strip()
    if not text or len(text) < 10:
        raise ValueError("Extracted text is too short or empty")

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)

    if not chunks:
        raise ValueError("No content chunks created from input")

    # Create vector store using LangChain's FastEmbedEmbeddings wrapper
    vectorstore = FAISS.from_texts(
        texts=chunks,
        embedding=embedder
    )

    return vectorstore

# =========================
# QA
# =========================
def answer_question(vectorstore, query, groq_api_key, groq_model):
    """Answer a question using RAG"""
    
    if not query or not query.strip():
        raise ValueError("Please enter a valid question")

    # Retrieve relevant documents
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found in the indexed content."

    context = "\n\n".join(d.page_content for d in docs)

    # Initialize Groq LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=groq_model,
        temperature=0.2
    )

    prompt = f"""Answer the question based ONLY on the context provided below.
If the answer cannot be found in the context, clearly state that the information is not available.

Context:
{context}

Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    return clean_answer(response.content)

# =========================
# UI
# =========================
def main():
    st.set_page_config("RAG App", layout="wide")
    st.title("🧠 RAG App (Whisper + FAISS + Groq)")
    st.caption("Process YouTube videos, audio files, documents, and web pages • Ask questions using AI")

    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    groq_api_key = st.sidebar.text_input("Groq API Key", type="password", help="Get your API key from https://console.groq.com")
    groq_model = st.sidebar.selectbox("Groq Model", GROQ_MODELS, index=1)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 How to use")
    st.sidebar.markdown("""
1. Enter your Groq API key
2. Choose input source and provide content
3. Click 'Process Input' to index
4. Ask questions about the content
    """)

    if not groq_api_key:
        st.warning("⚠️ Please enter your Groq API key in the sidebar to continue.")
        st.stop()

    # Initialize session state
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "last_input" not in st.session_state:
        st.session_state.last_input = None

    st.subheader("📥 Input Source")
    
    input_type = st.selectbox(
        "Select input type",
        ["Link", "PDF", "DOCX", "TXT", "Text"]
    )

    input_data = None
    
    if input_type == "Link":
        input_data = st.text_input("Enter URL (YouTube, web page, audio file)")
        st.caption("Supports: YouTube videos, web pages, direct audio links (.mp3, .wav, .m4a)")
    elif input_type == "Text":
        input_data = st.text_area("Enter or paste text", height=200)
    else:
        input_data = st.file_uploader(f"Upload {input_type} file", type=input_type.lower())

    if st.button("🚀 Process Input", use_container_width=True):
        if not input_data:
            st.error("Please provide input data")
        else:
            try:
                with st.spinner("🔄 Processing and indexing content..."):
                    st.session_state.vectorstore = process_input(input_type, input_data)
                    st.session_state.last_input = input_type
                st.success("✅ Content indexed successfully! You can now ask questions.")
            except Exception as e:
                st.error(f"❌ Error processing input: {str(e)}")
                st.session_state.vectorstore = None

    st.markdown("---")
    st.subheader("💬 Ask Questions")
    
    if st.session_state.vectorstore:
        st.success(f"📚 Content loaded ({st.session_state.last_input})")
        
        query = st.text_input("What would you like to know?")
        
        if st.button("🔍 Ask", use_container_width=True):
            if not query:
                st.warning("Please enter a question")
            else:
                try:
                    with st.spinner("🤔 Thinking..."):
                        answer = answer_question(
                            st.session_state.vectorstore,
                            query,
                            groq_api_key,
                            groq_model
                        )
                    st.markdown("### 💡 Answer")
                    st.markdown(answer)
                except Exception as e:
                    st.error(f"❌ Error generating answer: {str(e)}")
        
        if st.button("🗑️ Clear Content"):
            st.session_state.vectorstore = None
            st.session_state.last_input = None
            st.rerun()
    else:
        st.info("👆 Process some content first to start asking questions")

if __name__ == "__main__":
    main()