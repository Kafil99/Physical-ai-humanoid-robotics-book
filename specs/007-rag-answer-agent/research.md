# Research & Decisions: RAG Answer Agent

This document outlines the key architectural decisions for the `agent.py` script.

## 1. Agent Architecture: Retrieval as a Tool

**Decision**: The core retrieval logic will be encapsulated in a dedicated function (e.g., `retrieve_book_content(query: str)`). This function will then be exposed to the OpenAI Agent as a "tool" that it can choose to call.

**Rationale**:
- **Modularity and Reusability**: Treating retrieval as a distinct tool separates the "getting" of information from the "reasoning" about it. This makes the retrieval logic easier to test and maintain independently.
- **Standard Agentic Pattern**: This is the standard and recommended architecture for building agents that need to interact with external data sources. The agent's primary responsibility becomes learning *when* to call the tool and *what* to pass to it.
- **Inspectability**: It is easy to log the inputs and outputs of the tool, providing clear visibility into what context the agent is using to form its answers.

**Alternatives Considered**:
- **Monolithic Function**: A single, large function that handles retrieval, prompt construction, and the LLM call. This was rejected as it creates tightly coupled code that is difficult to debug and maintain.

## 2. Grounding the Agent's Response

**Decision**: The agent's behavior will be strictly controlled via a system prompt. This prompt will contain explicit instructions for the agent to:
1.  Always use the `retrieve_book_content` tool to answer user queries.
2.  Base its final answer *exclusively* on the information returned by the tool.
3.  If the tool returns no relevant information, the agent MUST decline to answer and inform the user that it doesn't have enough information.
4.  NEVER use its own internal knowledge.

**Rationale**:
- **Reliability**: A strong system prompt is the most effective way to prevent the LLM from "hallucinating" or using outside knowledge, thus ensuring the "Grounded Responses" principle is met.
- **Clarity of Purpose**: It makes the agent's purpose and limitations explicit, leading to more predictable behavior.

**Alternatives Considered**:
- **No System Prompt**: Relying on the agent's default behavior. This was rejected as it would lead to unpredictable and non-grounded answers.
- **Complex Guard-railing**: Building complex post-processing logic to check if the answer is grounded. This is much more difficult than simply controlling the agent's behavior with a clear upfront instruction.
