# Research & Decisions: RAG Content Pipeline

This document outlines the key research findings and technical decisions made during the planning phase for the RAG Content Pipeline feature.

## 1. Content Ingestion Strategy

**Context**: The feature specification contained the following clarification request: `[NEEDS CLARIFICATION: Is re-ingestion a manual or automated process? What is the strategy for updating existing embeddings vs. creating new ones?]` This was resolved in the `/sp.clarify` session.

**Decision**: The ingestion process will be a **manual script execution**.

**Rationale**:
- This approach aligns with the clarification provided by the user.
- For the initial implementation, simplicity is key. An automated, event-driven, or scheduled process adds significant complexity (e.g., webhooks, cron jobs, CI/CD integration).
- To handle updates to the source content, the script will adopt a "delete and recreate" strategy. On each run, it will wipe the existing Qdrant collection and repopulate it with freshly crawled content. This avoids the complexity of tracking changed files and updating/deleting individual embeddings.

**Alternatives Considered**:
- **Automated Ingestion**: An automated pipeline that triggers on content changes (e.g., on `git push` to the book's repository). This was rejected as it's out of scope for the current feature and requires more infrastructure.
- **Incremental Updates**: A more complex script that tracks file hashes or timestamps to only update changed content. This was rejected for v1 to prioritize simplicity.

## 2. URL Discovery & Crawling Strategy

**Context**: The pipeline needs to discover all relevant URLs from the Docusaurus website `https://physical-ai-humanoid-robotics-book-pink-delta.vercel.app/`.

**Decision**: The pipeline will parse the `sitemap.xml` file.

**Rationale**:
- A `sitemap.xml` file was confirmed to exist at the target URL.
- Using the sitemap is far more efficient and reliable than recursively crawling the site. It provides a direct list of all canonical URLs, avoiding the need to parse HTML for links and manage visited-URL state.
- This approach is less prone to errors from broken links and is less likely to accidentally crawl external sites.

**Alternatives Considered**:
- **Recursive Crawling**: Starting from the base URL and recursively following all `<a>` tags. This was rejected because a sitemap is available and is the superior method.

## 3. Content Extraction Strategy

**Context**: Once a page is downloaded, the script needs to extract only the main textual content, excluding navigation, sidebars, headers, and footers.

**Decision**: The script will target the `<article>` HTML tag, which typically contains the main content in a Docusaurus site.

**Rationale**:
- Inspecting the HTML of the target Docusaurus site reveals that the primary content of each documentation page is enclosed within an `<article>` tag.
- Targeting a specific, semantic tag is more robust than relying on CSS classes (e.g., `.prose`), which can change with theme updates.
- Using a library like `BeautifulSoup` makes it simple to find this tag and extract all the text within it.

**Alternatives Considered**:
- **CSS Class Selectors**: Targeting a specific CSS class. This was rejected as it's more brittle and subject to change.
- **Heuristic-based Extraction**: Using algorithms to guess the main content block. This is overly complex and unnecessary when a clear structural pattern exists.
