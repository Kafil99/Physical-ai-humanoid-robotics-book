# Feature Specification: Integrate RAG Agent with Frontend Chatbot

**Feature Branch**: `010-rag-chatbot-integration`
**Created**: 2025-12-29
**Status**: Draft
**Input**: User description: "Integrate the RAG agent with an attractive frontend chatbot using FastAPI to enable end-to-end question answering over book content, including answering questions based only on user-selected text IMPORTANT IMPLEMENTATION CONSTRAINT: The Spec-3 agent has already been manually corrected to use the official OpenAI Agents SDK. This implementation must be reused as-is. Do NOT regenerate, refactor, or replace the agent core. --- # 🎯 Target Audience - Full-stack engineers integrating AI agents into web applications - Evaluators validating a complete, user-facing RAG system --- ## 🔍 Focus - Wrapping the standalone RAG agent (Spec-3) with a FastAPI backend - Building a web-based chatbot frontend with an interactive UI - Adding a floating chatbot icon that toggles the chat interface - Enabling user queries to flow from frontend → FastAPI → agent → Qdrant → response - Allowing users to ask questions based on text they explicitly select in the book - Completing the full RAG loop for the published book --- ## 🧠 Supported Query Modes (NEW) The system must support **two distinct query modes**: ### 1️⃣ Global Book RAG Mode (default) - User submits a question **without selecting any text** - FastAPI invokes the existing **Spec-3 agent** - Agent retrieves relevant chunks from **Qdrant** - Answer is generated **strictly from retrieved content** ### 2️⃣ Selected Text Mode (NEW) - User selects a portion of book text in the frontend - Frontend sends the following to FastAPI: - `question` - `selected_text` - FastAPI **bypasses Qdrant retrieval** - The selected text is injected directly as the **only allowed context** - Agent answers **strictly and exclusively** from the selected text - If the answer is not present in the selected text, the agent must respond: > “I don’t know based on the selected text.” --- ## 🧩 Backend Responsibilities (FastAPI) - Expose a chatbot endpoint (e.g. `/chat`) - Accept payloads containing: - `question` - optional `selected_text` - Determine execution mode: - If `selected_text` is present → **Selected Text Mode** - Otherwise → **Global Book RAG Mode** - Invoke the existing agent logic from `agent.py` - **Do NOT modify** the core agent implementation - Return agent responses to the frontend --- ## 🖥️ Frontend Responsibilities - Render a floating chatbot icon - Toggle chatbot open/close on click - Display user messages and agent responses distinctly - Allow users to: - Ask general questions about the book - Select text from the book and ask context-specific questions - When text is selected: - Capture the selected content - Send it along with the user question to FastAPI --- ## ✅ Success Criteria - A FastAPI backend exposes an endpoint for chatbot queries - A floating chatbot icon is visible on the frontend - Clicking the icon opens and closes the chatbot interface - The chatbot UI is visually clean and user-friendly - User messages and agent responses are clearly distinguishable - The frontend sends user queries to the FastAPI backend - FastAPI invokes the existing agent logic from `agent.py` **without modification** - The agent retrieves relevant context from Qdrant in global mode - The agent answers strictly from user-selected text in selected-text mode - Responses are rendered correctly in the frontend - Users can ask multiple questions sequentially without errors - The system works end-to-end in a local development environment --- ## ⚙️ Constraints - Agent logic must remain unchanged (reuse Spec-3 implementation) - Backend framework: **FastAPI** - Frontend: web-based chatbot (HTML/JS or Docusaurus React component) - Chatbot UI must be lightweight and responsive - Communication must be local (development setup) - No re-embedding or re-ingestion of data - Responses must remain strictly grounded in provided context - Minimal additional infrastructure --- ## 🚫 Not Building - Authentication or authorization - Production deployment or scaling - Streaming responses - Long-term chat history persistence - Analytics or monitoring dashboards"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Global Question Answering (Priority: P1)

As a reader, I want to ask a general question about the book in a chatbot and get an answer based on the entire content.

**Why this priority**: This is the primary use case for the RAG agent and provides the core value to the user.

**Independent Test**: Can be fully tested by opening the chatbot, asking a question, and verifying that the answer is relevant and derived from the book's content.

**Acceptance Scenarios**:

1.  **Given** the chatbot interface is open, **When** I type "What is ROS2?" and submit, **Then** I receive an answer explaining the basics of ROS2 based on the book's content.
2.  **Given** the chatbot is open, **When** I ask a question not covered in the book, **Then** the agent responds that it does not have the information.

---

### User Story 2 - Selected Text Question Answering (Priority: P2)

As a reader, I want to highlight a specific paragraph or section of the book, ask a question about that selection, and get an answer derived *only* from the text I selected.

**Why this priority**: This provides a powerful, focused-context Q&A experience, allowing users to drill down into specific details.

**Independent Test**: Can be tested by selecting text on a page, asking a question related to that text, and verifying the answer is based *only* on the selection.

**Acceptance Scenarios**:

1.  **Given** I have selected a paragraph about URDF files, **When** I ask the chatbot "What is a URDF?", **Then** I receive an answer generated exclusively from the selected paragraph.
2.  **Given** I have selected a paragraph about URDF files, **When** I ask a question whose answer is not in that paragraph (e.g., "What is Gazebo?"), **Then** the agent responds: “I don’t know based on the selected text.”

---

### User Story 3 - Chatbot UI Interaction (Priority: P1)

As a user, I want to see a floating chatbot icon on the website that I can easily click to open and close the chat window.

**Why this priority**: This provides the entry point for all chatbot functionality and is essential for user interaction.

**Independent Test**: Can be tested by navigating to any page of the book and interacting with the floating icon.

**Acceptance Scenarios**:

1.  **Given** I am on any page of the book, **Then** a floating chatbot icon is visible.
2.  **Given** the chatbot is closed, **When** I click the floating icon, **Then** the chatbot interface opens.
3.  **Given** the chatbot is open, **When** I click the floating icon (or a close button), **Then** the chatbot interface closes.

---

### Edge Cases

-   What happens when a user selects a very large block of text? Is there a character limit?
-   How does the system handle a question submitted while another is already being processed?
-   What is displayed in the chat window before the first question is asked?
-   How does the system handle non-text selections (e.g., images, code blocks)?

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST render a floating chatbot icon on all pages of the Docusaurus site.
-   **FR-002**: The system MUST open and close a chatbot interface when the user interacts with the icon.
-   **FR-003**: The chatbot interface MUST display a conversation history, distinguishing between user messages and agent responses.
-   **FR-004**: The system MUST provide an input field for users to type questions.
-   **FR-005**: The frontend MUST detect when a user has selected text on the page and capture that text when a question is submitted.
-   **FR-006**: The frontend MUST send a request to a FastAPI backend endpoint (`/chat`) with the user's `question` and an optional `selected_text`.
-   **FR-007**: The FastAPI backend MUST determine the query mode based on the presence of `selected_text` in the request.
-   **FR-008**: In **Global Book RAG Mode** (no `selected_text`), the backend MUST invoke the existing `agent.py` logic, which will retrieve context from Qdrant.
-   **FR-009**: In **Selected Text Mode**, the backend MUST invoke the agent logic, providing the `selected_text` as the sole context, bypassing Qdrant retrieval.
-   **FR-010**: The agent MUST answer questions strictly from the provided context (either from Qdrant or `selected_text`).
-   **FR-011**: If the answer cannot be found in the provided `selected_text`, the agent MUST respond with the exact message: “I don’t know based on the selected text.”
-   **FR-012**: The agent's core implementation in `agent.py` (Spec-3) MUST NOT be modified.

### Key Entities

-   **Chat Message**: Represents a single entry in the conversation.
    -   `id`: Unique identifier
    -   `sender`: "user" or "agent"
    -   `content`: The text of the message
    -   `timestamp`: Time the message was created
-   **Chat Payload**: The data sent from the frontend to the backend.
    -   `question`: The user's query (string, mandatory)
    -   `selected_text`: The user's highlighted text (string, optional)

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: A user can receive an answer to a global question within 5 seconds of submission in a local development environment.
-   **SC-002**: A user can receive an answer to a question on selected text within 3 seconds of submission.
-   **SC-003**: 100% of agent responses in "Selected Text Mode" are generated exclusively from the provided text.
-   **SC-004**: The floating chatbot icon is present on 100% of the book's pages.
-   **SC-005**: The end-to-end flow (frontend -> backend -> agent -> response -> frontend) functions successfully for both query modes in a local development environment.
-   **SC-006**: The chatbot UI is rated as "intuitive" or "easy to use" by at least 80% of internal testers.

## Out of Scope *(mandatory)*

-   User authentication or authorization.
-   Production deployment, hosting, or scaling considerations.
-   Streaming (real-time "typing") responses from the agent.
-   Persistence of chat history between sessions or across devices.
-   Analytics, monitoring, or logging dashboards.
