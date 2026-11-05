# Clasificador Automático de Reseñas de Amazon con Pydantic AI

Este repositorio contiene un sistema modular desarrollado en Python para el procesamiento, análisis y organización automatizada de reseñas de productos de Amazon alojadas en ficheros de texto plano. La arquitectura implementa la librería `pydantic-ai` e integra modelos de lenguaje de OpenAI (`gpt-4o-mini`) para la ejecución de tareas estructuradas y flujos de trabajo con agentes autónomos.

## Descripción General

El proyecto aborda la clasificación de opiniones de clientes mediante dos aproximaciones técnicas:

1. **Extracción y Validación de Estructuras (Schema Validation):** Garantiza que las respuestas emitidas por el modelo de lenguaje cumplan de forma estricta con esquemas definidos mediante Pydantic.
2. **Agentes Basados en Herramientas (Tool-Calling Agents):** Proporciona al modelo la capacidad de interactuar directamente con el sistema de archivos local para buscar, leer y reorganizar ficheros según la categoría identificada.
3. **Supervisión Humana (Human-in-the-Loop):** Permite pausar la ejecución del agente ante casos de baja confianza o clasificaciones ambiguas para requerir la validación o corrección por parte de un operador humano.

---

## Requisitos del Sistema y Dependencias

- **Python:** Version 3.10 o superior.
- **Gestor de Paquetes:** `uv` (Astral).
- **Modelo de Lenguaje:** Acceso a la API de OpenAI mediante API Key válida.

### Instalación

1. Clonar el repositorio localmente:
   ```bash
   git clone [https://github.com/ssofiarp-0/clasificacion-rese-as-amazon-agentes-IA.git](https://github.com/ssofiarp-0/clasificacion-rese-as-amazon-agentes-IA.git)
   cd clasificacion-rese-as-amazon-agentes-IA
