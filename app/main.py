from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.routers import warehouses, locations, items
import os

# Crear tablas al iniciar
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")
    yield
    # Shutdown
    print("🛑 App cerrando...")

app = FastAPI(
    title="ColdStore Manager API",
    description="API para gestión de almacén frío, contenedores y seco",
    version="1.0.0",
    lifespan=lifespan
)

# ========== CORS ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== ROUTERS ==========
app.include_router(warehouses.router)
app.include_router(locations.router)
app.include_router(items.router)

# ========== SERVIR FRONTEND ==========
# Montar carpeta static
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Servir index.html en raíz
@app.get("/")
async def root():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "✅ ColdStore Manager API está corriendo!"}

@app.get("/frontend")
async def frontend():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"error": "Frontend no disponible"}