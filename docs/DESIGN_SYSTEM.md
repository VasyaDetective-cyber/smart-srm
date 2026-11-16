# Smart CRM Design System and UI/UX Guidelines

**Status:** Agreed MVP direction  
**Product:** Smart CRM  
**Language:** English  
**Theme:** One dark theme only

## 1. Purpose and product principles

Smart CRM is a focused customer, deal, contact, and activity workspace. The interface should make the next useful action obvious, keep business data scannable, and provide consistent feedback after every meaningful interaction.

The product should feel calm, capable, and modern rather than theatrical. Prefer clear hierarchy, useful density, and progressive disclosure over decoration. Every visual decision in this document is subordinate to the functional requirements and backend contract.

## 2. Visual direction: Midnight Aurora

Midnight Aurora is a dark interface with readable, blue-purple surfaces—not a near-black interface. The background is deep navy, cards are visibly lifted from it, and restrained aurora gradients provide hierarchy and emphasis. Gradients are accents, never a substitute for contrast or semantic status color.

### 2.1 Color tokens

Use semantic tokens in implementation; do not hard-code colors in components.

| Token | Value | Use |
|---|---|---|
| `--color-bg` | `#10182B` | Application background |
| `--color-surface-1` | `#17233D` | Navigation and primary panels |
| `--color-surface-2` | `#1E2D4D` | Cards, tables, forms |
| `--color-surface-3` | `#26395F` | Hover, selected, and raised surfaces |
| `--color-border` | `#3A4D73` | Default borders and dividers |
| `--color-border-strong` | `#536B9A` | Focus and emphasized borders |
| `--color-text` | `#F4F7FF` | Primary text |
| `--color-text-muted` | `#AAB9D6` | Secondary text and metadata |
| `--color-text-subtle` | `#7F91B5` | Supporting text only |
| `--color-primary` | `#7C8CFF` | Main actions and links |
| `--color-primary-strong` | `#9A7CFF` | Hover, active, and emphasis |
| `--color-cyan` | `#45D6E8` | Informational accents |
| `--color-success` | `#46D39A` | Success and won/completed states |
| `--color-warning` | `#F4BE5E` | Warning and attention states |
| `--color-danger` | `#F2778A` | Errors, destructive actions, lost states |

Recommended gradients:

- **Aurora primary:** `linear-gradient(135deg, #6675F6 0%, #9A6BFF 100%)`
- **Aurora cool:** `linear-gradient(135deg, #425FC8 0%, #287EAA 100%)`
- **Panel glow:** a low-opacity blue-purple radial gradient behind a selected or featured panel only.

Text and controls must remain legible over every gradient. Do not use gradients for long text, dense tables, or status badges.

### 2.2 Typography

Use **Plus Jakarta Sans** throughout the product. Use the font’s regular weight for body text, medium or semibold for labels and controls, and bold sparingly for page titles and key metrics.

- Page title: 28–32px, 700, line-height 1.2.
- Section title: 18–20px, 600, line-height 1.3.
- Body: 14–16px, 400, line-height 1.5.
- Label and table text: 12–14px, 500–600.
- Metric value: 28–36px, 700; never rely on color alone.

Use sentence case. Keep labels short and action-oriented. Numbers should use tabular numerals where supported.

### 2.3 Shape, depth, and spacing

Use a 4px spacing base: 4, 8, 12, 16, 20, 24, 32, and 40px. Use 10–12px corner radii for cards and inputs, and 8px for compact controls. Borders should carry more of the structure than shadows. Use a soft shadow only for an overlay or clearly raised panel.

## 3. Application layout and navigation

The application shell has:

1. A left sidebar with product identity and primary navigation.
2. A top bar with the current page title, contextual actions, and the signed-in user menu.
3. A scrollable content area with a consistent maximum reading width.

Primary navigation must expose the agreed product areas: **Dashboard, Customers, Deals, Contacts, and Activities**. The active item uses a tinted surface, a visible leading indicator, and a text/icon treatment that remains distinguishable without color alone.

On smaller screens, collapse the sidebar into a menu or bottom navigation while preserving the same information architecture. Do not create a second mobile-only feature set.

## 4. Component rules and states

Every interactive component must define default, hover, focus-visible, pressed, disabled, loading, empty, error, and success behavior where applicable.

### Buttons

- Primary: aurora gradient, high-contrast text, one primary action per region.
- Secondary: surface fill with border.
- Tertiary: transparent, text-led action.
- Destructive: danger treatment and confirmation when the action cannot be undone.
- Disabled: reduced emphasis and no pointer interaction; do not communicate disabled state with opacity alone.

Buttons must have a visible `:focus-visible` ring and a minimum 44×44px touch target.

### Forms and inputs

Labels are always visible; placeholder text is not a label. Inputs use a clear border, a readable value, and an inline validation message tied to the field. Preserve entered values when validation fails. Required fields are indicated in the label and explained once near the form.

Use text inputs for text, select controls for constrained options, and date/time controls for dates and times. Do not introduce fields or validation rules that are not present in the requirements or backend contract.

### Tables, lists, and filters

Tables should support readable column alignment, row hover, keyboard focus, and responsive horizontal scrolling or a deliberate stacked layout. Keep the most important identifier and status visible first. Filters show their active state and provide a clear reset action. Sorting shows both the active column and direction.

### Feedback

Use inline messages for field errors, banners for page-level errors, and toasts only for short-lived confirmation. Loading states should preserve layout with skeletons or explicit progress. Empty states explain what is empty and provide the relevant next action without inventing data.

## 5. Page designs and domain requirements

The UI reflects the following required data and behavior. The backend/domain requirements remain authoritative; this section defines their presentation and interaction.

### 5.1 Dashboard

The Dashboard opens with a concise greeting/context line, then the required metric cards and the agreed supporting views. Metric cards must show a label, value, comparison or period when available, and a plain-language definition on hover or accessible description.

Required metrics and formulas:

- **Total Customers:** count of customer records.
- **Total Deals:** count of deal records.
- **Open Pipeline Value:** sum of the value of deals that are not in a terminal won or lost stage.
- **Won Revenue:** sum of the value of won deals.
- **Conversion Rate:** `won deals / (won deals + lost deals) × 100`. If the denominator is zero, display `—`, not `0%`.

Use the exact source fields and terminal-stage definitions supplied by the backend. Do not silently change currency, date range, rounding, or inclusion rules. If a metric is unavailable, show an honest unavailable state rather than a guessed value.

### 5.2 Customers

Customers is a searchable, filterable list with a clear create action and a detail view. Show the required customer fields from the domain contract; at minimum, the interface must provide a stable customer identity and the fields required by the project’s customer model. Do not add new persisted fields without a requirements change.

Search must clearly state which supported customer fields it searches, update results predictably, preserve the query during navigation, and provide an empty result state. Customer detail should expose related information only where the existing requirements define that relationship.

### 5.3 Deals

Deals may be represented as a table and/or stage-based board only if both views preserve the same records and actions. Each deal displays its required identity, value, customer relationship, stage, and other backend-defined fields.

Use the agreed deal stages exactly as defined by the backend. A stage change is allowed only through an agreed transition. The UI must not imply that every stage can transition to every other stage. Invalid transitions return an actionable error and leave the previous stage visible.

Deal filters must include the required stage filter and any other backend-defined filters. Show active filters, support reset, and keep filter state when returning from a detail view. Terminal stages (won and lost, where defined) must be visually distinct and must not be conflated with open pipeline value.

### 5.4 Contacts

Contacts is a list/detail experience for the required contact fields. Display the contact’s identity and all required contact attributes using readable labels, consistent formatting, and explicit empty values. If a contact is associated with a customer, show that relationship using the backend relationship; do not duplicate or infer customer data locally.

### 5.5 Activities

Activities show the required activity types, relationships, and sort behavior. Activity type is selected from the agreed domain values; it is not an arbitrary free-text status. Each activity clearly identifies its related customer, contact, or deal when that relationship exists in the requirements.

The default ordering is the agreed chronological sort, with a visible control for changing direction if supported. Dates and times use the user’s locale for display while preserving unambiguous meaning. Activity creation and editing must validate required relationships and fields before submission.

## 6. Role-aware UI and permissions

The interface must reflect authorization returned by the backend; hiding a control is not a security boundary. Unauthorized API responses are handled as permission errors and never presented as generic success.

- **Manager:** can access the manager-authorized CRM workflows and actions defined by the requirements. The UI may expose management actions only when the backend grants them.
- **Admin:** can access the admin-authorized workflows and actions defined by the requirements, including administrative controls where specified. Admin-only controls must be visibly separated from routine CRM actions.

Do not invent permissions, roles, audit features, invitations, or settings. For a user without permission, use a consistent unavailable/forbidden state and preserve navigation clarity.

## 7. Validation, errors, and data integrity

Validate obvious format and required-field errors at the point of entry, then rely on the backend as the source of truth. Map backend validation errors to the relevant field whenever possible. Never report a failed mutation as successful.

For destructive or irreversible actions, explain the consequence and require explicit confirmation. Prevent duplicate submissions while a mutation is pending. After a successful mutation, update the affected view from the returned server data or re-fetch it; do not fabricate an optimistic record that can diverge from the backend.

## 8. Accessibility and responsiveness

Target WCAG 2.2 AA practices: sufficient contrast, visible keyboard focus, semantic headings, labels associated with controls, meaningful button names, keyboard-operable dialogs, and status messages announced to assistive technology. Never use color as the only indicator of stage, error, permission, or success.

Responsive behavior should be designed at content breakpoints rather than device names. At narrow widths, stack metric cards, keep actions reachable, allow tables to scroll or transform intentionally, and ensure dialogs fit within the viewport. Touch targets should be at least 44×44px. Zoom to 200% must not make required actions unusable.

Respect reduced-motion preferences. Animation is limited to short state transitions and must never delay essential feedback.

## 9. Implementation guidance

Centralize tokens, typography, spacing, radii, and semantic colors. Build shared primitives before page-specific variants. Keep domain labels, stage values, activity types, permissions, and metric calculations aligned with the backend contract and a single source of truth.

Pages should compose the same shell, headings, cards, forms, tables, filters, status indicators, loading states, and error patterns. Prefer explicit states over clever abstractions. Test keyboard navigation, responsive layouts, empty data, validation failures, unauthorized responses, and loading/error transitions for every page.

## 10. Week 8 scope

Week 8 should deliver the agreed MVP UI polish and integration pass across the Dashboard, Customers, Deals, Contacts, and Activities areas: shared Midnight Aurora styling, responsive shell/navigation, required metric presentation and formulas, required search/filter/sort interactions, role-aware visibility, validation and error states, loading/empty states, and accessibility review.

Week 8 does not expand the domain model or change API behavior. Any mismatch discovered between the UI and backend requirements must be recorded and resolved explicitly rather than hidden in presentation logic.

## 11. Explicit MVP exclusions

Unless separately added to the requirements, MVP excludes:

- A light theme or theme switching.
- Additional roles, custom permission builders, or invented admin workflows.
- New CRM entities, custom fields, or unapproved relationships.
- Marketing automation, email campaigns, chat, telephony, or messaging integrations.
- Billing, subscriptions, payments, or forecasting beyond the required metrics.
- AI-generated recommendations, enrichment, or summaries.
- Real-time collaboration, comments, mentions, or an activity feed beyond required Activities.
- File storage, imports/exports, bulk editing, advanced reporting, or configurable dashboards.
- Mobile-native applications and offline mode.

These exclusions protect the agreed MVP boundary; they do not prevent future design work when requirements are formally updated.

## 12. Assumptions and source of truth

The repository inspected for this document contained no existing requirements or documentation files and an empty `sources/` directory. Accordingly, this document records the explicitly agreed visual direction and the domain areas, metrics, relationships, transitions, sorting, and role constraints named in the task. Exact field names, complete stage/type enumerations, transition matrices, and permission matrices must be taken from the project’s authoritative backend requirements when they are available; this document must not be used to invent them.
