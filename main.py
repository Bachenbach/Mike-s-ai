# app/main.py
from fastapi import FastAPI, HTTPException, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
import asyncio
import uvicorn
from datetime import datetime
import json

from core.api_integration.api_orchestrator import APIOrchestrator
from core.nlp.language_processor import LanguageProcessor
from core.nlp.context_manager import ContextManager
from core.database.mongodb_handler import MongoDBHandler

app = FastAPI(title="Advanced AI System API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize core components
api_orchestrator = APIOrchestrator()
language_processor = LanguageProcessor()
context_manager = ContextManager()
db_handler = MongoDBHandler()
