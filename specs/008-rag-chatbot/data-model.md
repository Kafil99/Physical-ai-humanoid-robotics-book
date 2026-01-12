# Data Model for Spec-4 RAG Chatbot

This document defines the data models for the API.

## API Request Model

**`ChatRequest`**
- **`question`**: `string` - The user's question.
- **`selected_text`**: `string | null` - The user-selected text from the frontend.

## API Response Model

**`ChatResponse`**
- **`answer`**: `string` - The agent's response.
