# TF - Agentes de Investigación y Desarrollo Basados en IA

Este proyecto es un sistema de agentes de inteligencia artificial multi-propósito basados en Google ADK (Agent Development Kit) y modelos de lenguaje avanzados (Gemini, LiteLLM) para investigación, diseño de arquitecturas, implementación de código y análisis de investigación.

## 📋 Requisitos Previos

- Python 3.12 o superior
- Virtual environment (se proporciona `env/` pre-configurado)
- Acceso a las APIs de Google Gemini y APIs remotas

## 🚀 Instalación y Configuración Inicial

### 1. Activar el Entorno Virtual

```bash
source env/bin/activate
```

### 2. Variables de Entorno Requeridas

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Google API - Requerido para Gemini
GOOGLE_API_KEY=tu_clave_api_de_google

# LangSmith API - Requerido para tracking y debugging
LANGSMITH_API_KEY=tu_clave_api_de_langsmith

# Configuración Remota (Opcional - para ejecución en servidor remoto)
REMOTE_USER=nombre_usuario_remoto
REMOTE_IP=dirección_ip_remota
REMOTE_PATH=/ruta/remota/al/proyecto
REMOTE_FILE=/ruta/remota/al/archivo

# Configuración adicional
# Agrega aquí otras variables específicas del proyecto
```

### 3. Instalación de Dependencias

Las dependencias principales ya están instaladas en el virtual environment (`env/lib/python3.12/site-packages/`). Si necesitas instalar paquetes adicionales:

```bash
pip install -r requirements.txt  # Si existe
# O instala paquetes individuales:
pip install google-adk litellm langchain langgraph pydantic
```

## 📁 Estructura del Proyecto

```
TF/
├── src/
│   ├── agents/              # Agentes de IA especializados
│   │   ├── eugenio/        # Agente implementador de PyTorch
│   │   ├── walter/         # Agente redactor de papers de investigación
│   │   ├── marialuisa/     # Agente diseñador de arquitecturas
│   │   ├── debora/         # Agente debugger de código
│   │   ├── gepeto/         # Agente adicional
│   │   └── codeagent/      # Agente general de código
│   ├── tools/              # Herramientas compartidas
│   │   ├── code.py         # Utilidades de ejecución de código
│   │   ├── arxiv.py        # Búsqueda en ArXiv
│   │   ├── lang.py         # Utilidades de lenguaje
│   │   └── planner.py      # Herramientas de planificación
│   └── workflow/           # Flujos de trabajo complejos
│       └── deepresearch/   # Sistema de investigación profunda
└── README.md              # Este archivo
```

## 🤖 Agentes Disponibles

### Eugenio - Implementador de PyTorch
Especializado en generar código PyTorch production-ready basado en especificaciones técnicas.

**Características:**
- Validación de dimensiones de tensores
- Generación de código modular y type-hinted
- Soporte para GPU/CPU automático
- Estabilidad y mejores prácticas

### Walter - Redactor de Papers de Investigación
Genera papers de investigación formatizados profesionalmente a partir de blueprints técnicos.

**Características:**
- Estructura formal de papers científicos
- Inclusión de código como apéndice
- Referencias y análisis de resultados
- Publicación en venues top-tier

### María Luisa - Diseñador de Arquitecturas
Diseña arquitecturas de redes neuronales óptimas basadas en requisitos del proyecto.

**Características:**
- Análisis de requisitos
- Selección teórica de arquitecturas
- Cálculo de formas de tensores
- Generación de blueprints técnicos en JSON

### Debora - Debugger de Código
Agente especializado en encontrar y corregir errores en código Python.

**Características:**
- Análisis estático de código
- Identificación de errores lógicos
- Sugerencias de optimización

### Tocho (v1) - Asistente de Tráfico
Agente para orquestación de semáforos en intersecciones viales.

## 🏃 Uso Básico

### Ejecutar un Agente Individual

```python
from src.agents.eugenio.agent import agent as eugenio_agent

# Configurar el agente con tu consulta
response = eugenio_agent.run(
    technical_blueprint="tu_blueprint_json_aqui"
)
```

### Usar el Workflow de Investigación Profunda

```python
from src.workflow.deepresearch.graph_flow import graph

# Ejecutar búsqueda profunda
result = graph.invoke({
    "research_question": "¿Cómo optimizar modelos de deep learning?"
})
```

### Usar Herramientas

```python
from src.tools.code import send_to_env
from src.tools.arxiv import search_papers
from src.tools.planner import create_plan

# Enviar código a un entorno remoto
send_to_env(code="tu_codigo_python")

# Buscar papers en ArXiv
papers = search_papers("deep learning optimization")

# Crear un plan
plan = create_plan(objective="entrenar modelo")
```

## 🔧 Configuración Avanzada

### Usar Diferentes Modelos LLM

```python
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm

# Gemini
gemini_model = Gemini(api_key="tu_api_key")

# LiteLLM (múltiples proveedores)
litellm_model = LiteLlm(provider="openai", api_key="tu_key")
```

### Configurar LangSmith para Debugging

El proyecto utiliza LangSmith para tracing y debugging. Asegúrate de que `LANGSMITH_API_KEY` esté configurada en `.env` para ver traces detallados de agentes.

## 📝 Archivos de Configuración Clave

- `.env` - Variables de entorno (crear localmente)
- `.gitignore` - Archivos ignorados en git
- `env/` - Virtual environment con todas las dependencias

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY not found"
Verifica que `.env` esté en la raíz del proyecto con la variable `GOOGLE_API_KEY` correctamente configurada.

### Error: "Module not found"
Asegúrate de activar el virtual environment:
```bash
source env/bin/activate
```

### Error de conexión remota
Verifica que las variables `REMOTE_IP`, `REMOTE_USER` y `REMOTE_PATH` estén correctamente configuradas en `.env`.

## 📚 Referencias

- [Google ADK Documentation](https://github.com/google-cloud/google-cloud-python)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

## 📄 Licencia

Proyecto de investigación - Tópicos en Ciencias de la Computación

## ✉️ Soporte

Para preguntas o issues, contacta al equipo de desarrollo del proyecto.
