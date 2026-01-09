"""Agent"""
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.events.lifespan import init_db, start_sqs_consumer, stop_sqs_consumer
import app.core.api_config_agent as api_config_agent
from app.loggers.loggers import LOGGING_CONFIG
from app.routes.health import router as health_router


origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos del ciclo de vida de la aplicación."""
    # Inicializar la base de datos
    await init_db()

    # Iniciar el consumidor SQS en un hilo separado
    start_sqs_consumer()

    # Ceder el control a FastAPI
    yield

    # Código que se ejecuta al apagar la aplicación
    stop_sqs_consumer()
    logging.info("Aplicación detenida correctamente")

# Crear la aplicación FastAPI
app = FastAPI(**api_config_agent.fastAPI_Options, lifespan=lifespan)

# Incluir routers
app.include_router(health_router)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Punto de entrada para uvicorn cuando se ejecuta como "uvicorn app.agent:app"
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.agent:app", host="0.0.0.0", port=8001,
                reload=True, log_config=LOGGING_CONFIG)
