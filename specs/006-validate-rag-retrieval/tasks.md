# Tasks: RAG Retrieval Validation

**Input**: Design documents from `specs/006-validate-rag-retrieval/`
**Prerequisites**: `plan.md`, `spec.md`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

---

## Phase 1: Setup

**Purpose**: Create the new validation script file.

- [x] T001 Create the main validation script file at `backend/retrieve.py`.

---

## Phase 2: Foundational (Initialization)

**Purpose**: Set up the necessary clients and environment for the script to run.

- [x] T002 [P] Add necessary imports (`os`, `cohere`, `qdrant_client`, `dotenv`, `argparse`) to `backend/retrieve.py`.
- [x] T003 [P] Add functions to initialize and return Cohere and Qdrant clients in `backend/retrieve.py`, reusing the secure loading pattern from `main.py`.

---

## Phase 3: User Story 1 - Semantic Search Validation (Priority: P1)

**Goal**: Implement the core logic for embedding a query and searching the vector database.
**Independent Test**: This phase can be tested by calling the search function with a test query and printing the raw results to see if points are returned.

### Implementation for User Story 1

- [x] T004 [US1] Implement a `search_qdrant(query: str, co_client, qd_client, collection_name: str, top_k: int)` function in `backend/retrieve.py`.
- [x] T005 [US1] Inside `search_qdrant`, implement the logic to take the text query, generate its embedding using Cohere (`input_type='search_query'`).
- [x] T006 [US1] Inside `search_qdrant`, implement the logic to use the generated query vector to search the Qdrant collection.

---

## Phase 4: User Story 2 - Metadata and Integrity Verification (Priority: P2)

**Goal**: Format and display the search results in a human-readable way for manual validation.
**Independent Test**: This phase can be tested by feeding it mock `ScoredPoint` objects and verifying the console output is clear and well-formatted.

### Implementation for User Story 2

- [x] T007 [US2] Implement a `display_results(results: list)` function in `backend/retrieve.py`.
- [x] T008 [US2] Inside `display_results`, add logic to loop through the search results and print the similarity score, source URL, chunk index, and text for each result.
- [x] T009 [US2] Add headers and separators in the `display_results` output to make the results easy to read.

---

## Phase 5: Integration & Orchestration

**Purpose**: Create the main execution block to make the script runnable from the command line.

- [x] T010 Implement a `main()` function in `backend/retrieve.py` that orchestrates the client initializations and function calls.
- [x] T011 [P] Use Python's `argparse` module within `main()` to accept a user's query from the command line (e.g., `python retrieve.py "my search query"`).
- [x] T012 Add a `if __name__ == "__main__":` block to call the `main()` function.

---

## Phase 6: Polish & Documentation

**Purpose**: Finalize the script and update project documentation.

- [x] T013 [P] Add docstrings and type hints to all new functions in `backend/retrieve.py`.
- [x] T014 [P] Add logging to `retrieve.py` to show progress (e.g., "Embedding query...", "Searching collection...", "Displaying results...").
- [x] T015 Update the `backend/README.md` to include instructions on how to run the new `retrieve.py` validation script.
