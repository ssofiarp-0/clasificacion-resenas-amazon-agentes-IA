from pathlib import Path
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from config import model

class Clasificacion(BaseModel): 
    sentimiento: str = Field(description="El sentimiento general de la reseña: Positivo, Neutro o Negativo")
    categoria: str = Field(description="Categoría a la que pertenece el producto (ej. Electrónica, Hogar, Ropa, etc.)")
    resumen: str = Field(description="Un resumen breve de 1 línea con el punto clave del cliente")

INSTRUCTIONS = """\
You classify customer reviews for products sold on Amazon. Categories:
- positive: the review is favorable, expressing satisfaction, praise, or strong points.
- negative: the review is critical, reporting defects, bad experience, or dissatisfaction.
- neutral: the review is balanced, mixed, purely objective, or lacks a clear opinion.
- spam_fake: the review seems irrelevant, bot-generated, self-promotional, or incomprehensible.
- other: anything that does not fit into the categories above.
"""

# Cambiado instructions por system_prompt
agent = Agent(
    model, 
    output_type=Clasificacion, 
    system_prompt=INSTRUCTIONS
)

if __name__ == "__main__": 
    ruta = Path(__file__).parent / "Documents" / "resena_01.txt"
    
    if not ruta.exists():
        print(f"Error: No existe el archivo en {ruta}")
    else:
        resena = ruta.read_text(encoding="utf-8")

        print(f"Leyendo reseña desde {ruta}...")
        result = agent.run_sync(resena)
        
        # Cambiado result.output por result.data
        print(result.output.model_dump_json(indent=2))