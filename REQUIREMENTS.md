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

## 3. Functional Requirements and Business Logic
* **Access Management:** Managers have access only to their own clients and deals.
* **Client Base:** CRUD operations for companies and their contacts.
* **Sales Pipeline:** A strictly defined pipeline of deal statuses: `New` → `Qualified` → `Proposal` → `Negotiation` → `Won` / `Lost`.
* **Search and Filtering** for clients and deals.

## 4. Analytics Dashboard
To fulfill the mathematical component of the coursework, the dashboard includes:
* Total count of clients and the total value of open deals.
* Distribution of deals by pipeline status.
* Expected Revenue calculation using the formula: `Deal Amount × Probability`.
* Conversion statistics (Win Rate) based on closed deals using the formula: `Won / (Won + Lost)`.

## 5. Main Use Cases
1. A manager logs into the system and views summary statistics for their own deals on the dashboard.
2. A manager creates a new Customer record and adds a Contact for the person they are negotiating with.
3. A manager opens a Deal (status `New`), sets the deal budget, and initial success probability.
4. After a meeting, the manager logs the outcome in Activity, moves the deal to the `Negotiation` stage, and updates the probability percentage.