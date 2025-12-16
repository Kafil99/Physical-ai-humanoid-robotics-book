# Research and Decisions

This document records the key architectural and technical decisions for the project.

## Docusaurus Version

- **Decision**: Use Docusaurus 3.x.
- **Rationale**: Docusaurus 3.x is the latest stable version, offering the best performance, features, and security. It uses React 18 and MDX v3, which are modern and well-supported technologies.
- **Alternatives considered**:
  - Docusaurus 2.x: Older version, not recommended for new projects.

## Content Format

- **Decision**: Use MDX (`.mdx`) for all content files.
- **Rationale**: MDX allows embedding React components directly in Markdown, which will be useful for creating interactive examples, quizzes, and other dynamic content. This provides more flexibility than plain Markdown.
- **Alternatives considered**:
  - Plain Markdown (`.md`): Simpler, but less powerful. We can start with `.md` and rename to `.mdx` as needed, but starting with `.mdx` is more future-proof.

## Diagram Tool

- **Decision**: Use Mermaid for diagrams.
- **Rationale**: Mermaid is a text-based diagramming tool that is easy to version control and integrates well with Docusaurus. It allows for creating a variety of diagrams (flowcharts, sequence diagrams, etc.) directly in Markdown.
- **Alternatives considered**:
  - Static images (e.g., PNG, SVG): Harder to maintain and version control.
  - Interactive diagram tools (e.g., Excalidraw): Can be embedded, but adds an external dependency and may not be as accessible.

## Search Implementation

- **Decision**: Use the default Docusaurus local search plugin for the initial phase.
- **Rationale**: The local search plugin is easy to set up and works well for small to medium-sized sites. It does not require any external service or API keys. We can upgrade to Algolia later if needed.
- **Alternatives considered**:
  - Algolia DocSearch: More powerful search, but requires an application process and external configuration. Overkill for the initial version.

## Code Examples Approach

- **Decision**: Use inline code blocks with language highlighting.
- **Rationale**: Docusaurus has excellent support for code blocks with syntax highlighting. This is the simplest and most common approach for displaying code examples.
- **Alternatives considered**:
  - Embeds (e.g., from GitHub Gists or other services): Adds external dependencies and can slow down page load times.

## ROS 2 Distribution

- **Decision**: Use ROS 2 Humble Hawksbill.
- **Rationale**: ROS 2 Humble is the current long-term support (LTS) release, which is the most stable and well-supported version. This is crucial for a book with code examples that need to be reliable.
- **Alternatives considered**:
  - ROS 2 Iron Irwini: The latest release, but not an LTS. It may have newer features but also more potential for breaking changes.

## Book Versioning

- **Decision**: No versioning for the initial release.
- **Rationale**: The book will be a single, living document initially. Docusaurus versioning adds complexity that is not needed for the first iteration. We can add versioning later if we decide to create a second edition of the book.
- **Alternatives considered**:
  - Docusaurus versioning: Useful for managing multiple versions of documentation, but overkill for a single book.

## Target OS

- **Decision**: Officially support Ubuntu 22.04 LTS only.
- **Rationale**: ROS 2 Humble and many of the other tools are primarily developed and tested on Ubuntu. Focusing on a single OS will ensure the quality and reliability of the code examples.
- **Alternatives considered**:
  - Multi-platform support (Windows, macOS): Would significantly increase the complexity of testing and maintaining the code examples.
