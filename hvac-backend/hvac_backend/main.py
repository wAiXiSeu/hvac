import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yaml
from pathlib import Path

from hvac_backend.modbus_client import ModbusClient
from hvac_backend.router import router as api_router
from hvac_backend.state import AppState


# Load config
def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    config = load_config()
    
    # Initialize Modbus client
    modbus_client = ModbusClient(config["modbus"])
    
    # Initialize app state
    app.state = AppState(config=config, modbus_client=modbus_client)
    
    # Start background tasks
    asyncio.create_task(modbus_client.auto_reconnect())
    asyncio.create_task(modbus_client.poll_environment_data())
    
    yield
    
    # Shutdown
    await modbus_client.disconnect()


# Create FastAPI app
app = FastAPI(
    title="HVAC Control API",
    description="三恒系统本地控制 API",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "HVAC Control API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}
