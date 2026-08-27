# Banking AI Assistant

An AI-powered banking assistant built with a distributed, event-driven architecture using Python, FastAPI, PostgreSQL, Redis, Kafka, pgvector, LLMs, and MCP.

The system provides contextual banking assistance by combining:

- Short-term conversational memory
- Long-term AI-generated memory
- Semantic memory retrieval
- Real-time banking data
- Event-driven background processing
- Context-aware prompt construction
- LLM validation and fallback mechanisms

The project is designed to demonstrate a practical architecture for building production-oriented AI applications rather than a simple chatbot.

---

## Architecture Overview

```text
                           ┌─────────────────────┐
                           │      React UI       │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │    FastAPI API      │
                           └──────────┬──────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
        ┌────────────────┐   ┌────────────────┐   ┌────────────────┐
        │ Redis          │   │ PostgreSQL     │   │ Banking APIs   │
        │ Short-Term     │   │ Long-Term      │   │ / MCP Tools    │
        │ Memory         │   │ Memory         │   │ Real-Time Data │
        └───────┬────────┘   └───────┬────────┘   └────────┬───────┘
                │                    │                     │
                │                    ▼                     │
                │             ┌───────────────┐             │
                │             │ pgvector      │             │
                │             │ Semantic      │             │
                │             │ Retrieval     │             │
                │             └───────┬───────┘             │
                │                     │                     │
                └─────────────────────┼─────────────────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │ Context Selection   │
                           │ & Prompt Builder    │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │     LLM Provider    │
                           │   Groq / Llama      │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │    AI Response      │
                           └─────────────────────┘