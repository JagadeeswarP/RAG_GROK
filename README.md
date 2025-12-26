<!DOCTYPE html>
<html lang="en">
<head>
 
</head>

<body>

<h1> Jagadeeswar's RAG-based Q&A System </h1>

<p>
A <strong>Retrieval-Augmented Generation (RAG)</strong> application built with
<strong>Python</strong>, <strong>Streamlit</strong>, <strong>LangChain</strong>,
<strong>FAISS</strong>, <strong>FastEmbed</strong>, <strong>Whisper</strong>, and
<strong>Groq LLMs</strong>.
</p>

<p>
This system allows users to ingest knowledge from <strong>documents, web pages,
YouTube videos, and audio files</strong>, then ask natural-language questions that are
answered <strong>strictly from the retrieved content</strong>.
</p>

<hr />

<h2> Features</h2>
<ul>
  <li>📥 Multi-source input support:
    <ul>
      <li>Web URLs</li>
      <li>YouTube videos</li>
      <li>Audio files (.mp3, .wav, .m4a)</li>
      <li>PDF documents</li>
      <li>DOCX documents</li>
      <li>TXT files</li>
      <li>Raw text input</li>
    </ul>
  </li>
  <li>🎧 Automatic audio & video transcription using Whisper</li>
  <li>🧩 Local embeddings using FastEmbed (nomic-embed-text-v1.5)</li>
  <li>🔍 Semantic search powered by FAISS</li>
  <li>⚡ Ultra-fast inference using Groq LLMs</li>
  <li>🛡️ Context-grounded answers with hallucination control</li>
  <li>🧹 Automatic temporary file cleanup</li>
  <li>🔄 Session-based vector indexing and reset support</li>
</ul>

<hr />

<h2>🏗️ Architecture Overview</h2>

<pre>
User Input (Link / PDF / Audio / Text)
            ↓
Content Extraction
  - Web scraping (WebBaseLoader)
  - YouTube/audio download (yt-dlp)
  - Transcription (Whisper)
            ↓
Text Chunking
(RecursiveCharacterTextSplitter)
            ↓
Embeddings
(FastEmbed – nomic-embed-text-v1.5)
            ↓
FAISS Vector Store (In-Memory)
            ↓
Retriever (Top-K Similar Chunks)
            ↓
Groq LLM (Context-Aware Prompt)
            ↓
Answer (Based Only on Retrieved Content)
</pre>

<hr />

<h2>🧠 Tech Stack</h2>

<table border="1" cellpadding="6" cellspacing="0">
  <tr>
    <th>Component</th>
    <th>Technology</th>
  </tr>
  <tr>
    <td>UI</td>
    <td>Streamlit</td>
  </tr>
  <tr>
    <td>LLM</td>
    <td>Groq (LLaMA 3.1 / Mixtral)</td>
  </tr>
  <tr>
    <td>Embeddings</td>
    <td>FastEmbed (nomic-embed-text-v1.5)</td>
  </tr>
  <tr>
    <td>Vector Store</td>
    <td>FAISS</td>
  </tr>
  <tr>
    <td>Audio Transcription</td>
    <td>Whisper</td>
  </tr>
  <tr>
    <td>Document Processing</td>
    <td>PyPDF2, python-docx</td>
  </tr>
  <tr>
    <td>YouTube Audio</td>
    <td>yt-dlp + FFmpeg</td>
  </tr>
  <tr>
    <td>Language</td>
    <td>Python</td>
  </tr>
</table>

<hr />

<h2>📦 Installation (Local)</h2>

<h3>1️⃣ Clone the repository</h3>
<pre>
git clone https://github.com/JagadeeswarP/RAG_GROK.git
cd RAG_GROK
</pre>

<h3>2️⃣ Create virtual environment (recommended)</h3>
<pre>
python -m venv .venv
source .venv/bin/activate
</pre>

<p><strong>Windows</strong></p>
<pre>
.venv\Scripts\activate
</pre>

<h3>3️⃣ Install dependencies</h3>
<pre>
pip install -r requirements.txt
</pre>

<h3>4️⃣ Run the application</h3>
<pre>
streamlit run app.py
</pre>

<hr />

<h2>🔐 API Configuration</h2>

<p>
The application requires a <strong>Groq API key</strong> for LLM inference.
The key is entered securely via the Streamlit sidebar and is not stored in code.
</p>

<hr />

<h2>🧪 Supported Inputs</h2>

<table border="1" cellpadding="6" cellspacing="0">
  <tr>
    <th>Input Type</th>
    <th>Supported</th>
  </tr>
  <tr><td>Web URLs</td><td>✅</td></tr>
  <tr><td>YouTube Videos</td><td>✅</td></tr>
  <tr><td>Audio Files</td><td>✅</td></tr>
  <tr><td>PDF</td><td>✅</td></tr>
  <tr><td>DOCX</td><td>✅</td></tr>
  <tr><td>TXT</td><td>✅</td></tr>
  <tr><td>Raw Text</td><td>✅</td></tr>
</table>

<hr />

<h2>🔐 Hallucination Control</h2>

<p>
The Groq LLM is prompted to answer <strong>only using retrieved context</strong>.
If the answer is not present in the indexed content, the system explicitly states that
the information is unavailable.
</p>

<hr />

<h2>⚠️ Limitations</h2>
<ul>
  <li>FAISS vector store is in-memory (resets on restart)</li>
  <li>Large documents increase indexing time</li>
  <li>Requires FFmpeg for YouTube/audio processing</li>
  <li>Not optimized for multi-user concurrent deployments</li>
</ul>

<hr />

<h2>📈 Future Enhancements</h2>
<ul>
  <li>Persistent vector storage</li>
  <li>Source citation in answers</li>
  <li>Multi-document indexing</li>
  <li>User authentication</li>
  <li>Dockerized deployment</li>
</ul>

<hr />

<h2>👨‍💻 Author</h2>
<p>
<strong>Jagadeeswar Pattupogula</strong><br />
GitHub:
<a href="https://github.com/JagadeeswarP" target="_blank">github.com/JagadeeswarP</a><br />
LinkedIn:
<a href="https://www.linkedin.com/in/jagadeeswar-pattupogula" target="_blank">
linkedin.com/in/jagadeeswar-pattupogula
</a>
</p>

<hr />

<h2>⭐ If you like this project</h2>
<ul>
  <li>Give it a ⭐ on GitHub</li>
  <li>Fork and extend the RAG pipeline</li>
  <li>Use it as a foundation for production RAG systems</li>
</ul>

</body>
</html>
