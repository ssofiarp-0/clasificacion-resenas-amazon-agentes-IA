from pydantic_ai import Agent

from config import model

if __name__ == "__main__": 
    agent = Agent(model)

    result = agent.run_sync("Responde con la palabra: OK")

    print(f"Respuesta del modelo: {result.output}")
    print("Conexion establecida correctamente")