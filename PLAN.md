### CRM MVP Scope

The MVP is a lightweight web-based CRM that allows a user to manage customers, contacts, deals, and basic sales activities. The goal is not to reproduce a commercial CRM, but to demonstrate a complete client-server application built with **Python, FastAPI, Vue 3, JavaScript, Bootstrap, SQLAlchemy, and PostgreSQL**.

The MVP should support user authentication, customer management, contact information, deal tracking, search and filtering, and a small analytical dashboard.

The core data model can consist of `User`, `Customer`, `Contact`, `Deal`, and `Activity`. A customer can have several contacts and deals. A deal should contain an amount, status, probability, creation date, and expected closing date. Activities can represent calls, meetings, emails, or notes associated with a customer.

The dashboard should provide simple CRM analytics such as the number of customers, number and value of active deals, deals by status, expected revenue calculated as `Deal Amount × Probability`, and basic conversion statistics. This analytical component is particularly relevant for an Applied Mathematics course project.

Features such as email integration, notifications, advanced permissions, AI functionality, complex forecasting, mobile applications, and third-party integrations should remain outside the MVP.

### Weekly MVP Development Plan

| Week           | Dates        | Focus                           | Expected Result                                                                           |
| -------------- | ------------ | ------------------------------- | ----------------------------------------------------------------------------------------- |
| **1**          | Sep 22-27    | Requirements and MVP definition | Final feature list, use cases, entities, project scope                                    |
| **2**          | Sep 28-Oct 4 | System and database design      | Architecture diagram, ER diagram, database schema                                         |
| **3**          | Oct 5-11     | Backend setup                   | FastAPI project, PostgreSQL connection, SQLAlchemy configuration, basic project structure |
| **4**          | Oct 12-18    | Customer API                    | Customer model and CRUD endpoints implemented and tested                                  |
| **5**          | Oct 19-25    | Contacts and relationships      | Contact CRUD, Customer-Contact relationship, API validation                               |
| **6**          | Oct 26-Nov 1 | Deal management                 | Deal model, statuses, amounts, probabilities, Customer-Deal relationship                  |
| **7**          | Nov 2-8      | Authentication                  | User model, login, password hashing, JWT-based authentication, protected API endpoints    |
| **8**          | Nov 9-15     | Frontend foundation             | Vue 3 project, Bootstrap, Vue Router, API communication, Login page, main navigation      |
| **9**          | Nov 16-22    | Customer UI                     | Customer list, search, Add/Edit/Delete forms, Customer Details page                       |
| **10**         | Nov 23-29    | Contacts and Deals UI           | Contact management and deal management integrated with backend                            |
| **11**         | Nov 30-Dec 6 | Activities and filtering        | Customer activities/notes, deal filtering by status, customer search                      |
| **12**         | Dec 7-13     | CRM analytics                   | Backend aggregation endpoints, expected revenue and conversion calculations               |
| **13**         | Dec 14-20    | Dashboard and integration       | Dashboard with KPI cards, simple charts, complete frontend-backend integration            |
| **14**         | Dec 21-27    | Testing and stabilization       | API tests, validation, error handling, UI fixes, end-to-end testing                       |
| **Final days** | Dec 28-Jan 1 | Release preparation             | Deployment, database initialization, demo data, README, screenshots, final MVP            |

### MVP milestone structure

By **November 1**, the backend should already represent a usable CRM API. By **November 29**, you should have a working full-stack application where customers, contacts, and deals can be managed through the browser. By **December 13**, all required functionality should be complete.

This is important because I would **not plan new functionality after December 13**. The remaining 2.5 weeks should be treated as a stabilization and release period rather than development time. This gives you some protection against integration problems, deployment issues, university workload, and underestimated tasks.

The **January 1 MVP** can therefore be considered successful when a user can log in, create and edit customers, maintain their contacts, create and track deals, record basic activities, search/filter CRM data, and view basic sales analytics on a dashboard.

For an Applied Mathematics student, I would then make **analytical development the post-MVP direction**. For example, the next version could introduce a mathematically defined customer/deal scoring model and later compare it with a simple ML-based prediction model. That creates a natural path from a relatively ordinary CRM course project toward a project with a clear Applied Mathematics component.
