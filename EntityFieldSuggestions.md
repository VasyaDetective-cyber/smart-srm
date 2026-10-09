**Review of Entity Field Definitions**

### High-priority issues

1. **Customer required fields conflict with the schema**

The acceptance criteria require company name, email, and phone during customer creation, but the field definition marks `email` and `phone` as optional at `REQUIREMENTS.md:31-36`.

Suggestion: choose one rule and apply it consistently. If required for the MVP:

```text
phone | VARCHAR(20) | NOT NULL | Company phone
email | VARCHAR(255) | NOT NULL | Company email
```

If they are genuinely optional, remove them from the required creation criteria.

2. **Ownership must be restricted to managers**

`Customer.owner_id` and `Deal.owner_id` reference `User`, but the definition does not ensure that the referenced user has the `Manager` role (`REQUIREMENTS.md:32`, `REQUIREMENTS.md:58`).

Suggestion: state that ownership must reference an active Manager. Admins may own records administratively, but should not normally be selectable as sales owners.

3. **Activity access and audit ownership are underspecified**

Activities rely on `customer_id` for authorization, but there is no `created_by` or `author_id`. This makes it impossible to identify which user logged an activity or audit status-change entries.

Suggestion: add:

```text
created_by_id | UUID | FK, NOT NULL | User who created the activity
```

Also clarify whether activities may be edited. The permissions allow creation and deletion for Managers but do not explicitly allow updates.

4. **Activity-to-deal consistency is not enforceable from the current fields**

An Activity can contain a `customer_id` and an unrelated `deal_id`. The schema must ensure that the deal belongs to the same customer.

Suggestion: add a business rule:

```text
If deal_id is provided, deal.customer_id must equal activity.customer_id.
```

This should be enforced transactionally or with a composite foreign key.

5. **Deal status rules require more than an ENUM**

The status ENUM defines allowed values but cannot enforce the permitted progression (`REQUIREMENTS.md:62-66`). It also does not guarantee that:

- `closed_at` is set only for `Won` or `Lost`
- closed deals cannot be reopened
- status transitions are forward-only

Suggestion: explicitly require service-layer validation and database checks where possible. Consider a `deal_status_history` table if status changes need to be audited independently of Activities.

### Important improvements

6. **`DECIMAL(15,2)` does not match the stated maximum**

The validation rules specify a maximum of `999,999,999.99`, but `DECIMAL(15,2)` permits a much larger value (`REQUIREMENTS.md:60-61`, `REQUIREMENTS.md:281-284`).

Suggestion: use `DECIMAL(11,2)` or add:

```text
CHECK (amount > 0 AND amount <= 999999999.99)
```

Also add a `currency_code` field if multiple currencies may ever be supported.

7. **Date requirements are inconsistent**

The field definition says expected close date must be in the future, while validation allows today (`REQUIREMENTS.md:64`, `REQUIREMENTS.md:283-285`).

Suggestion: standardize on “today or a future date” and enforce it in the API. Database checks involving the current date may be database-specific.

8. **Soft deletion is missing from the entity definitions**

Soft deletes are recommended later, but no entity has a `deleted_at` field (`REQUIREMENTS.md:293-295`).

Suggestion: add `deleted_at TIMESTAMP NULL` to Customer, Contact, Deal, and Activity, and define uniqueness and foreign-key behavior for deleted records.

9. **Foreign-key deletion behavior is undefined**

The requirements prohibit cascading deletion from Customer to Deal or Activity, but the field definitions do not specify `ON DELETE` behavior.

Suggestion:

- Use soft deletion for Customer, Deal, Contact, and Activity.
- Use `RESTRICT` or `NO ACTION` for critical foreign keys.
- Explicitly state that physical Customer deletion is blocked while dependent records exist.

10. **Timestamps should be timezone-aware and automatically managed**

All timestamps are described only as `TIMESTAMP`, without defaults or update behavior (`REQUIREMENTS.md:24-25`).

Suggestion:

```text
created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now()
updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now()
```

Specify that `updated_at` is updated automatically and `closed_at` is server-generated.

### Lower-priority consistency improvements

- Make User email uniqueness case-insensitive, usually by normalizing to lowercase or using a functional unique index.
- Make Contact uniqueness explicitly composite: `(customer_id, email)`, with defined behavior for multiple `NULL` emails.
- Add indexes for `owner_id`, `customer_id`, `deal_id`, `status`, `created_at`, and searchable customer fields.
- Clarify whether `scheduled_date` represents the planned time or the actual activity time. Historical activities may legitimately have a past occurrence date.
- Add minimum and maximum length constraints for text fields, not only application-level validation.
- Add a database check that `probability` is between `0` and `100`.
- Add a database check that `closed_at IS NULL` for open deals and is non-null for `Won` or `Lost`.
- Clarify whether deleting a User is allowed. Since Customers and Deals require an owner, users should likely be deactivated rather than physically deleted.

Overall, the definitions are a good starting point, but the most important corrections are the Customer required-field contradiction, ownership-role enforcement, activity auditability, deal amount precision, and soft-delete/foreign-key behavior.