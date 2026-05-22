import os

from fastapi import ( #type: ignore
    FastAPI,

)
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from routers import api_router


# Créez l'application FastAPI
app = FastAPI()

# CORS configurable via variable d'environnement
cors_origin = os.getenv("CORS_ORIGIN", "https://preprod.azert.fr")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluez le routeur API avec le préfixe /api
app.include_router(api_router, prefix="/api")