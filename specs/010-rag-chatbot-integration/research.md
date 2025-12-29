# Research: RAG Chatbot Integration

**Purpose**: This document outlines the key technical decisions made to resolve ambiguities identified during the planning phase for the RAG Chatbot Integration feature.

---

## 1. Frontend: Chatbot UI Styling

-   **Topic**: Selecting a UI library or styling approach for the chatbot components.
-   **Requirement**: The UI must be "clean and attractive," responsive, and lightweight.

### Options Considered

1.  **React-Chatbot-Kit**: A pre-built library of chatbot components.
2.  **Mantine UI**: A full-featured React component library.
3.  **Custom Components with Tailwind CSS**: Build the UI from scratch using a utility-first CSS framework.

### Decision: Custom Components with Tailwind CSS

-   **Rationale**:
    -   **Design Flexibility**: Building custom components gives us full control over the look and feel, ensuring the chatbot's style perfectly matches the Docusaurus site's existing design.
    -   **No New Dependencies**: Avoids adding a new, potentially heavy component library just for the chatbot.
    -   **Consistency**: Reusing existing styling patterns (if any) is easier. Tailwind is utility-first and won't clash with existing CSS.
-   **Implications**: Requires more initial development effort than using a pre-built kit, but provides a more tailored and lightweight result.

---

## 2. Frontend: Docusaurus Integration Strategy

-   **Topic**: Best practice for embedding a persistent React component (the chatbot) across all pages in a Docusaurus site.
-   **Requirement**: The chatbot icon and interface must be available on all pages of the book.

### Options Considered

1.  **Manual Component Injection**: Add the `<Chatbot />` component to the bottom of every `.mdx` file. (Not scalable)
2.  **Docusaurus Theme Swizzling**: Use Docusaurus's built-in feature to override a core theme component, like the main layout.

### Decision: Theme Swizzling to Wrap the Root Layout

-   **Rationale**:
    -   **Centralized Control**: By "swizzling" the `Root` or `Layout` component, we can insert the chatbot component at the top level of the entire site. This single change propagates to all pages.
    -   **Clean Separation**: The chatbot logic remains separate from the page content. We are simply wrapping the Docusaurus page structure with our chatbot provider/UI.
    -   **Maintainability**: This is the officially recommended Docusaurus approach for such customizations, ensuring better compatibility with future updates.
-   **Implications**: We will create a custom `src/theme/Root.js` file that imports the original `Root` component and our new `Chatbot` component, rendering the chatbot alongside the main site content.

---

## 3. Frontend: Selected Text UX Pattern

-   **Topic**: The user experience pattern for triggering the "Ask about selection" functionality.
-   **Requirement**: Users must be able to ask a question about a specific piece of text they highlight.

### Options Considered

1.  **Browser Context Menu**: Add a custom option to the right-click menu. (Complex and brittle)
2.  **Floating Button**: A small button or icon appears immediately above or below the selected text.
3.  **Static UI Button**: A button in the main chatbot UI becomes "active" when text is selected.

### Decision: Floating Button on Text Selection

-   **Rationale**:
    -   **Intuitive UX**: This pattern provides a direct and immediate visual cue right at the point of interaction. The user selects text, and the action they can take appears in the same location.
    -   **Low Cognitive Load**: The user doesn't have to look elsewhere (like the main chatbot window) to find the relevant action.
    -   **Good Discoverability**: The button's appearance upon selection makes the feature highly discoverable.
-   **Implications**: We will need to implement a JavaScript listener for `mouseup` events, check for a text selection, and then dynamically position a button in the DOM near the selection range.
