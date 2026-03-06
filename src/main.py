"""FastAPI implementation of the Todo REST API."""

from . import logging_config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import todos

logging_config.configure_logging()

# 'app' is refers to FastAPI
# use param: redirect_slashes=False to disable automatic
# redirection of paths without trailing slash.
app = FastAPI(title="Todo REST API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

### REST service URLs and request handlers ###
app.include_router(todos.router)
