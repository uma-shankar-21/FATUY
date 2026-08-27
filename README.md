# Banking AI Assistant
FATUY(Financial Assistant That Understands You)

An AI-powered banking assistant built with FastAPI, React, PostgreSQL, Redis, Kafka, pgvector, and Large Language Models.

The system is designed around a memory-aware AI architecture that combines short-term conversation context, long-term user memory, banking data, semantic retrieval, asynchronous event processing, and real-time data access.

---

## Features

- AI-powered banking assistant
- Multi-turn conversations with short-term memory
- Redis-based session storage with sliding expiration
- Automatic session expiration after 30 minutes of inactivity
- Expired conversation persistence using PostgreSQL JSONB
- Kafka-based asynchronous memory processing
- Long-term memory generation using LLM summarization
- Persistent user memory storage
- Semantic retrieval using pgvector
- Context selection for relevant long-term memories
- Banking-aware context generation
- Transaction, account, loan, and loan payment data access
- REST APIs using FastAPI
- PostgreSQL with pgvector
- Redis for short-term session memory
- Kafka for asynchronous event processing
- LLM provider abstraction
- Groq LLM integration
- Model Context Protocol (MCP) integration for real-time data access
- Context-aware mega-prompt generation
- Prompt validation and iterative refinement
- Docker-based development environment

---

# Architecture

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
