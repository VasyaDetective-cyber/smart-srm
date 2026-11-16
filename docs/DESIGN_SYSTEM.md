# SMART CRM

# Design System and UI/UX Guidelines

**Version:** 1.1  
**Visual style:** Midnight Aurora  
**Interface type:** Modern CRM SaaS platform  
**Theme:** Dark only  
**Primary font:** Plus Jakarta Sans

---

# 1. Design direction

## 1.1. Product impression

Smart CRM should look like a modern, professional SaaS product rather than a basic CRUD application.

The interface should feel:

- professional;
- modern;
- clear;
- reliable;
- visually attractive;
- comfortable for everyday use.

The design must prioritize clarity, consistency, readability, and efficient work.

## 1.2. Midnight Aurora

Midnight Aurora is a dark visual style based on rich blue and purple colors, lighter work surfaces, smooth gradients, rounded components, and subtle glow effects.

The interface must not look almost black. The background should remain dark, but blue and purple tones must be clearly visible. Cards and work areas must be visibly separated from the background.

Use decorative effects carefully. Gradients, shadows, glow, and animation should support hierarchy and interaction rather than distract from the content.

## 1.3. Design principles

1. **Consistency** — all pages use the same visual language.
2. **Clarity** — every element has a clear purpose.
3. **Readability** — text and data remain easy to read on dark surfaces.
4. **Hierarchy** — important information is visually prioritized.
5. **Efficiency** — common actions remain easy to find.
6. **Moderation** — decorative effects never interfere with work.
7. **Responsiveness** — the interface remains usable on different screen sizes.
8. **Data alignment** — the visual design must support the project requirements without inventing new product concepts.

---

# 2. Color system

## 2.1. Primary colors

| Purpose | Color |
|---|---|
| Primary background | `#111A3B` |
| Sidebar | `#10183A` |
| Main work area | `#1B2857` |
| Primary card background | `#202D65` |
| Lighter card background | `#293A78` |
| Border color | `#384B91` |
| Primary blue | `#398BFF` |
| Bright blue | `#2475FF` |
| Purple | `#824BFA` |
| Bright purple | `#A05CFF` |
| Turquoise | `#20D6D0` |

The primary background should be used for the overall application shell. The main work area and cards must use visibly lighter blue surfaces.

## 2.2. Text colors

| Purpose | Color |
|---|---|
| Primary text | `#FFFFFF` |
| Secondary text | `#C4CBEA` |
| Supporting text | `#9BA8D5` |
| Inactive text | `#7886B5` |

Primary text must have strong contrast against its background. Supporting and inactive text may be less bright but must remain readable.

## 2.3. Status colors

| Purpose | Color |
|---|---|
| Success | `#25D6A0` |
| Warning | `#FFC15C` |
| Error | `#FF647C` |
| Information | `#45B7FF` |
| Neutral | `#9BA8C8` |

Status colors should be used consistently for feedback, results, and visual states. Color must not be the only way to communicate meaning.

## 2.4. Gradients

### Primary gradient

`#397BFF → #854BFA`

### Aurora gradient

`#397BFF → #824BFA → #20D6D0`

### Purple-blue gradient

`#553BDB → #A05CFF`

### Decorative gradient

`#172A63 → #3947A5`

Gradients may be used for:

- primary buttons;
- active navigation items;
- selected icons;
- accent blocks;
- decorative backgrounds;
- selected Dashboard elements.

Do not apply gradients to every card, text element, or table row.

## 2.5. Color usage rules

- Use blue and purple as the main visual accents.
- Use turquoise sparingly for emphasis and information.
- Use status colors only for their semantic purpose.
- Keep large reading surfaces mostly solid.
- Avoid placing long text directly on bright gradients.
- Avoid excessive glow and highly saturated backgrounds.
- Maintain sufficient contrast in every state.

---

# 3. Typography

## 3.1. Primary font

Use **Plus Jakarta Sans** throughout the product.

The font is used for:

- page headings;
- section headings;
- body text;
- buttons;
- navigation;
- tables;
- forms;
- hints;
- numeric metrics.

Use one primary font family to keep the interface cohesive.

## 3.2. Type scale

| Element | Size |
|---|---:|
| Main page heading | 28–32px |
| Large section heading | 20–24px |
| Card heading | 16–18px |
| Body text | 14–16px |
| Button text | 14–15px |
| Field label | 13–14px |
| Supporting text | 12–13px |
| Small label | 11–12px |

## 3.3. Font weights

- Regular 400 — body text.
- Medium 500 — labels, navigation, secondary headings.
- SemiBold 600 — primary headings and buttons.
- Bold 700 — important headings and large metrics.

Do not use bold text for every element. Weight should create hierarchy.

## 3.4. Numeric content

Metrics, percentages, dates, and monetary values should use consistent formatting.

Important numbers may use a larger font size and semibold or bold weight. Numbers must remain understandable without relying only on color.

---

# 4. Layout and navigation

## 4.1. Application shell

The main application layout consists of:

1. Left Sidebar.
2. Topbar.
3. Main content area.
4. Page-specific content.

The Login page uses a separate layout without the authenticated application navigation.

## 4.2. Sidebar

The Sidebar is positioned on the left on large screens.

It contains:

- Smart CRM branding;
- primary navigation;
- role-aware navigation visibility;
- current-user information near the bottom.

Primary navigation should visually support the main product areas:

- Dashboard;
- Customers;
- Deals;
- Contacts;
- Activities.

The active item uses:

- a blue-purple gradient or highlighted surface;
- a clear active indicator;
- readable text;
- a consistent icon treatment.

Hover states should use subtle surface highlighting. The Sidebar should feel structured and calm rather than visually heavy.

## 4.3. Topbar

The Topbar is positioned above the main work area.

It may contain:

- the current page context;
- contextual actions;
- user information;
- avatar or initials;
- profile controls;
- search where search is implemented.

Do not add decorative controls or notifications without corresponding functionality.

## 4.4. Main content

Every page should begin with:

- a clear page title;
- a short supporting description;
- a visible primary action area when applicable.

Content should be organized using consistent spacing between:

- page headers;
- filters;
- cards;
- tables;
- lists;
- empty states;
- feedback messages.

---

# 5. Spacing, shape, and depth

## 5.1. Spacing

Use a consistent spacing system based on 4px increments:

- 4px;
- 8px;
- 12px;
- 16px;
- 20px;
- 24px;
- 32px;
- 40px.

Use larger spacing between major page sections and smaller spacing inside compact controls.

## 5.2. Border radius

Recommended values:

- Cards: 12–16px.
- Inputs: 8–12px.
- Buttons: 8–12px.
- Compact badges: 999px or a fully rounded shape.
- Modals: 16px.

Keep radii consistent across equivalent components.

## 5.3. Borders and shadows

Borders should provide most of the visual structure.

Use:

- subtle borders for cards and inputs;
- stronger borders for focused or selected elements;
- soft shadows only for elevated surfaces;
- stronger elevation for modals and overlays.

Do not make every element glow or cast a large shadow.

---

# 6. UI components

## 6.1. Cards

Cards are used for metrics, grouped information, lists, and page sections.

Cards should have:

- rounded corners;
- dark-blue or blue-purple surfaces;
- a subtle border;
- sufficient internal padding;
- clear content hierarchy;
- a light shadow where appropriate;
- a subtle hover effect when interactive.

Cards must remain visually distinct from the page background.

## 6.2. Buttons

Use the following button types.

### Primary

Used for the main action in a page or section.

- blue-purple gradient;
- high-contrast text;
- clear hover and pressed states.

### Secondary

Used for supporting actions.

- dark-blue surface;
- visible border;
- restrained emphasis.

### Outline

Used for low-emphasis actions.

- transparent or surface background;
- visible border;
- readable text.

### Danger

Used for destructive actions.

- danger color treatment;
- clear confirmation where appropriate.

Every button must define:

- default state;
- hover state;
- focus state;
- pressed state;
- disabled state;
- loading state when an operation takes time.

Buttons should only be visible or enabled when the corresponding action is available.

## 6.3. Input fields

Input fields must use:

- dark-blue surfaces;
- light text;
- visible labels;
- rounded corners;
- clear borders;
- visible focus state;
- readable error messages;
- optional hints where necessary.

Placeholder text must not be the only field label.

## 6.4. Tables and lists

Tables and lists should provide:

- clear headers or labels;
- consistent row height;
- sufficient spacing;
- readable alignment;
- subtle row separation;
- hover feedback;
- visible keyboard focus;
- clear actions.

Avoid unnecessary borders and visual noise.

On narrow screens, tables may scroll horizontally or use a deliberate compact layout.

## 6.5. Status badges

Status badges are compact rounded elements with short labels.

They should:

- use semantic colors consistently;
- remain readable on dark backgrounds;
- have enough padding;
- not rely on color alone;
- avoid excessive saturation.

Do not introduce visual status concepts that are not supported by the product model.

## 6.6. Icons

Icons must be:

- simple;
- modern;
- consistent in visual weight;
- consistent in size;
- understandable;
- used only when they improve recognition.

Icons should not replace important text labels when the meaning may be unclear.

## 6.7. Modals

Modals are used for forms, confirmations, and focused actions.

They should have:

- a dimmed background;
- a clear title;
- a short explanation where necessary;
- visible confirm and cancel actions;
- a visible close control;
- clear error placement.

Destructive actions require a visually distinct confirmation state.

## 6.8. Messages and notifications

Use:

- inline messages for field-level problems;
- banners for page-level issues;
- toast notifications for short-lived confirmations;
- empty states for missing content;
- loading states while data is being retrieved.

Messages must not obscure important controls or content.

---

# 7. Component states

Interactive components must define consistent visual states:

1. **Default** — normal state.
2. **Hover** — pointer is over the element.
3. **Focus** — element is focused, including keyboard focus.
4. **Active** — element is selected or pressed.
5. **Disabled** — action is unavailable.
6. **Loading** — operation is in progress.
7. **Error** — operation or input failed.
8. **Success** — operation completed successfully.
9. **Empty** — no content is available.
10. **Unavailable** — content or action cannot be accessed.

States should be communicated through a combination of:

- color;
- borders;
- icons;
- labels;
- layout;
- text feedback.

Never use color as the only indicator.

---

# 8. Animation and transitions

Animations should make the interface feel responsive without distracting the user.

Use:

- smooth button color transitions;
- subtle active-navigation highlights;
- smooth modal appearance;
- short notification transitions;
- restrained page transitions;
- loading indicators;
- subtle hover effects on interactive cards.

Recommended duration for short transitions: **150–250ms**.

Respect reduced-motion preferences.

Avoid:

- constant decorative animation;
- sharp movement;
- excessive glow;
- long transitions;
- animation that delays essential feedback.

---

# 9. Page-level visual direction

The following rules describe the visual treatment of the main pages. Functional fields, calculations, permissions, and business rules are defined in the project requirements and are not duplicated here.

## 9.1. Login

The Login page should create a strong first impression.

Visual structure:

- centered authentication card;
- Smart CRM logo or wordmark;
- page title or greeting;
- clearly separated form fields;
- primary Sign In button;
- visible error area;
- blue-purple decorative background treatment.

The card should be readable and focused. Decorative effects must not compete with the form.

Do not visually imply functionality that is not implemented.

## 9.2. Dashboard

The Dashboard should feel like the main workspace.

Visual structure:

- page title and context;
- metric cards;
- charts or visual data blocks where supported;
- clear separation between summary information and detailed content;
- consistent card heights and spacing;
- restrained use of accent gradients.

Metrics should be visually prioritized, but the design must not invent additional metrics or data blocks.

## 9.3. Customers

The Customers page should use a clear management layout:

- page header;
- primary action area;
- search and filter area where applicable;
- table or list;
- pagination or navigation controls;
- empty, loading, and error states.

The layout should support scanning many records without visual overload.

## 9.4. Deals

The Deals page may use a table, a Kanban-style layout, or both when supported by the product.

The visual design should provide:

- clear stage or status visibility;
- readable deal cards or rows;
- consistent value and metadata alignment;
- filters that are visually easy to identify;
- clear transition feedback;
- distinct terminal-state treatment.

The visual system must not suggest unsupported transitions or features.

## 9.5. Contacts

The Contacts page should provide a clean list/detail experience.

The visual design should emphasize:

- person identity;
- readable contact information;
- relationship context;
- consistent table or card layout;
- clear create and edit actions;
- empty and loading states.

Use avatars or colored initials only when they improve recognition.

## 9.6. Activities

The Activities page should support chronological scanning.

The visual design should emphasize:

- activity type;
- title or short description;
- associated context;
- date and time;
- filters;
- chronological ordering;
- clear empty and loading states.

Use simple visual distinctions between activity types without adding unsupported statuses.

---

# 10. Role-aware visual behavior

The interface should visually respond to the permissions returned by the application.

- Show only navigation items and actions available to the current user.
- Keep unavailable actions disabled or hidden according to the product’s interaction rules.
- Make restricted states understandable.
- Do not expose sensitive content through visual previews.
- Do not treat frontend visibility as a security boundary.
- Keep the visual language consistent across roles.

This section defines presentation behavior only. The actual roles and permissions are defined in the project requirements.

---

# 11. Validation and feedback presentation

Validation is part of the visual experience.

The interface should:

- keep labels visible;
- place errors near the relevant field;
- use clear, human-readable wording;
- preserve entered values when possible;
- visually distinguish invalid fields;
- prevent duplicate submissions during loading;
- show success feedback after completed actions;
- show page-level errors without destroying the current layout.

Exact validation rules are defined in the project requirements and should not be duplicated in this design document.

---

# 12. Accessibility

The interface should follow WCAG 2.2 AA practices wherever applicable.

Provide:

- sufficient contrast;
- visible keyboard focus;
- semantic headings;
- labels associated with controls;
- descriptive button names;
- keyboard-operable modals;
- accessible status messages;
- readable error messages;
- non-color indicators for important states;
- touch targets of at least 44×44px.

The interface must remain understandable when:

- zoomed;
- navigated by keyboard;
- viewed with reduced motion;
- used with assistive technology;
- displayed on a smaller screen.

---

# 13. Responsiveness

The interface must adapt to content and screen size.

## Large screens

- full Sidebar;
- wide content area;
- multiple cards in one row;
- complete table layouts;
- generous spacing.

## Tablets

- reduced spacing;
- adapted card layout;
- compact navigation;
- horizontal scrolling for wide tables when necessary.

## Mobile devices

- compact or hidden Sidebar;
- menu-based navigation;
- vertically stacked cards;
- full-width forms;
- accessible buttons;
- compact tables or mobile-specific list presentation.

Responsiveness must not be achieved only by shrinking every element. Content hierarchy and interaction patterns should also adapt.

---

# 14. Implementation guidance

## 14.1. Shared tokens

Centralize:

- colors;
- gradients;
- typography;
- spacing;
- border radii;
- shadows;
- transitions;
- component states.

Use CSS variables or an equivalent centralized token system.

## 14.2. Shared components

Create reusable visual components for common patterns, such as:

- Sidebar;
- Topbar;
- PageHeader;
- StatCard;
- BaseButton;
- BaseInput;
- DataTable;
- StatusBadge;
- Modal;
- Notification;
- EmptyState;
- LoadingState.

Equivalent components should look and behave consistently across pages.

## 14.3. Bootstrap

Bootstrap may be used for:

- grid;
- responsive behavior;
- layout utilities;
- base interaction patterns.

The default Bootstrap appearance must not define the final product design. Components must be styled according to Midnight Aurora.

Avoid mixing default Bootstrap styling with custom styling inconsistently.

## 14.4. Frontend foundation

The visual system should support the project’s Vue 3, Vue Router, Bootstrap, CSS/SCSS, and API-based architecture.

The design document does not redefine the API, data model, authentication rules, or business logic. It only defines how the interface should present the product.

---

# 15. Week 8 visual scope

The Week 8 visual scope includes:

- Midnight Aurora tokens;
- Plus Jakarta Sans;
- shared application shell;
- Sidebar and Topbar;
- Login page styling;
- shared page headers;
- base Dashboard visual structure;
- Customers, Deals, Contacts, and Activities page layouts;
- reusable buttons, cards, inputs, tables, badges, modals, and notifications;
- loading, empty, error, disabled, and success states;
- responsive behavior;
- keyboard focus and basic accessibility;
- consistent Bootstrap customization.

Week 8 should establish the visual foundation without inventing fake data, unsupported features, or new product requirements.

---

# 16. Explicit visual MVP exclusions

The MVP visual system does not include:

- light theme or theme switching;
- a separate visual system for different roles;
- unnecessary decorative notifications;
- invented entities, fields, statuses, or relationships;
- unsupported dashboard blocks;
- excessive glassmorphism;
- excessive neon glow;
- large animated backgrounds;
- visual features that imply unsupported functionality;
- a separate Analytics page when analytics belong to Dashboard;
- mobile-native application design;
- unrelated branding systems.

These exclusions protect the visual direction and keep the interface focused.

---

# 17. Requirements alignment

This document defines the visual system and UI/UX presentation rules only.

Functional requirements remain the source of truth for:

- fields;
- metrics;
- formulas;
- deal stages;
- transitions;
- filters;
- activity types;
- relationships;
- sorting;
- roles;
- permissions;
- validation rules;
- API behavior.

The design must remain visually consistent with those requirements, but this document does not repeat them. If a visual decision conflicts with the functional requirements, the functional requirements take priority and the visual treatment must be adjusted.

---

# 18. Final concept

Smart CRM should be a modern, professional, and visually cohesive SaaS product.

The visual foundation is Midnight Aurora: a dark blue interface with clearly visible blue and purple accents, lighter cards, smooth gradients, consistent typography, clear hierarchy, and subtle interaction feedback.

The main principle is:

**Smart CRM must not only look beautiful. It must be clear, comfortable, consistent, and pleasant to use every day.**