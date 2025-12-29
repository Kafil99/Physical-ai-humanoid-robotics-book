<!--
    Sync Impact Report
    - Version change: 1.0.0 -> 1.1.0
    - Rationale: MINOR bump for addition of new Backend principles.
    - Added sections: Governance, Frontend: Docusaurus Content, Backend: RAG Chatbot
    - Removed sections: None (previous content was unstructured and has been organized into the 'Frontend' section).
    - Templates requiring updates:
        - .specify/templates/plan-template.md (PENDING CHECK)
        - .specify/templates/spec-template.md (PENDING CHECK)
        - .specify/templates/tasks-template.md (PENDING CHECK)
    - Follow-up TODOs:
        - TODO(RATIFICATION_DATE): Determine original adoption date of the constitution.
-->

# Project Constitution: physical-ai-robotics-books

## 1. Governance

- **Constitution Version**: `1.1.0`
- **Ratification Date**: `TODO(RATIFICATION_DATE): Determine original adoption date`
- **Last Amended**: `2025-12-17`

### Amendment Process

Amendments to this constitution require a pull request that is reviewed and approved by the project owner. The PR must include updates to the version number and a summary of changes in the Sync Impact Report.

### Versioning

This constitution follows semantic versioning:
- **MAJOR**: Backward-incompatible changes, such as removing a core principle.
- **MINOR**: Adding new principles or sections that expand governance.
- **PATCH**: Minor clarifications, typo fixes, or rephrasing.

## 2. Frontend: Docusaurus Content

### Core Principles

- **Clarity**: All content must be clear and easily understandable for technical readers, including developers and students.
- **Consistency**: The structure, formatting, and writing style must be consistent across all chapters and modules.
- **Accuracy**: All code examples, technical explanations, and hardware requirements must be accurate and tested.
- **Deployability**: The entire Docusaurus site must build without errors and be deployable to GitHub Pages.

### Key Standards

- **Writing Style**: The tone should be clear, conversational, and friendly, suitable for a tutorial format.
- **Code Blocks**: All code examples must be tested and fully functional. They should be copy-paste ready.
- **Format**: All content will be written in Docusaurus-compatible Markdown (.mdx).
- **Headings**: Headings must follow a logical hierarchy (H1 > H2 > H3) to ensure readability and proper document structure.
- **Links**: Internal navigation must use relative paths.

### Constraints

- **Platform**: The project will be built using Docusaurus and deployed as a static site to GitHub Pages.
- **Tools**: Development will use Spec-Kit Plus for specifications and the Gemini CLI for content generation and automation.
- **File Structure**: The project will adhere to the standard Docusaurus conventions for `docs`, `static`, and other directories.
- **Images**: All images must be optimized for the web and stored in the `/static/img` folder.

### Success Criteria

- The Docusaurus site builds without any errors.
- All internal and external links work correctly.
- Navigation, including the sidebar and previous/next buttons, is fully functional.
- All code examples are accurate and can be run successfully on the target platform.
- The final site is successfully deployed and accessible via GitHub Pages.

## 3. Backend: RAG Chatbot

### Tech Stack

- FastAPI (Python 3.11+)
- OpenAI Agents SDK / ChatKit SDK
- Cohere (Reranking & Embeddings)
- Qdrant Cloud (Free Tier)
- Neon Serverless Postgres

### Core Principles

- **API-First**: All backend functionality MUST be exposed via a well-documented OpenAPI interface.
- **Grounded Responses**: The RAG chatbot MUST only generate responses based on the provided book content and not use external knowledge.
- **Contextual Filtering**: The API MUST support filtering retrieval context based on user-selected text from the frontend.
- **Secure Configuration**: All secrets, API keys, and environment-specific configurations MUST be loaded from environment variables and never hardcoded.

### Key Standards

- **Static Typing**: All Python functions MUST include type hints for parameters and return values.
- **Data Validation**: Pydantic models MUST be used for all API request/response bodies and for internal data validation.
- **Error Handling**: The API MUST return consistent, structured JSON error responses for all failed requests.

### RAG Pipeline

- **Embeddings**: Use Cohere `embed-english-v3.0` for generating text embeddings.
- **Reranking**: Use Cohere `rerank-v3.5` to improve the relevance of retrieved chunks before synthesis.
- **LLM**: Use OpenAI `gpt-4o-mini` for generating the final chat response.

### API Endpoints

- `POST /api/chat`: Main chat endpoint for general queries.
- `POST /api/chat/selected`: Chat endpoint that accepts selected text from the frontend to narrow the retrieval context.
- `GET /api/health`: A simple health check endpoint that confirms service availability.

### Constraints

- **Chunking**: Text should be chunked with a size of 500-1000 tokens and an overlap of 100 tokens.
- **Retrieval**: Retrieve the top 10 most similar chunks (Top-K=10), then rerank to select the top 3-5 for the final context.
- **Performance**: P95 response latency for the `/api/chat` endpoint MUST be under 3 seconds.
- **Rate Limiting**: Implement a rate limit of 10 requests per minute per IP address.

### Success Criteria

- **Factual Grounding**: All chatbot responses are verifiably sourced from the Docusaurus book content.
- **Relevance**: The Cohere reranker demonstrably improves the relevance of answers compared to a baseline without reranking.
- **Feature Completeness**: The selected-text context filtering feature is fully functional and correctly influences responses.
- **Integration**: The backend API integrates successfully with the Docusaurus frontend.
- **Security**: No secrets or keys are exposed in the codebase or in deployment artifacts.
