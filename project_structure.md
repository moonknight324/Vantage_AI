# Vantage AI PersonaPilot - Project Structure

```
vantage_ai/
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── persona_manager.py      # Persona definition and management
│   │   ├── prompt_engine.py        # Dynamic prompt engineering
│   │   ├── rag_system.py           # RAG implementation
│   │   ├── output_formatter.py     # Structured output generation
│   │   └── ai_client.py            # Gemini API integration
│   ├── personas/
│   │   ├── __init__.py
│   │   ├── base_persona.py         # Base persona class
│   │   ├── college_student.py      # College student persona
│   │   ├── budget_traveler.py      # Budget traveler persona
│   │   ├── developer.py            # Developer persona
│   │   ├── startup_founder.py      # Startup founder persona
│   │   ├── sci_fi_writer.py        # Sci-fi writer persona
│   │   └── businessman.py          # Businessman persona
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── document_store.py       # Document storage and retrieval
│   │   ├── embeddings.py           # Text embedding utilities
│   │   ├── vector_db.py            # Vector database operations
│   │   └── knowledge_base.py       # Knowledge base management
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py               # Configuration management
│   │   ├── logger.py               # Logging utilities
│   │   └── helpers.py              # General helper functions
│   └── api/
│       ├── __init__.py
│       ├── routes.py               # API endpoints
│       ├── models.py               # API data models
│       └── middleware.py           # API middleware
├── data/
│   ├── personas/                   # Persona definitions and prompts
│   ├── knowledge_base/             # RAG knowledge base documents
│   ├── templates/                  # Output templates
│   └── examples/                   # Example queries and responses
├── tests/
│   ├── __init__.py
│   ├── test_personas.py
│   ├── test_rag_system.py
│   ├── test_prompt_engine.py
│   └── test_integration.py
├── docs/
│   ├── api_documentation.md
│   ├── persona_guide.md
│   └── deployment_guide.md
├── scripts/
│   ├── setup_rag.py               # RAG system setup script
│   ├── persona_builder.py         # Persona creation utility
│   └── data_loader.py             # Knowledge base loader
├── config/
│   ├── __init__.py
│   ├── settings.py                # Application settings
│   └── persona_configs.py         # Persona-specific configurations
├── .env                           # Environment variables
├── .gitignore
├── requirements.txt
├── setup.py
├── main.py                        # Application entry point
└── README.md
```

## Key Components

### Core System
- **Persona Manager**: Handles persona selection, creation, and management
- **Prompt Engine**: Dynamic prompt generation based on persona and context
- **RAG System**: Retrieval-Augmented Generation for external knowledge
- **Output Formatter**: Structured output generation (JSON, tables, etc.)

### Personas
- **Base Persona**: Abstract base class for all personas
- **Specific Personas**: College student, traveler, developer, etc.
- **Custom Personas**: User-defined persona creation

### RAG System
- **Document Store**: Manages knowledge base documents
- **Embeddings**: Text embedding and similarity search
- **Vector DB**: Vector database operations (FAISS, Pinecone, etc.)

### API Layer
- **REST API**: HTTP endpoints for persona interactions
- **WebSocket**: Real-time persona chat
- **Function Calling**: Structured action execution

