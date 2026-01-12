# Task List: RAG Chatbot (FastAPI + Docusaurus)

This document outlines the implementation tasks for integrating the RAG chatbot.

## User Stories

- **US1**: As a user, I can ask a question in the chatbot and receive an answer generated from the entire book's content.
- **US2**: As a user, I can select text on the page, ask a question, and receive an answer generated *only* from that selected text.

## Phase 1: Foundational Setup

These tasks prepare the environment and shared components.

- [X] T001 Install or update backend dependencies in `backend/requirements.txt`
- [X] T002 Create the Pydantic schemas in `backend/schemas.py`
- [X] T003 [P] Create the basic chatbot stylesheet in `src/clientModules/chatbot.css`

## Phase 2: User Story 1 - Global Book RAG

**Goal**: Implement the default chat mode where the agent answers questions based on the entire book.
**Test Criteria**: User can send a message and receive a response from the backend agent.

- [X] T004 [US1] Create the initial FastAPI application in `backend/main.py`
- [X] T005 [US1] Implement the `/chat` endpoint in `backend/main.py`
- [X] T006 [US1] Add the Global Book RAG logic to the `/chat` endpoint in `backend/main.py`
- [X] T007 [P] [US1] Create the basic chatbot UI component in `src/clientModules/chatbot.js`
- [X] T008 [US1] Implement the message sending and display logic in `src/clientModules/chatbot.js`

## Phase 3: User Story 2 - Selected Text RAG

**Goal**: Implement the strict context mode where the agent answers questions based only on user-selected text.
**Test Criteria**: When text is selected, the agent's response is limited to that context.

- [X] T009 [P] [US2] Add logic to detect and store selected text in `src/clientModules/chatbot.js`
- [X] T010 [US2] Modify the frontend request to include `selected_text` in `src/clientModules/chatbot.js`
- [X] T011 [US2] Add the Selected Text Mode routing logic to the `/chat` endpoint in `backend/main.py`

## Phase 4: Polish & Finalization

These tasks cover final cleanup and documentation.

- [X] T012 [P] Review and remove any console logs or debug statements
- [X] T013 Create/update a `README.md` with instructions on how to run the backend and frontend

## Dependencies

- **US2** depends on **US1**. The basic chat functionality must be working before the selected text feature can be added.

## Parallel Execution

- Within each user story, frontend (`.js`/`.css`) and backend (`.py`) tasks can often be worked on in parallel. For example, T006 and T008 can be implemented concurrently.

## Implementation Strategy

The implementation will follow an MVP-first approach.
1.  First, implement US1 to get the core chatbot functionality working.
2.  Then, incrementally add the US2 feature for selected text.
3.  Finally, complete the polish tasks.
