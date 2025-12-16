# Design Guidelines: UI Enhancement and Logo Integration

## 1. Color Palette

Based on the project's technical nature and the desire for a modern, clean aesthetic:

-   **Primary Brand Color**: `#4690FF` (A vibrant, professional blue, representing technology and innovation)
    -   `--ifm-color-primary`: `#4690FF`
    -   `--ifm-color-primary-dark`: `#367EE0`
    -   `--ifm-color-primary-darker`: `#2B70D0`
    -   `--ifm-color-primary-darkest`: `#205CA6`
    -   `--ifm-color-primary-light`: `#5FA0FF`
    -   `--ifm-color-primary-lighter`: `#76B0FF`
    -   `--ifm-color-primary-lightest`: `#99C7FF`
-   **Secondary Accent Color**: `#3CAD6E` (A complementary green, for highlights or success states)
-   **Text Colors**:
    -   `--ifm-font-color-base`: `#333333` (Dark Gray for body text)
    -   `--ifm-color-secondary-text`: `#666666` (Medium Gray for secondary text/labels)
-   **Background Colors**:
    -   `--ifm-background-color`: `#FFFFFF` (Clean White for main content areas)
    -   `--ifm-background-color-light`: `#F8F8F8` (Light Gray for subtle differentiation)
-   **Call to Action (CTA) Buttons**: Use `--ifm-color-primary` for primary CTAs.

## 2. Typography

Prioritizing readability, professionalism, and a modern feel.

-   **Font Families**:
    -   **Headings (H1-H6)**: `Montserrat`, sans-serif (Bold, clean, modern)
    -   **Body Text**: `Roboto`, sans-serif (Highly readable, neutral)
    -   **Code Blocks & Monospace**: `Fira Code`, monospace (Clear, developer-friendly ligatures optional)
-   **Font Sizes**: Establish a scalable type system (e.g., based on `rem`).
    -   `--ifm-font-size-base`: `16px` (Default body text size)
    -   Headings: Scale up appropriately (e.g., `h1: 3.0rem`, `h2: 2.25rem`, `h3: 1.75rem`, etc.)
-   **Line Spacing (Line-height)**:
    -   `--ifm-line-height-base`: `1.5` for body text.
    -   Headings: Tighter line height (e.g., `1.2`) for visual density.
-   **Font Weights**: Use a limited set (e.g., Regular, Medium, SemiBold, Bold) to maintain hierarchy.
-   **Contrast**: Ensure all text has sufficient contrast against its background for WCAG 2.1 AA accessibility (minimum contrast ratio of 4.5:1 for normal text, 3:1 for large text).

## 3. Spacing and Layout

Consistent spacing creates visual harmony and clear information hierarchy.

-   **Spacing Unit**: Establish a base spacing unit, e.g., `--ifm-spacing-unit: 8px;`
    -   All paddings, margins, and gaps will be multiples of this unit (e.g., `8px, 16px, 24px, 32px`).
-   **Max Content Width**: Define a maximum width for main content areas to improve readability on large screens.
-   **Responsive Design**: Ensure layouts adapt gracefully to different screen sizes (mobile, tablet, desktop) using Docusaurus's responsive utilities or custom media queries.

## 4. Components

Standardize the look and feel of common UI components.

-   **Buttons**:
    -   `--ifm-button-padding-vertical`: `10px`
    -   `--ifm-button-padding-horizontal`: `20px`
    -   `--ifm-button-border-radius`: `4px`
    -   Define styles for: Primary, Secondary, Outline, Ghost buttons. Include clear hover and active states.
-   **Form Inputs**:
    -   Consistent border, background, padding.
    -   Clear focus state (e.g., using `--ifm-color-primary`).
    -   Validation states (error, success).
-   **Icons**:
    -   Prefer vector-based icons (SVG) for scalability.
    -   Consistent sizing and color.
-   **Navigation**:
    -   Clear active states for current page/section.
    -   Intuitive hierarchy in sidebars and top navigation.

## 5. Logo Guidelines

-   **Design**: Simple, modern, and abstract/geometric to represent AI and Robotics. Incorporate the primary blue (`#4690FF`) and potentially the secondary green (`#3CAD6E`).
-   **Format**: Primarily SVG for scalability, with fallback PNGs for older contexts if needed.
-   **Placement**: Prominently featured in the navbar (header), favicon, and potentially social media cards.
-   **Clear Space**: Ensure adequate clear space around the logo to maintain visibility.
