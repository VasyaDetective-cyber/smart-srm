# Smart CRM MVP Requirements Specification

## 1. Project Scope
This project is a web-based CRM system for managing clients and sales pipelines. The main goal of the MVP is to implement a core client-server architecture using Vue 3, FastAPI, and PostgreSQL. Third-party integrations (email, notifications) and advanced Lead Scoring algorithms are excluded from this initial development phase.

## 2. Data Model (Entities and Relationships)
The MVP database will consist of 5 core tables:
* **User:** System user (role: Manager or Admin).
* **Customer:** Client company. Has a mandatory relationship with a specific manager (`owner_id`) for access control.
* **Contact:** Contact person (company representative). Belongs to a specific Customer.
* **Deal:** Commercial deal (amount, success probability, creation date, expected close date). Linked to both Customer and User.
* **Activity:** Activity log (calls, meetings, notes). Always linked to a Customer, and optionally linked to a specific Deal.

### 2.1 Entity Field Definitions

**User**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| full_name | VARCHAR(255) | NOT NULL | User's full name |
| role | ENUM | NOT NULL, DEFAULT='Manager' | One of: 'Manager', 'Admin' |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Customer**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Unique identifier |
| name | VARCHAR(255) | NOT NULL | Company name |
| owner_id | UUID | FK, NOT NULL | Reference to User (manager) |
| industry | VARCHAR(100) | Optional | Industry classification |
| phone | VARCHAR(20) | Optional | Company phone |
| email | VARCHAR(255) | Optional | Company email |
| address | TEXT | Optional | Company address |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Contact**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Unique identifier |
| customer_id | UUID | FK, NOT NULL | Reference to Customer |
| first_name | VARCHAR(100) | NOT NULL | Contact first name |
| last_name | VARCHAR(100) | NOT NULL | Contact last name |
| title | VARCHAR(100) | Optional | Job title |
| email | VARCHAR(255) | Optional, UNIQUE per customer | Contact email |
| phone | VARCHAR(20) | Optional | Contact phone |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Deal**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Unique identifier |
| customer_id | UUID | FK, NOT NULL | Reference to Customer |
| owner_id | UUID | FK, NOT NULL | Reference to User (manager) |
| title | VARCHAR(255) | NOT NULL | Deal title |
| amount | DECIMAL(15,2) | NOT NULL, > 0 | Deal amount in currency |
| probability | INTEGER | NOT NULL, 0-100 | Success probability as percentage |
| status | ENUM | NOT NULL, DEFAULT='New' | One of: 'New', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost' |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| expected_close_date | DATE | NOT NULL | Expected close date |
| closed_at | TIMESTAMP | Optional | Actual close timestamp (set when Won/Lost) |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

**Activity**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | UUID | PK | Unique identifier |
| customer_id | UUID | FK, NOT NULL | Reference to Customer |
| deal_id | UUID | FK, Optional | Reference to Deal |
| activity_type | ENUM | NOT NULL | One of: 'Call', 'Meeting', 'Email', 'Note' |
| title | VARCHAR(255) | NOT NULL | Activity title |
| description | TEXT | Optional | Detailed description |
| scheduled_date | TIMESTAMP | Optional | Scheduled date/time for future activities |
| created_at | TIMESTAMP | NOT NULL | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL | Last update timestamp |

### 2.2 Relationships
- **User** can own multiple Customers (1:N)
- **User** can own multiple Deals (1:N)
- **Customer** belongs to exactly one User (N:1)
- **Customer** can have multiple Contacts (1:N)
- **Customer** can have multiple Deals (1:N)
- **Customer** can have multiple Activities (1:N)
- **Deal** belongs to exactly one Customer (N:1)
- **Deal** belongs to exactly one User (N:1)
- **Deal** can have multiple Activities (1:N)
- **Activity** is always linked to a Customer and optionally to a Deal

## 3. Functional Requirements and Business Logic

### 3.1 Access Management and Permissions
* **Manager Role:**
  - Can view, create, update, and delete their own Customers (where `customer.owner_id = current_user.id`)
  - Can view, create, update, and delete their own Deals
  - Can view, create, and delete Activities linked to their own Customers
  - Cannot view or modify Customers, Deals, or Activities owned by other managers
  - Can view all Contacts belonging to their own Customers
  
* **Admin Role:**
  - Can view, create, update, and delete all Customers, Deals, Activities, and Contacts
  - Can reassign ownership of Customers and Deals to other managers
  - Can view analytics for all managers
  - Can manage User accounts

* **Unauthenticated Users:**
  - No access to any resources. Must log in first.

### 3.2 Client Base Management
* **CRUD Operations for Customers:**
  - Create: Managers can create a new Customer; `owner_id` is set to the current user automatically
  - Read: Managers can view only their own Customers; Admins can view all
  - Update: Managers can update only their own Customers (name, industry, phone, email, address)
  - Delete: Managers can delete only their own Customers (soft delete recommended to preserve history)

* **CRUD Operations for Contacts:**
  - Create: Only if the associated Customer is owned by the current user (Manager) or user is Admin
  - Read: Contacts are visible to the manager who owns the Customer, or to Admins
  - Update: Only the owning manager or an Admin can update a Contact
  - Delete: Only the owning manager or an Admin can delete a Contact

### 3.3 Sales Pipeline
* **Deal Status Flow:** Strictly follows the pipeline: `New` → `Qualified` → `Proposal` → `Negotiation` → `Won` / `Lost`
  - Status can only move forward or to final states (Won/Lost)
  - A deal cannot revert to an earlier status
  - Only an Admin or the owning manager can change deal status
  - When a deal is marked Won or Lost, set `closed_at` timestamp

* **Deal Constraints:**
  - Amount must be > 0
  - Probability must be an integer between 0 and 100
  - Expected close date must be in the future when deal is created
  - A deal must always be linked to a valid Customer and User (manager)

### 3.4 Search and Filtering
* **Customer Search:**
  - Searchable fields: name, industry, email, phone
  - Search is case-insensitive
  - Results are paginated (default: 20 per page, max 100)
  - Managers see only their own Customers; Admins see all
  
* **Deal Filtering:**
  - Filter by: status, owner (manager), customer, probability range, amount range, date range
  - Managers see only their own Deals; Admins see all
  - Results are paginated (default: 20 per page, max 100)

* **Activity Filtering:**
  - Filter by: activity_type, associated customer, associated deal, date range
  - Managers see only activities linked to their own Customers
  - Results are sorted by `created_at` (newest first)

## 4. Analytics Dashboard

To fulfill the mathematical component of the coursework, the dashboard displays metrics calculated as follows:

* **Total Customers:** Count of all Customers owned by the current user (Managers see their own; Admins see all)

* **Total Value of Open Deals:** Sum of all Deal amounts where `status != 'Won'` and `status != 'Lost'`, filtered to the current user's Deals

* **Distribution of Deals by Pipeline Status:** Count of Deals per status (New, Qualified, Proposal, Negotiation, Won, Lost) for the current user

* **Expected Revenue:** 
  - Formula: $\sum (\text{Deal Amount} \times \frac{\text{Probability}}{100})$
  - Calculated only for open deals (status != 'Won' and status != 'Lost')
  - Filtered to the current user's Deals

* **Win Rate (Conversion Statistics):**
  - Formula: $\frac{\text{Number of Won Deals}}{\text{Number of Won Deals} + \text{Number of Lost Deals}} \times 100\%$
  - Only considers closed deals (status = 'Won' or status = 'Lost')
  - If no closed deals exist, display "N/A"
  - Filtered to the current user's Deals

* **Dashboard Scope:**
  - All metrics refresh on page load
  - Managers see metrics for their own Deals only
  - Admins see metrics for all Deals or can filter by specific manager

## 5. User Stories and Acceptance Criteria

### 5.1 User Story 1: Dashboard Summary
**As a** Manager  
**I want to** view summary statistics for my own deals on the dashboard  
**So that** I can quickly understand my sales pipeline health and expected revenue

**Acceptance Criteria:**
- Given a Manager is logged in, when they navigate to the Dashboard, then they see:
  - Total number of their Customers
  - Total value of their open Deals
  - Distribution chart showing count of Deals per status
  - Expected Revenue (sum of deal_amount × probability/100 for open deals)
  - Win Rate percentage (or "N/A" if no closed deals exist)
- Given a Manager has no Deals, when they view the Dashboard, then all metrics display zero or "N/A"
- Given a Manager has both Won and Lost deals, when they view the Dashboard, then Win Rate is calculated as: Won / (Won + Lost) × 100%

### 5.2 User Story 2: Create Customer and Contact
**As a** Manager  
**I want to** create a new Customer record and add a Contact for negotiation  
**So that** I can organize my interactions with new companies

**Acceptance Criteria:**
- Given a Manager is on the Customer creation page, when they fill in the required fields (Company name, email, phone) and click "Save", then:
  - A new Customer is created with owner_id set to the current Manager
  - The Customer appears in the Manager's Customer list
  - Optional fields (industry, address) can be left blank
- Given a Customer has been created, when a Manager navigates to the Customer details page, then they can add a Contact by providing:
  - First name (required)
  - Last name (required)
  - Job title (optional)
  - Email (optional, must be unique per Customer)
  - Phone (optional)
- Given a Manager clicks "Save Contact", when the contact data is valid, then the Contact is created and linked to the Customer
- Given a Manager is not the owner of a Customer, when they try to create a Contact for that Customer, then access is denied and an error message is shown

### 5.3 User Story 3: Create and Initialize a Deal
**As a** Manager  
**I want to** open a Deal with initial budget and success probability  
**So that** I can track potential revenue from new sales opportunities

**Acceptance Criteria:**
- Given a Manager is viewing a Customer, when they click "Create Deal", then a form appears with fields:
  - Deal title (required)
  - Amount in currency (required, must be > 0)
  - Initial probability percentage (required, 0–100)
  - Expected close date (required, must be in the future)
  - Deal status is automatically set to `New`
- Given a Manager completes the form and clicks "Save Deal", when all validations pass, then:
  - The Deal is created and linked to the Customer and the Manager
  - The Deal appears in the Manager's Deal list with status `New`
  - The Deal amount and probability are displayed correctly
- Given a Manager enters an invalid amount (≤ 0) or an invalid probability (< 0 or > 100), when they click "Save Deal", then an error message is shown and the Deal is not created
- Given a Manager enters a close date in the past, when they click "Save Deal", then an error message is shown

### 5.4 User Story 4: Log Activity and Update Deal Status
**As a** Manager  
**I want to** log activity (meeting notes) and move a deal to the next pipeline stage  
**So that** I can track progress and update success probability

**Acceptance Criteria:**
- Given a Manager is viewing a Deal, when they click "Add Activity", then a form appears with fields:
  - Activity type (Call, Meeting, Email, Note) — required
  - Title (required)
  - Description (optional)
  - Scheduled date/time (optional, for future activities)
- Given a Manager completes the Activity form and clicks "Save", then:
  - The Activity is created and linked to the Customer and Deal
  - The Activity appears in the Activity log, sorted by creation date (newest first)
- Given a Manager is on the Deal detail page, when they click "Change Status", then a dropdown appears showing only valid next statuses (according to the pipeline)
  - Example: if Deal status is `New`, only `Qualified` is available
  - From `Negotiation`, both `Won` and `Lost` are available
- Given a Manager changes a Deal status and clicks "Save", when the transition is valid, then:
  - The Deal status is updated
  - If the status is `Won` or `Lost`, the `closed_at` timestamp is set
  - An Activity log entry records the status change
- Given a Manager updates a Deal, when they edit the probability percentage, then:
  - The new probability must be between 0 and 100
  - The Expected Revenue is recalculated on the Dashboard
## 6. Data Validation Rules

All inputs must be validated on both client (Vue 3) and server (FastAPI) sides.

**User Entity:**
- Email must be a valid email format and unique across all Users
- Password must be at least 8 characters long
- Full name must not be empty and must be <= 255 characters
- Role must be one of: 'Manager', 'Admin'

**Customer Entity:**
- Name is required and must be 1–255 characters
- Owner_id must reference a valid User
- Phone (if provided) must match a valid phone format
- Email (if provided) must be a valid email format

**Contact Entity:**
- First name and last name are required and must each be 1–100 characters
- Email must be unique per Customer (if provided)
- Phone (if provided) must match a valid phone format

**Deal Entity:**
- Title is required and must be 1–255 characters
- Amount must be a positive decimal > 0, max 999,999,999.99
- Probability must be an integer in the range [0, 100]
- Status must be one of: 'New', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost'
- Expected close date must be a future date (or today)
- Customer and User references must point to valid, existing records
- Only the owning Manager or an Admin can update a Deal

**Activity Entity:**
- Activity type must be one of: 'Call', 'Meeting', 'Email', 'Note'
- Title is required and must be 1–255 characters
- Customer and Deal references must point to valid, existing records
- Scheduled date (if provided) must not be in the past

**General Validation:**
- All timestamps (created_at, updated_at, closed_at) are auto-generated server-side
- All IDs are UUIDs and auto-generated server-side
- Soft deletes: Deleted records are marked with a `deleted_at` timestamp and excluded from queries (optional for MVP, but recommended for data integrity)

## 7. Non-Functional Requirements

### 7.1 Security
- All API endpoints require authentication (JWT or session-based)
- Passwords must be hashed using bcrypt or similar secure algorithm
- HTTPS must be used in production
- API responses must not leak sensitive data (e.g., password hashes)
- Authorization checks must be enforced on all endpoints (Manager can only access their own data unless they are Admin)
- Input validation and sanitization on all endpoints to prevent SQL injection and XSS attacks

### 7.2 Performance
- API response time for list endpoints (GET) must be < 500ms for <= 1000 records
- Dashboard metrics must load within 1 second
- Database queries must use appropriate indexes on foreign keys and frequently filtered fields
- Search queries on Customers and Deals must support pagination to prevent large result sets

### 7.3 Data Integrity and Persistence
- Database migrations must version control all schema changes
- Cascading deletes: Deleting a Customer should not cascade-delete Deals or Activities (implement soft deletes or explicit cleanup logic)
- Foreign key constraints must be enforced at the database level
- Transactional consistency: Deal status updates and Activity logging should be atomic

### 7.4 Usability and User Experience
- Form validation errors must be displayed to the user in real-time (client-side) and confirmed server-side
- The UI should prevent invalid actions (e.g., disable status buttons that are not allowed)
- The Dashboard should auto-refresh on page load and optionally on data changes
- All dates/times must be displayed in the user's local timezone (or a configurable timezone)

### 7.5 Logging and Debugging
- All API requests and errors should be logged with timestamp, user ID, endpoint, and response code
- Failed authentication/authorization attempts must be logged
- Database errors should be logged server-side (but not exposed to the client as detailed error messages)

### 7.6 Deployment and Maintenance
- The application must support Docker containerization for ease of deployment
- Environment variables must configure database connection, API base URL, and JWT secrets
- Database migrations must be runnable on application startup (or manually)
- A simple README or deployment guide should document how to set up and run the MVP locally and in production