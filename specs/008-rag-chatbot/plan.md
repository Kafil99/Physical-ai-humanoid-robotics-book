# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of a complete end-to-end RAG chatbot system. It integrates an existing Spec-3 agent (`agent.py`) with a FastAPI backend and a floating Docusaurus chatbot UI. The system will support two query modes: a global book RAG mode using Qdrant for context retrieval, and a selected-text mode that uses only user-highlighted text as context. The core agent logic will be reused without modification.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, Docusaurus, React, Pydantic, Cohere, Qdrant-client, OpenAI
**Storage**: Qdrant Cloud (for embeddings)
**Testing**: Manual testing as per the plan
**Target Platform**: Web (Docusaurus)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: p95 response latency < 3 seconds
**Constraints**: Agent logic must remain unchanged.
**Scale/Scope**: Single user, local development environment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Frontend: Docusaurus Content**
- **Clarity**: PASS
- **Consistency**: PASS
- **Accuracy**: PASS
- **Deployability**: PASS

**Backend: RAG Chatbot**    
- **API-First**: PASS
- **Grounded Responses**: PASS
- **Contextual Filtering**: PASS
- **Secure Configuration**: PASS

All gates pass.


## Project Structure

This project modifies an existing repository and does not introduce new folder structures.

- **Backend**: The FastAPI server and RAG agent logic reside in the existing `backend/` directory. All changes will be contained within `backend/main.py` and `backend/schemas.py`. The core `backend/agent.py` file will be reused without modification.

- **Frontend**: The chatbot UI will be injected into the existing Docusaurus application using the `clientModules` system. All frontend code will be located in `src/clientModules/chatbot.js` and `src/clientModules/chatbot.css`.
