
import os
from contextlib import asynccontextmanager
import tomli
import yaml
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.utils import setup_logger


app_logger = setup_logger("Device")


def get_project_metadata():
    try:
        with open("pyproject.toml", "rb") as f:
            data = tomli.load(f)  # Use tomllib.load(f) for Python >= 3.11
            project = data["project"]
            return {
                "title": project["name"].replace("-", " ").title().upper(),
                "version": project["version"],
                "description": project["description"],
            }
    except (FileNotFoundError, KeyError):
        return {
            "title": "device",
            "version": "0.2.0",
            "description": "Quản lý thiết bị",
        }


def write_openapi_yaml(schema: dict):
    with open("openapi.yaml", "w", encoding="utf-8") as f:
        yaml.dump(schema, f, sort_keys=False, allow_unicode=True)


def setup_middleware(app: FastAPI):
    # Thiết lập CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],  # Trong môi trường production, nên giới hạn các origin cụ thể
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # Generate OpenAPI Schema
    openapi_schema = get_openapi(
        title=metadata["title"],
        version=metadata["version"],
        description=metadata["description"],
        routes=app.routes,
    )

    # Write OpenAPI YAML file
    write_openapi_yaml(openapi_schema)

    yield

    app_logger.error("Shutting down the server")


metadata = get_project_metadata()
app = FastAPI(
    docs_url="/",
    lifespan=lifespan,
    openapi_url="/openapi.json",
    title=metadata["title"],
    version=metadata["version"],
    description=metadata["description"],
)

app.include_router(api_router)


@app.get("/openapi.yaml", include_in_schema=False)
async def get_openapi_yaml():
    return FileResponse("openapi.yaml", media_type="text/yaml")
