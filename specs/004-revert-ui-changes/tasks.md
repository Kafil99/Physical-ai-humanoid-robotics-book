# Tasks: Revert UI Changes

**Input**: Design documents from `/specs/004-revert-ui-changes/`
**Prerequisites**: plan.md, spec.md

## Phase 1: Reversion Planning & Assessment

**Purpose**: To identify all UI and logo changes introduced during the enhancement process and confirm the original baseline.

- [X] T001 Identify all UI-related changes in `docusaurus.config.js`, `sidebars.js`, `src/css/custom.css`, `src/pages/index.js`, `src/components/HomepageFeatures.js`.
- [X] T002 Identify all logo-related changes in `static/img/logo.svg` and `static/img/favicon.ico`.
- [X] T003 Confirm the original layouts, typography, color scheme, components, and branding assets by referencing the project's initial state (e.g., Git history).

## Phase 2: UI Reversion

**Purpose**: To restore all UI elements to their original state.

- [X] T004 [US1] Revert `src/css/custom.css` to its original content, restoring color palette, typography, and component styling.
- [X] T005 [US1] Revert `src/pages/index.js` to its original content, restoring layout and component usage.
- [X] T006 [US1] Revert `src/components/HomepageFeatures.js` to its original content.
- [X] T007 [US1] Revert `sidebars.js` to its original content, restoring navigation structure.

## Phase 3: Logo Reversion

**Purpose**: To remove the newly designed custom logo and restore the original.

- [X] T008 [US1] Revert `static/img/logo.svg` to its original content (or remove if it was not present).
- [X] T009 [US1] Revert `static/img/favicon.ico` to its original content (or remove if it was not present).
- [X] T010 [US1] Revert `docusaurus.config.js` to its original configuration, specifically regarding `navbar.logo` and `favicon` settings.

## Phase 4: Integration & Consistency Rollback

**Purpose**: To ensure visual consistency with the original design across all screens.

- [ ] T011 [US1] Review all affected pages to ensure no visual elements from the new logo or UI enhancements remain.
- [ ] T012 [US1] Verify that spacing, alignment, and general styling have reverted to the original design baseline.

## Phase 5: Review & Validation

**Purpose**: To confirm the successful restoration of the UI and ensure no new issues are introduced.

- [ ] T013 [US1] Visually inspect all pages to confirm 100% adherence to the original UI design.
- [ ] T014 [US1] Start the development server (via `npm run start`) and check the browser console for any new UI-related errors.
- [ ] T015 [US1] Verify that page load performance is consistent with the original version.

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Phase 1 (Reversion Planning & Assessment)**: No dependencies. Must be completed first.
-   **Phase 2 (UI Reversion)**: Depends on Phase 1 completion (T003).
-   **Phase 3 (Logo Reversion)**: Depends on Phase 1 completion (T003). Can be done in parallel with Phase 2.
-   **Phase 4 (Integration & Consistency Rollback)**: Depends on Phase 2 (T007) and Phase 3 (T010) completion.
-   **Phase 5 (Review & Validation)**: Depends on Phase 4 completion (T012).

### User Story Dependencies

-   **User Story 1 (Restore Original UI)**: All phases contribute to this story.

### Parallel Opportunities

-   Tasks within Phase 1 (T001, T002, T003) can be performed in parallel.
-   Phase 2 (UI Reversion) and Phase 3 (Logo Reversion) can be executed in parallel.
-   Tasks within Phase 5 (T013, T014, T015) can be executed in parallel.

### Implementation Strategy

-   Prioritize identifying the original state of all affected files.
-   Perform reversions systematically, file by file.
-   Thoroughly verify the reverted UI against the original baseline.
