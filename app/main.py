from fastapi import FastAPI
from app.api.main import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ORC's FastAPI")

app.add_middleware(CORSMiddleware,allow_origins=["*"])

app.include_router(api_router)