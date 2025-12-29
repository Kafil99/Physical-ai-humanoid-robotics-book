---
id: 002
title: Add Backend RAG Constitution
stage: constitution
date: 2025-12-17
surface: agent
model: gemini-pro
feature: none
branch: main
user: (unknown)
command: /sp.constitution Add the following backend section to my existing sp.constitution without modifying any frontend requirements...
labels: ["constitution", "backend", "rag"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 (none)
---

## Prompt

/sp.constitution

Add the following backend section to my existing sp.constitution without modifying any frontend requirements:

## Backend: RAG Chatbot

Tech Stack:
- FastAPI (Python 3.11+)
- OpenAI Agents SDK / ChatKit SDK
- Cohere (Reranking & Embeddings)
- Qdrant Cloud (Free Tier)
- Neon Serverless Postgres

Core Principles:
- API-First with OpenAPI documentation
- RAG responses grounded only in book content
- Support user-selected text as context filter
- All secrets via environment variables

Key Standards:
- Type hints on all functions
- Pydantic models for validation
- Consistent JSON error responses

RAG Pipeline:
- Embeddings: Cohere embed-english-v3.0
- Reranking: Cohere rerank-v3.5 for improved relevance
- LLM: OpenAI GPT-4o-mini for response generation

API Endpoints:
- POST /api/chat - Main chat
- POST /api/chat/selected - Chat with selected text context
- GET /api/health - Health check

Constraints:
- Chunk size: 500-1000 tokens, 100 overlap
- Top-K retrieval: 10 chunks → Rerank → Top 3-5
- Response latency: < 3 seconds
- Rate limiting: 10 req/min per IP

Success Criteria:
- Responses cite only book content
- Cohere reranking improves answer relevance
- Selected text feature works correctly
- Integrates with Docusaurus frontend
- Zero exposed secrets

## Response snapshot

The agent updated the project constitution at `.specify/memory/constitution.md`.
- Bumped version to `1.1.0`.
- Added a `Governance` section.
- Organized existing frontend principles under a `Frontend` section.
- Added the new `Backend: RAG Chatbot` section as requested.
- Checked dependent templates for consistency and found no changes were needed.

## Outcome

- ✅ Impact: The constitution was successfully updated with the new backend principles and a proper governance structure.
- 🧪 Tests: No tests were run.
- 📁 Files: 1 file modified.
- 🔁 Next prompts: N/A
- 🧠 Reflection: The process of updating the constitution and checking dependent templates was successful. The templates are generic enough to not require changes.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
