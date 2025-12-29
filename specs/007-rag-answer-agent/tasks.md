# Tasks: RAG Answer Agent

**Input**: Design documents from `specs/007-rag-answer-agent/`
**Prerequisites**: `plan.md`, `spec.md`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

---

## Phase 1: Setup

**Purpose**: Create the new agent script file and add the new dependency.

- [x] T001 Create the main agent script file at `backend/agent.py`.
- [x] T002 Add `openai` to the dependencies in `backend/pyproject.toml`.
- [x] T003 Install the new dependency into the virtual environment using `uv pip sync`.

---

## Phase 2: Foundational (Initialization)

**Purpose**: Set up the necessary clients, environment, and the core retrieval tool for the agent.

- [x] T004 [P] Add necessary imports (`os`, `cohere`, `qdrant_client`, `openai`, `dotenv`, `argparse`) to `backend/agent.py`.
- [x] T005 [P] Add functions to initialize and return Cohere, Qdrant, and OpenAI clients in `backend/agent.py`, reusing the secure loading pattern.
- [x] T006 Implement the `retrieve_book_content(query: str)` function in `backend/agent.py`. This function will encapsulate the logic from `retrieve.py` to embed a query and search Qdrant, returning a list of formatted context strings.

---

## Phase 3: User Story 1 - Grounded Question Answering (Priority: P1)

**Goal**: Implement the core agent logic for retrieving context and generating a grounded answer.
**Independent Test**: This can be tested by running the script with a query and ensuring it produces a coherent answer based on the book's content.

### Implementation for User Story 1

- [x] T007 [US1] Define the system prompt as a constant in `backend/agent.py`, instructing the agent to answer only from the provided context.
- [x] T008 [US1] In a `main()` function in `backend/agent.py`, initialize the OpenAI agent.
- [x] T009 [US1] Expose the `retrieve_book_content` function as a tool that the agent can use.
- [x] T010 [US1] Create the main agent execution loop in `main()` that takes a user query, runs the agent, and gets a response.
- [x] T011 [US1] Implement logic to check if the retrieval tool returned any content. If not, print a "cannot answer" message instead of calling the LLM.
- [x] T012 [US1] Print the final generated answer to the console.

---

## Phase 4: User Story 2 - Context Transparency (Priority: P2)

**Goal**: Add a "verbose" mode to show the retrieved context for debugging.
**Independent Test**: Can be tested by running the script with a `--verbose` flag and checking if the context is printed.

### Implementation for User Story 2

- [x] T013 [US2] Modify the `argparse` setup in `backend/agent.py` to include an optional `--verbose` flag (e.g., a boolean flag).
- [x] T014 [US2] Modify the `main()` function to check for the `--verbose` flag. If true, print the formatted context strings returned by the `retrieve_book_content` tool before printing the final answer.

---

## Phase 5: Polish & Documentation

**Purpose**: Finalize the script and update project documentation.

- [x] T015 [P] Add docstrings and type hints to all new functions in `backend/agent.py`.
- [x] T016 [P] Add logging to `agent.py` for better traceability of the agent's actions (e.g., "Retrieving context...", "Calling LLM...", "Final answer received.").
- [x] T017 Update the `backend/README.md` to include instructions on how to run the new `agent.py` script, including the `--verbose` option.
