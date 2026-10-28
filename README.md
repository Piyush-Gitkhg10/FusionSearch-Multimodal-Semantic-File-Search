# 🔎 FusionSearch - Multimodal Semantic File Search System

**Find files by meaning, not just by filename.**

FusionSearch is an AI-powered file search application designed to make finding relevant information easier and more intuitive. It combines semantic search, vector similarity, and a modern web interface to help users discover relevant content through natural-language queries.

Instead of relying entirely on exact keyword matches, FusionSearch uses AI-driven representations of content to make searching more meaningful.

---

## ✨ Features

- 🧠 **Semantic Search** — Search using natural-language queries and discover relevant content based on meaning.
- 🔍 **AI-Powered Retrieval** — Use vector similarity search to retrieve relevant results.
- 🗂️ **File Management API** — Organize file-related operations through a dedicated backend API.
- ⚡ **FAISS Vector Search** — Leverage efficient similarity search over vector representations.
- 🤖 **Sentence Transformers** — Generate text embeddings for semantic retrieval.
- 🗄️ **PostgreSQL Integration** — Store and manage structured application metadata.
- 🌐 **Modern Web Interface** — A React-based frontend powered by Vite.
- 🚀 **FastAPI Backend** — Build and serve API endpoints with Python.
- 🔗 **Frontend–Backend Integration** — Connect the user interface to the backend using Axios.
- 🧩 **Modular Architecture** — Keep frontend, API routes, database access, and search functionality organized separately.

---

## 🏗️ System Architecture

FusionSearch separates the frontend, backend, metadata storage, and vector search components to support a modular search workflow.

```mermaid
flowchart TD
    A["👤 User"] --> B["React + Vite Frontend"]
    B --> C["FastAPI Backend"]
    C --> D["File Management API"]
    C --> E["Semantic Search API"]
    D --> F[("PostgreSQL")]
    E --> G["Embedding Generation"]
    G --> H[("FAISS Vector Index")]
    E --> I["Google GenAI SDK"]
    F --> E
    H --> E
    E --> C
    C --> B
    B --> J["🔎 Ranked Search Results"]
```

### How It Works

1. **User interaction:** The user interacts with the web interface to perform file-related operations or submit a search query.
2. **API communication:** The React frontend communicates with the FastAPI backend.
3. **Content representation:** The semantic search pipeline uses embedding models to represent supported content as vectors.
4. **Similarity search:** FAISS helps identify vectors that are similar to the search query.
5. **Metadata access:** PostgreSQL provides structured data storage for the application.
6. **Results delivery:** The backend returns search results to the frontend for presentation.

*The diagram illustrates the intended high-level architecture; individual processing steps depend on the implemented search pipeline.*

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| React 19 | Frontend user interface |
| Vite | Frontend development server and build tool |
| Tailwind CSS 4 | Interface styling |
| Axios | HTTP communication |
| Lucide React | Interface icons |
| Python | Backend development |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| Sentence Transformers | Semantic embedding generation |
| FAISS CPU | Vector similarity search |
| PostgreSQL | Relational database |
| SQLAlchemy | Database access and ORM |
| Psycopg2 | PostgreSQL connectivity |
| Google GenAI SDK | Google generative AI integration |
| Pydantic | Data validation |
| Pillow | Image processing utilities |

---

## 📁 Project Structure

The repository separates the application into two main components:

```text
FusionSearch-Multimodal-Semantic-File-Search/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── routes_file.py
│   │   │   └── routes_search.py
│   │   └── database/
│   │       └── postgres.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

*The structure above highlights the known application entry point, API routers, database module, and frontend project. Other files and directories may exist in the repository.*

---

## ⚙️ Getting Started

Follow these steps to set up FusionSearch locally.

### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/downloads/)

You will also need a Google GenAI API key if your configured application features use Google's API.

### 1. Clone the Repository

```bash
git clone https://github.com/Piyush-Gitkhg10/FusionSearch-Multimodal-Semantic-File-Search.git
```

Navigate into the project directory:

```bash
cd FusionSearch-Multimodal-Semantic-File-Search
```

### 2. Set Up the Backend

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the backend dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure PostgreSQL and Environment Variables

Ensure that PostgreSQL is installed and running, and create a database for FusionSearch.

Configure the database connection and any required API credentials according to the environment-variable names expected by the backend configuration.

For example, your local configuration may contain values in this general format:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/fusionsearch
GOOGLE_API_KEY=your_google_api_key
```

**Important:** These are illustrative variable names. Confirm the exact names expected by the implementation before using them. Do not commit credentials or your actual `.env` file to GitHub.

### 4. Start the Backend Server

From the `backend` directory, run:

```bash
uvicorn app.main:app --reload
```

The API should be available at:

- **Base URL:** http://127.0.0.1:8000
- **Interactive API documentation:** http://127.0.0.1:8000/docs
- **Alternative API documentation:** http://127.0.0.1:8000/redoc

The application defines a root health-check endpoint at `/` that returns a basic API status response.

### 5. Set Up the Frontend

Open a second terminal and navigate to the frontend directory:

```bash
cd FusionSearch-Multimodal-Semantic-File-Search/frontend
```

Install the Node.js dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will display the local development URL in your terminal, typically:

http://localhost:5173

Open the displayed URL in your browser to access the frontend.

### 6. Run the Application

For local development, keep both servers running:

| Component | Command | Default URL |
|---|---|---|
| Backend | `uvicorn app.main:app --reload` | `http://127.0.0.1:8000` |
| Frontend | `npm run dev` | `http://localhost:5173` |

Make sure the backend's CORS configuration and the frontend's API base URL match your local setup.

---

## 🔎 Semantic Search: The Core Idea

Traditional search typically depends on matching words, filenames, or manually assigned tags.

Semantic search aims to retrieve content based on the meaning of a query.

For example:

| Search query | Intended behavior |
|---|---|
| `machine learning study notes` | Find content related to machine learning notes |
| `documents about hospital management` | Retrieve relevant hospital management material |
| `files discussing financial planning` | Find content related to financial planning |
| `AI applications in healthcare` | Identify relevant healthcare and AI content |

These are illustrative queries, not verified test results from the application.

The underlying idea is to represent content and queries as numerical embeddings, then use similarity search to identify relevant candidates.

---

## 🧠 Key Technical Concepts

### 1. Embeddings

Embeddings transform text or other supported inputs into numerical vectors that capture semantic information. Similar concepts can be represented by nearby vectors in an embedding space.

### 2. Vector Similarity Search

FAISS provides tools for searching collections of vectors efficiently, making it useful for semantic retrieval applications.

### 3. Relational Metadata

PostgreSQL and SQLAlchemy provide structured storage and database access for application records and metadata.

### 4. API-Driven Architecture

FastAPI exposes dedicated file and search routers, allowing the frontend and backend to communicate through HTTP requests.

### 5. AI Integration

The project includes the Google GenAI SDK for generative AI capabilities, alongside embedding and vector-search dependencies.

---

## 🧪 Development

### Frontend

Run the development server:

```bash
npm run dev
```

Create a production build:

```bash
npm run build
```

Run lint checks:

```bash
npm run lint
```

Preview the production build locally:

```bash
npm run preview
```

### Backend

Start the API in development mode:

```bash
uvicorn app.main:app --reload
```

Explore and test the available API routes through the automatically generated Swagger UI at `/docs`.

---

## 🔐 Security Considerations

When configuring FusionSearch for local development or deployment:

- Keep API keys and database credentials in environment variables.
- Add `.env` files and virtual environments to `.gitignore`.
- Never expose production database credentials in frontend code.
- Restrict CORS origins appropriately for production deployments.
- Validate uploaded files and enforce sensible file-size limits.
- Apply authentication and authorization where private file collections require them.
- Review database permissions and error handling before deploying publicly.

---

## 🎯 Project Goals

FusionSearch explores how modern AI and software engineering techniques can improve the way users interact with their digital files.

The project brings together:

- Semantic search and vector retrieval.
- Backend API development.
- Relational database integration.
- Modern frontend development.
- AI service integration.
- Modular application architecture.

It serves as a practical exploration of building an AI-assisted search application using a full-stack architecture.

---

## 👨‍💻 Author

**Piyush Kumar**

MCA Student | Artificial Intelligence & Machine Learning

- GitHub: [@Piyush-Gitkhg10](https://github.com/Piyush-Gitkhg10)
- Project Repository: [FusionSearch](https://github.com/Piyush-Gitkhg10/FusionSearch-Multimodal-Semantic-File-Search)
