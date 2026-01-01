# Implementation Plan: Chatbot UI/UX Overhaul

**Feature Branch**: `011-fix-chatbot-ui`
**Feature Spec**: [spec.md](spec.md)

This plan outlines the precise, step-by-step strategy to perform a mandatory overhaul of the chatbot UI, fixing all identified bugs and implementing a professional, modern design.

---

## 1. Technical Context & Decisions

-   **Primary Goal**: Fix all UI bugs and implement a professional, floating chatbot experience.
-   **Core Technology**: React, Docusaurus, Tailwind CSS.
-   **Architectural Constraint**: All UI components must be self-contained within `src/components/Chatbot/` and injected via `src/clientModules/chatbot.js`. **No backend changes are permitted.**
-   **Key Decision**: The root cause of the layout bug ("chatbot under footer") is a CSS stacking context conflict. The plan's foundational step is to fix the mounting strategy to isolate the chatbot from Docusaurus's DOM structure, which will guarantee the `position: fixed` and `z-index` properties work as intended.

---

## 2. Implementation Strategy & File Audit Order

The implementation will be a full rewrite of the chatbot's frontend components. The order is critical to ensure a stable foundation before building the details.

1.  **`src/clientModules/chatbot.js` (FIX FIRST)**: This is the entry point. It contains the critical import bug and the flawed mounting strategy. Fixing this first is mandatory to ensure the chatbot can render at all and to solve the layout bug's root cause.
2.  **`src/components/Chatbot/ChatContainer.js`**: This is the root component. It will be rewritten to be the single source of truth for all state (`isOpen`, `selectedText`, etc.) and to implement the primary floating layout and toggle button.
3.  **`src/components/Chatbot/ChatWindow.js`**: The main panel. Will be rewritten for the new design and to correctly display child components.
4.  **`src/components/Chatbot/ChatInput.js` & `Message.js`**: These will be rewritten with the new professional styling.
5.  **`FloatingActionButton.js`**: This will be audited and styled to fit the new design.

---

## 3. Step-by-Step Execution Plan

### Phase 1: Foundational Fixes (Root Cause)

**Goal**: Fix the critical rendering and layout bugs.

-   **Task 1: Correct the Mounting Strategy**:
    -   **File**: `src/clientModules/chatbot.js`
    -   **Action**: Rewrite the file. Create a new `div` element, append it directly to `document.body`, and use `createRoot` to render the React component tree into this isolated `div`. This will break it out of any parent stacking contexts.

-   **Task 2: Fix the Import Bug**:
    -   **File**: `src/clientModules/chatbot.js`
    -   **Action**: While rewriting, change the import from `import Chatbot from ...` to `import ChatContainer from ...` to match the actual root component.

### Phase 2: UI Overhaul & State Management

**Goal**: Implement the new, professional UI and stabilize the state logic.

-   **Task 3: Rewrite the Root Component (`ChatContainer.js`)**:
    -   **File**: `src/components/Chatbot/ChatContainer.js`
    -   **Action**: Perform a full rewrite.
        -   **State**: Initialize `const [isOpen, setIsOpen] = useState(false);` as the single source of truth for visibility.
        -   **Layout**: The main container will now manage the fixed positioning for the toggle button and the conditionally rendered chat window.
        -   **Toggle Logic**: Implement a simple `onClick={() => setIsOpen(!isOpen)}` on the floating button.
        -   **Selected-Text Logic**: Simplify the state to only use `selectedText` and `selectionRect`. The complex `isContextPrimed` state will be removed and its logic simplified.

-   **Task 4: Redesign the Chat Window & Child Components**:
    -   **Files**: `ChatWindow.js`, `MessageList.js`, `Message.js`, `ChatInput.js`, `FloatingActionButton.js`
    -   **Action**: Rewrite each file to implement the new SaaS-style design.
        -   **Colors**: Use a neutral palette (e.g., `bg-white`, `bg-gray-50`) with a single brand accent color (e.g., `bg-blue-600`) for user elements and actions.
        -   **Typography**: Use standard, readable system fonts.
        -   **Layout**: Use Flexbox for alignment and consistent spacing/padding throughout.
        -   **Styling**: Apply `rounded-xl`, `shadow-2xl`, and `border` for a modern look. The toggle icon will be circular. Use icons from `react-icons` for a professional feel.

### Phase 3: Verification

**Goal**: Ensure all mandatory requirements are met.

-   **Checklist 1: Initial State**:
    -   Verify on page load that the chat window is not visible and only the floating icon appears at the bottom-right.
-   **Checklist 2: Toggle Behavior**:
    -   Confirm clicking the icon reliably opens the chat window with a smooth animation.
    -   Confirm clicking the icon again reliably closes the window.
-   **Checklist 3: Floating Behavior**:
    -   Scroll the main page content and confirm the chatbot and icon remain fixed in the viewport, floating above all content, including the footer.
-   **Checklist 4: No Errors**:
    -   Open the browser's developer console and ensure there are no React rendering errors or other runtime exceptions.

---

## 4. Generated Artifacts

-   **Implementation Plan**: `specs/011-fix-chatbot-ui/plan.md`