# Tasks: RAG Content Pipeline

**Input**: Design documents from `specs/005-rag-content-pipeline/`
**Prerequisites**: `plan.md`, `spec.md`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)

---

## Phase 1: Setup

**Purpose**: Initialize the backend project structure and configuration.

- [x] T001 Create the main project directory at `backend/`.
- [x] T002 [P] Create an empty file for environment variables at `backend/.env`.
- [x] T003 [P] Create a placeholder README file at `backend/README.md`.
- [x] T004 Create a `pyproject.toml` file in `backend/` to initialize the `uv` project.
- [x] T005 Create the main application file at `backend/main.py`.

---

## Phase 2: Foundational (Dependencies)

**Purpose**: Configure and install all necessary third-party libraries.

- [x] T006 Add project dependencies (`requests`, `beautifulsoup4`, `cohere`, `qdrant-client`, `python-dotenv`) to `backend/pyproject.toml`.
- [x] T007 Create a virtual environment and install the dependencies using `uv pip install -r requirements.txt` or `uv pip sync` after generating the requirements file.

---

## Phase 3: User Story 1 - Content Ingestion and Processing (Priority: P1)

**Goal**: Implement the logic to discover, fetch, and process text content from the Docusaurus site.
**Independent Test**: The functions in this phase can be tested by running them and verifying that they output a list of clean text chunks from the target URL.

### Implementation for User Story 1

- [x] T008 [US1] Implement the `get_all_urls()` function in `backend/main.py` to parse the `sitemap.xml` and return a list of all page URLs.
- [x] T009 [US1] Implement the `extract_text_from_url(url: str)` function in `backend/main.py` to download HTML from a URL and extract clean text from the `<article>` tag.
- [x] T010 [US1] Implement the `chunk_text(text: str)` function in `backend/main.py` to split a given text into fixed-size chunks with overlap.

---

## Phase 4: User Story 2 - Embedding Generation and Storage (Priority: P2)

**Goal**: Implement the logic to generate embeddings for the text chunks and store them in Qdrant.
**Independent Test**: The functions in this phase can be tested by providing them with sample text chunks and verifying that the corresponding vectors are created and stored in the Qdrant collection.

### Implementation for User Story 2

- [x] T011 [US2] Implement the `embed(chunks: list[str])` function in `backend/main.py` to take a list of text chunks and generate embeddings for them using the Cohere API.
- [x] T012 [P] [US2] Implement the `create_collection(collection_name: str)` function in `backend/main.py` to set up the `rag_embedding` collection in Qdrant, ensuring it's recreated on each run.
- [x] T013 [US2] Implement the `save_chunk_to_qdrant(chunks_with_embeddings: list)` function in `backend/main.py` to upload the chunks, their embeddings, and metadata to the Qdrant collection.

---

## Phase 5: Integration & Orchestration

**Purpose**: Combine all the implemented functions into a single, executable pipeline.

- [x] T014 Implement the `main()` function in `backend/main.py` to orchestrate the end-to-end pipeline: call `get_all_urls`, process each URL to get chunks, embed the chunks, and save them to Qdrant.
- [x] T015 Add environment variable loading using `dotenv` at the start of `backend/main.py` to securely access API keys.

---

## Phase 6: Polish & Documentation

**Purpose**: Finalize the script with error handling, logging, and clear documentation.

- [x] T016 [P] Add robust error handling (e.g., for network issues, API failures) to all functions in `backend/main.py`.
- [x] T017 [P] Add logging throughout `backend/main.py` to provide visibility into the ingestion progress and any potential issues.
- [x] T018 Update the `backend/README.md` with detailed instructions on how to set up the `.env` file, install dependencies with `uv`, and run the `main.py` script.

---

## Dependencies & Execution Order

- **Phase 1 & 2** must be completed first.
- **Phase 3 (US1)** can be implemented and tested independently.
- **Phase 4 (US2)** can be implemented and tested independently, using mock data from US1.
- **Phase 5** depends on the completion of both Phase 3 and Phase 4.
- **Phase 6** can be worked on in parallel with other phases but should be finalized last.
