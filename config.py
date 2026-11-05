import os
import shutil
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

ROOT = Path(__file__).parent
DOCUMENT_DIR = ROOT / "Documents"
WORKSPACE_DIR = ROOT / "workspace"

Sentiment = Literal["positivo", "negativo", "neutro"]
Category = Literal["precio", "envio", "calidad", "atencion_cliente", "otro"]
Confidence = Literal["high", "medium", "low"]

model = OpenAIResponsesModel(
    os.environ["MODEL"], 
    provider = OpenAIProvider(
        base_url = os.environ["OPEN_AI_BASE_URL"], 
        api_key = os.environ["OPENAI_API_KEY"]
    ),
)


def create_workspace(path: Path) -> None:
    """Copy the original documents into `path/inbox`, discarding any previous run."""
    shutil.rmtree(path, ignore_errors=True)
    shutil.copytree(DOCUMENT_DIR, path / "inbox")
