<!DOCTYPE html>
<html lang="en">
<body>

<h1> RAG Q&A Application (Whisper + FAISS + Groq)</h1>

<p>
A <strong>Retrieval-Augmented Generation (RAG)</strong> application built with
<strong>Streamlit</strong> that allows users to ask questions from:
</p>

<ul>
  <li>YouTube videos</li>
  <li>Audio files</li>
  <li>PDF documents</li>
  <li>DOCX files</li>
  <li>TXT files</li>
  <li>Web pages</li>
  <li>Raw text input</li>
</ul>

<p>
The application transcribes audio using <strong>Whisper</strong>, creates vector
embeddings using <strong>FastEmbed + FAISS</strong>, and generates answers using
<strong>Groq-hosted LLMs</strong>.
</p>

<div class="section">
  <h2> Key Features</h2>
  <ul>
    <li> YouTube & audio transcription using Whisper </li>
    <li> Note: You should install ffmpeg </li>
    <li> Supports PDF, DOCX, TXT, web links, and plain text</li>
    <li> Chunking with overlap for better retrieval accuracy</li>
    <li> FAISS vector search for fast similarity retrieval</li>
    <li> Groq-powered LLM responses</li>
    <li> Secure API key input via sidebar</li>
    <li> Cached models for fast performance</li>
  </ul>
</div>

<div class="section">
  <h2> Tech Stack</h2>

  <span class="badge">Python</span>
  <span class="badge">Streamlit</span>
  <span class="badge">Whisper</span>
  <span class="badge">FAISS</span>
  <span class="badge">FastEmbed</span>
  <span class="badge">LangChain</span>
  <span class="badge">Groq</span>
  <span class="badge">yt-dlp</span>
</div>

<div class="section">
  <h2> Project Architecture</h2>
  <pre>
rag-qa-app/
│
├── app.py
├── requirements.txt
└── README.html   (optional )

  </pre>
</div>

<div class="section">
  <h2> How It Works</h2>

  <ol>
    <li>User provides content (file, link, or text)</li>
    <li>Content is extracted and cleaned</li>
    <li>Text is split into overlapping chunks</li>
    <li>Chunks are embedded and stored in FAISS</li>
    <li>User asks a question</li>
    <li>Relevant chunks are retrieved</li>
    <li>Groq LLM answers using only retrieved context</li>
  </ol>
</div>

<div class="section">
  <h2> Groq Models Supported</h2>
  <ul>
    <li><code>llama-3.1-8b-instant</code></li>
    <li><code>llama-3.1-70b-versatile</code></li>
    <li><code>mixtral-8x7b-32768</code></li>
  </ul>
</div>

<div class="section">
  <h2> Setup Instructions</h2>

  <h3>1️⃣ Install Dependencies</h3>
  <pre>
pip install streamlit whisper yt-dlp faiss-cpu langchain langchain-community langchain-groq fastembed pypdf python-docx
  </pre>

  <h3>2️⃣ Run the App</h3>
  <pre>
streamlit run app.py
  </pre>

  <h3>3️⃣ Enter Groq API Key</h3>
  <p>
Get your API key from:
<br />
<a href="https://console.groq.com" target="_blank">https://console.groq.com</a>
</p>
</div>

<div class="section">
  <h2>🧪 Example Use Cases</h2>
  <ul>
    <li>Ask questions from long YouTube lectures</li>
    <li>Query PDFs like resumes, books, or reports</li>
    <li>Analyze meeting recordings</li>
    <li>Research from web articles</li>
  </ul>
</div>

<div class="section">
  <h2> Notes</h2>
  <ul>
    <li>Answers are strictly based on retrieved context</li>
    <li>If information is missing, the model states it clearly</li>
    <li>Temporary audio files are auto-deleted</li>
  </ul>
</div>


<div class="section">
  <h2> Author</h2>
  <p>
<strong>Jagadeeswar Pattupogula</strong><br />
RAG • AI • Full-Stack Development
  </p>
</div>

</body>
</html>
