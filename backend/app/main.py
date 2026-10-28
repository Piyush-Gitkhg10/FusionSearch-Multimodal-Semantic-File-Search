# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_file, routes_search
from app.database.postgres import engine, Base

# Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hybrid Multimodal File Search API")

# Configure CORS so the React frontend can communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # The Vite React port
    allow_credentials=True,
    allow_methods=["*"],  # This allows the OPTIONS method!
    allow_headers=["*"],
)

# Include Routers
app.include_router(routes_file.router, prefix="/api/files", tags=["Files"])
app.include_router(routes_search.router, prefix="/api/search", tags=["Search"])


@app.get("/")
def health_check():
    return {"status": "ok", "system": "Hybrid Search API running"}
