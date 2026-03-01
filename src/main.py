"""FastAPI implementation of the Todo REST API."""

from fastapi import FastAPI
from .routers import todos


# 'app' is refers to FastAPI
# use param: redirect_slashes=False to disable automatic
# redirection of paths without trailing slash.
app = FastAPI(title="Todo REST API")


### REST service URLs and request handlers ###
app.include_router(todos.router)
