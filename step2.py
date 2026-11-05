import shutil
from pathlib import Path
from pydantic_ai import Agent, UsageLimits

from config import model, Sentiment, Category, DOCUMENT_DIR, Confidence, WORKSPACE_DIR

INSTRUCTIONS = """\
You classify customer reviews for products sold on Amazon. Categories:
- positive: the review is favorable, expressing satisfaction, praise, or strong points.
- negative: the review is critical, reporting defects, bad experience, or dissatisfaction.
- neutral: the review is balanced, mixed, purely objective, or lacks a clear opinion.
- spam_fake: the review seems irrelevant, bot-generated, self-promotional, or incomprehensible.
- other: anything that does not fit into the categories above.

List the documents, then read each one, classify it and move it with `move_document`.
Work on one document at a time: never read or move more than one document at once.
When the inbox is empty, reply with a short summary.
"""


agent = Agent(model, system_prompt = INSTRUCTIONS)

@agent.tool_plain
def list_documents() -> list[str]: 
    """List the review documents waitinf in the documents / inbox folder"""
    inbox = WORKSPACE_DIR / "inbox"
    if not inbox.exists():
        return []

    names = [path.name for path in inbox.iterdir() if path.is_file()]
    return sorted(names)

@agent.tool_plain
def read_document(filename: str) -> str:
    """Read a review document from the inbox"""
    print(f"Leyendo: {filename}")

    path = WORKSPACE_DIR / "inbox" / filename
    if not path.exists(): 
        return f"El archivo {filename} no está en la bandeja de entrada"
    return path.read_text(encoding = "utf-8")



@agent.tool_plain
def move_document(filename: str, category: Category, confidence: Confidence, reason: str) -> str:
    """"Move a review document from inbox to its corresponding category folder."""
    print(f"Moviendo {filename} -> {category} | confianza: {confidence} | motivo: {reason}")

    source = DOCUMENT_DIR / "inbox" / filename
    dest_dir = DOCUMENT_DIR / category

    if not source.exists(): 
        return f"El archivo {filename} no existe"

    dest_dir.mkdir(parents = True, exist_ok = True)

    shutil.move(source, dest_dir / filename)

    return f"El documento {filename} ha sido movido con exito a {category}"


def preparar_entorno(): 
    """Asegura que exista la carpeta Documents/inbox para las pruebas"""
    inbox = DOCUMENT_DIR / "inbox"
    inbox.mkdir(parents = True, exist_ok = True)


if __name__ == "__main__": 
    preparar_entorno()

    print("Iniciando procesador automático de reseñas...\n")
    result = agent.run_sync(
        "Process the inbox.",
        usage_limits=UsageLimits(request_limit=100),
    )

    print("\n--- RESUMEN FINAL ---")
    print(result.output)