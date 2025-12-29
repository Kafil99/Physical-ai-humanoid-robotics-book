# Research & Decisions: RAG Retrieval Validation

This document outlines the key technical decisions for the `retrieve.py` validation script.

## 1. Query Process

**Decision**: The validation script will follow a simple, three-step process for each query:
1.  **Embed the Query**: Take a raw text string as input and use the Cohere client (`co.embed()`) to generate a single vector embedding. The `input_type` will be set to `"search_query"`.
2.  **Search Qdrant**: Use the `qdrant_client.search()` method to find the most similar vectors in the `rag_embedding` collection. The generated query vector will be used as the `query_vector`.
3.  **Display Results**: Print the results to the console in a readable format, including the text of the retrieved chunk, its similarity score, and its metadata payload (source URL, chunk index).

**Rationale**:
- This process directly mirrors the core logic that any future RAG agent or API would use for the retrieval step.
- It provides a clear, direct validation of the data's integrity and the relevance of the embeddings.
- The output is simple to inspect manually, which is the primary goal of this validation feature.

**Alternatives Considered**:
- **Batch Queries**: The script could accept a file of queries to run in a batch. This was rejected for V1 to maintain simplicity. The script can be run multiple times with different queries.

## 2. Validation Queries

**Decision**: The script will not have hardcoded queries. Instead, it will be designed to accept a query as a command-line argument or prompt the user for input. This provides the flexibility to test a wide range of query types as required by the success criteria.

**Rationale**:
- Hardcoding queries would make the script less reusable and harder to adapt for testing different scenarios.
- An interactive or argument-driven approach allows the AI engineer running the validation to easily test conceptual questions, keyword searches, and section-specific queries without modifying the code.
