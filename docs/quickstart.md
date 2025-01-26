# docs/quickstart.md
# Quick Start Guide

## Installation

```bash
pip install gracie-framework
```

## Basic Usage

```python
from gracie import Agent, Topic

# Create agent
agent = Agent("MyAgent")

# Add knowledge
agent.add_knowledge([
    Topic(
        name="example",
        definition="Example topic",
        facts=["Fact 1", "Fact 2"]
    )
])

# Use agent
response = agent.process_input("Hello!")
print(response)
```

## Configuration

The Gracie Framework can be configured through the `KnowledgeConfig` class:

```python
from gracie import KnowledgeConfig

config = KnowledgeConfig(
    embedding_model="all-MiniLM-L6-v2",  # Choose embedding model
    enable_faiss=True,                    # Enable FAISS for faster search
    max_contexts=5,                       # Maximum contexts to retrieve
    confidence_threshold=0.7              # Minimum confidence threshold
)
```

# docs/architecture.md
# Architecture Overview

## Core Components

1. Knowledge System
   - Central knowledge management
   - RAG (Retrieval-Augmented Generation)
   - Memory management

2. Embedding System
   - Text embeddings generation
   - Similarity search
   - FAISS integration

3. Database Management
   - Topic storage
   - Interaction history
   - Performance metrics

4. Agent Interface
   - Input processing
   - Response generation
   - Personality traits

## Memory Management

The framework uses a sophisticated memory system:

1. Short-term Memory
   - Recent interactions
   - Context window
   - Temporary storage

2. Long-term Memory
   - Persistent knowledge
   - Vector database
   - Learned patterns

# docs/examples.md
# Example Implementations

## Basic Agent

```python
from gracie import Agent
agent = Agent("BasicAgent")
```

## Crypto Bot

```python
from gracie import Agent, KnowledgeConfig

config = KnowledgeConfig(
    enable_faiss=True,
    max_contexts=10
)

agent = Agent(
    name="CryptoBot",
    knowledge_config=config,
    personality_traits=[
        {"name": "analytical", "strength": 0.8}
    ]
)
```

## Custom Knowledge Integration

```python
from gracie import Topic

agent.add_knowledge([
    Topic(
        name="custom_topic",
        definition="Custom knowledge",
        facts=["Custom fact 1", "Custom fact 2"]
    )
])
```
