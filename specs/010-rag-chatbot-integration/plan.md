# Implementation Plan: RAG Chatbot Integration

**Feature Branch**: `010-rag-chatbot-integration`
**Feature Spec**: [spec.md](spec.md)

## 1. Technical Context & Decisions

This plan outlines the technical approach for integrating a RAG-powered chatbot into the Docusaurus-based book.

-   **Backend Framework**: **FastAPI** will be used to create the API endpoint that serves the chatbot. This will be a new application within the existing `backend/` directory.
-   **Backend Agent Logic**: The implementation will reuse the existing agent from `backend/agent.py` **without any modifications**, as per the spec constraints.
-   **Frontend Framework**: The chatbot UI will be built as a **custom React component** within the Docusaurus site.
-   **Frontend Styling**: **Tailwind CSS** will be used to style the custom chatbot components to ensure a clean, attractive, and consistent look and feel.
    -   *Reference*: [research.md#decision-custom-components-with-tailwind-css](research.md#1-frontend-chatbot-ui-styling)
-   **Docusaurus Integration**: The chatbot component will be integrated globally by **swizzling the Docusaurus `Root` theme component**. This will wrap the entire site and provide a single, persistent entry point for the chatbot UI.
    -   *Reference*: [research.md#decision-theme-swizzling-to-wrap-the-root-layout](research.md#2-frontend-docusaurus-integration-strategy)
-   **Selected-Text UX**: A **floating button** will appear near the user's selected text to trigger the contextual "Ask about selection" feature.
    -   *Reference*: [research.md#decision-floating-button-on-text-selection](research.md#3-frontend-selected-text-ux-pattern)

## 2. Constitution Check & Gate Evaluation

The following project constitution principles have been reviewed and are addressed by this plan.

-   **API-First**: Yes, all functionality is exposed via a documented OpenAPI interface.
-   **Grounded Responses**: Yes, the plan ensures the agent only uses provided book content.
-   **Contextual Filtering**: Yes, the `selected_text` mode is a core part of the design.
-   **Secure Configuration**: Yes, the FastAPI backend will be configured to load secrets from environment variables.

All planning gates are passed. The specification is clear, dependencies are understood, and research has resolved all initial ambiguities.

---

## 3. Phase 0: Research (Completed)

Research has been completed to resolve initial technical unknowns. The findings and decisions are documented in [research.md](research.md).

## 4. Phase 1: Design (Completed)

The data models and API contracts have been designed based on the feature specification.

-   **Data Models**: See [data-model.md](data-model.md) for detailed definitions of the `ChatPayload`, `AgentResponse`, and frontend `ChatMessage` structures.
-   **API Contracts**: A formal OpenAPI v3 contract has been defined in [contracts/openapi.yaml](contracts/openapi.yaml).

## 5. Phase 2: Implementation Tasks

The implementation will be broken down into the following high-level tasks.

-   **Task 1: Backend (FastAPI Setup)**
    -   Create a new FastAPI application file (e.g., `backend/chatbot_api.py`).
    -   Implement the `POST /chat` endpoint.
    -   Add Pydantic models for request (`ChatPayload`) and response (`AgentResponse`) validation based on `data-model.md`.
    -   Import and call the existing agent function from `backend/agent.py`.
    -   Implement the logic to switch between `global_rag` and `selected_text` modes based on the presence of the `selected_text` field.

-   **Task 2: Frontend (Chatbot Component)**
    -   Create a new directory `src/components/Chatbot`.
    -   Build the core React components for the chatbot UI using Tailwind CSS for styling:
        -   `ChatWindow.js`: The main container.
        -   `MessageList.js`: To render the list of messages.
        -   `Message.js`: To display a single user or agent message.
        -   `ChatInput.js`: The text input and send button.
    -   Implement state management for the conversation history, input, and loading status.

-   **Task 3: Frontend (Docusaurus Integration)**
    -   Swizzle the Docusaurus `Root` component by creating `src/theme/Root.js`.
    -   In the custom `Root.js`, import and render the `Chatbot` component, wrapping the main Docusaurus content.
    -   This will make the chatbot's floating icon and UI available on all pages.

-   **Task 4: Frontend (Floating Button & Text Selection)**
    -   Implement a global event listener to detect `mouseup` events and check for text selections.
    -   Create a `FloatingActionButton` React component.
    -   When text is selected, render this button near the selected text.
    -   On button click, store the selected text in the chatbot's state to be sent with the next question.

-   **Task 5: End-to-End Integration & Testing**
    -   Connect the frontend's `ChatInput` component to the FastAPI backend, making `fetch` requests to `POST /chat`.
    -   Ensure the `question` and optional `selected_text` are correctly sent in the payload.
    -   Render the agent's response in the `MessageList`.
    -   Perform manual end-to-end testing of both the "Global RAG Mode" and the "Selected Text Mode".
    -   Verify that error handling works as expected.

## 6. Generated Artifacts

-   **Research**: `specs/010-rag-chatbot-integration/research.md`
-   **Data Models**: `specs/010-rag-chatbot-integration/data-model.md`
-   **API Contracts**: `specs/010-rag-chatbot-integration/contracts/openapi.yaml`
-   **Implementation Plan**: `specs/010-rag-chatbot-integration/plan.md`