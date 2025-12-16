# Data Model

This document describes the main data entities for the project.

## Book

The top-level entity representing the entire book.

- **Attributes**:
  - `title`: The title of the book.
  - `tagline`: The tagline of the book.
  - `modules`: A collection of Modules.

## Module

A collection of related chapters, representing a major section of the book.

- **Attributes**:
  - `title`: The title of the module.
  - `description`: A brief description of the module's content.
  - `chapters`: A collection of Chapters.

## Chapter

A single content page within a module.

- **Attributes**:
  - `title`: The title of the chapter.
  - `slug`: The URL-friendly identifier for the chapter.
  - `content`: The main content of the chapter in MDX format.
  - `sidebar_position`: The position of the chapter in the sidebar navigation.
