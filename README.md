# 🤖 AI Webpage Assistant

A Chrome extension that lets you **chat with any webpage** using AI. Ask questions about the page you're currently viewing and get instant, context-aware answers — powered by LangChain and Hugging Face.


---

## ✨ Features

- 💬 **Chat interface** — Ask questions about the currently open webpage in a clean, chat-style popup
- 🌐 **Works on any page** — No manual URL entry needed, automatically reads the active tab
- ⚡ **Real-time answers** — Powered by Llama 3.1 8B Instruct via Hugging Face Inference API
- 🎨 **Polished UI** — Smooth animations, loading states, and a modern chat bubble design
- 🛡️ **Graceful error handling** — Friendly fallback messages instead of crashes when a page can't be processed

---

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌───────────────────┐      ┌──────────────────┐
│  Chrome Extension │ ───> │   FastAPI Backend │ ───> │  LangChain Pipeline │ ───> │  Hugging Face LLM │
│  (popup + content) │ <─── │   (/ask endpoint) │ <─── │  (prompt + parser)  │ <─── │  (Llama 3.1 8B)   │
└─────────────────┘      └──────────────────┘      └───────────────────┘      └──────────────────┘
```

1. The extension grabs the URL of the currently active tab
2. It sends the URL + the user's question to a local FastAPI backend
3. The backend scrapes the page content using `WebBaseLoader`
4. LangChain builds a prompt with the page content + question and sends it to the LLM
5. The model's answer is returned to the extension and displayed in the chat UI

---

## 🛠️ Tech Stack

**Frontend (Extension)**
- Chrome Extension (Manifest V3)
- Vanilla JavaScript (async/await, Chrome Tabs API)
- HTML/CSS

**Backend**
- FastAPI
- LangChain
- Hugging Face Inference API (`meta-llama/Llama-3.1-8B-Instruct`)
- `WebBaseLoader` for page content extraction

---

## 📂 Project Structure

```
chat-with-page-extension/
├── extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── style.css
│   └── extension_image.png
├── backend/
│   ├── main.py
└── README.md
```

---

## 🚀 Setup & Installation

### 1. Backend Setup

```bash
cd backend
```


Run the server:

```bash
uvicorn main:app --reload
```

The backend will be running at `http://localhost:8000`.

### 2. Extension Setup

1. Open Chrome and go to `chrome://extensions`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked**
4. Select the `extension` folder
5. Pin the extension and click its icon on any webpage to start chatting!

> ⚠️ Make sure the backend is running before using the extension.

---


---

## ⚠️ Known Limitations

- **JavaScript-heavy pages**: Since content extraction uses `WebBaseLoader` (which fetches raw HTML without executing JavaScript), pages that render their content dynamically via JS (e.g. modern React/Vue sites) may return incomplete content. Static and server-rendered pages (like Wikipedia) work reliably.
- **Very long pages**: Page content is truncated to stay within the LLM's practical context limits on the free Hugging Face Inference tier. Extremely long articles may lose some detail from later sections.
- **Fixed popup size**: Chrome extension popups can't be resized by dragging — the window has a fixed size.

## 🔭 Future Improvements

- Add proper **RAG (Retrieval-Augmented Generation)** with chunking + embeddings + vector search (FAISS/Chroma) to handle long pages without truncation
- Switch to a **Selenium/Playwright-based loader** to support JavaScript-rendered pages
- Add conversation memory so follow-up questions retain context
- Publish to the Chrome Web Store

---

## 🧠 What I Learned

- Building and debugging a Manifest V3 Chrome extension from scratch (permissions, content scripts, async messaging)
- Integrating a FastAPI backend with LangChain and a Hugging Face LLM
- Handling real-world issues: CORS, async JavaScript, host permissions, and scraping limitations on JS-heavy sites
- Designing graceful error handling so the app degrades nicely instead of crashing

---

## 📄 License

This project is for educational/portfolio purposes.