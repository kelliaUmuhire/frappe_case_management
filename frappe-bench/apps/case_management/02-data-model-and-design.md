# Case Management System — Data Model, Workflow, Permissions & API Design

Status: DRAFT for review. Lock this before creating DocTypes in Frappe (Phase 2).

## 1. User Stories (minimum set to build against)

1. As a **Case Officer**, I can create a new Case for a Person so that a record exists to track their request.
2. As a **Case Officer**, I can log Case Activities and Notes against my assigned Cases so there's a running history.
3. As a **Case Officer**, I can move a Case through the normal workflow states (Open → Assigned → In Progress → Pending → Resolved) for cases assigned to me.
4. As a **Supervisor**, I can assign or reassign any Case to a Case Officer.
5. As a **Supervisor**, I can approve higher-level transitions (e.g. Resolved → Closed, Closed → Reopened).
6. As a **Supervisor**, I can view all cases and see SLA/overdue state on a dashboard.
7. As any authenticated role, I cannot read or edit a Case I'm not assigned to and don't have elevated permissions for.
8. As an external system, I can call a REST/API endpoint to assign a case and receive a structured success/failure response.

## 2. DocType Field Specifications

### Person
| Field | Fieldname | Type | Notes |
|---|---|---|---|
| First Name | `first_name` | Data | Mandatory |
| Last Name | `last_name` | Data | |
| Date of Birth | `date_of_birth` | Date | |
| Gender | `gender` | Select | Male / Female / Other / Prefer not to say |
| Contact Number | `contact_number` | Data (Phone) | |
| Email | `email` | Data (Email) | |
| Preferred Language | `preferred_language` | Select | Small fixed list to start |
| Location | `location` | Small Text | Free text, not geocoded in MVP |
| Notes | `notes` | Text | |

Naming: `PERS-.#####` (auto-increment series).

### Case (central DocType, Workflow-controlled)
| Field | Fieldname | Type | Notes |
|---|---|---|---|
| Title | `title` | Data | Mandatory |
| Case Type | `case_type` | Select | Support Request / Inquiry / Follow-up / Incident Report / Other |
| Priority | `priority` | Select | Critical / High / Medium / Low — drives SLA |
| Status | `workflow_state` | Link (Workflow State) | Managed by the Workflow, not set directly by users |
| Person | `person` | Link → Person | Mandatory |
| Assigned Officer | `assigned_officer` | Link → User | Set via Assignment logic, not typed directly |
| Opened Date | `opened_date` | Date | Default: Today, read-only after creation |
| Target Resolution Date | `target_resolution_date` | Date | **Calculated server-side** from `priority` + `opened_date` |
| Description | `description` | Text Editor | |
| Confidentiality Level | `confidentiality_level` | Select | Standard / Restricted / Highly Restricted |

Naming: `CASE-.YYYY.-.#####`.

### Case Activity (standalone DocType, not a child table — see design note below)
| Field | Fieldname | Type | Notes |
|---|---|---|---|
| Case | `case` | Link → Case | Mandatory |
| Activity Type | `activity_type` | Select | Call / Visit / Email / Internal Review / Assignment Change / Status Change / Note |
| Date | `date` | Datetime | Default: Now |
| Actor | `actor` | Link → User | Default: current user |
| Notes | `notes` | Text | |
| Next Action | `next_action` | Data | |
| Due Date | `due_date` | Date | |

> **Design note (interview talking point):** the plan allowed either a child table or a linked DocType here. Going with a standalone linked DocType instead of a child table trades a bit of simplicity for: independent list views/filtering, its own permission rules (e.g. restricting who sees Internal Review entries), and the ability to report on activity volume/type across cases — none of which a child table gives you cleanly.

### Organization
| Field | Fieldname | Type | Notes |
|---|---|---|---|
| Name | `organization_name` | Data | Mandatory |
| Type | `type` | Select | Government / NGO / Partner / Vendor / Other |
| Contact | `contact` | Data | |
| Location | `location` | Small Text | |
| Notes | `notes` | Text | |

### Assignment
| Field | Fieldname | Type | Notes |
|---|---|---|---|
| Case | `case` | Link → Case | Mandatory |
| Assigned User | `assigned_user` | Link → User | Mandatory |
| Assignment Date | `assignment_date` | Date | Default: Today |
| Role | `role` | Select | Primary Officer / Supervisor / Reviewer / Observer |
| Status | `status` | Select | Active / Reassigned / Completed |

### Case Note
| Field | Fieldname | Type | Notes |
|---|---|---|---|
| Case | `case` | Link → Case | Mandatory |
| Note Type | `note_type` | Select | Internal / Confidential / General |
| Content | `content` | Text Editor | |
| Created By | `created_by` | Link → User | Default: current user |
| Created On | `created_on` | Datetime | Default: Now |
| Visible To Role | `visible_to_role` | Link → Role | Used to demonstrate row-level permission separation |

## 3. Workflow

**States:** Draft → Open → Assigned → In Progress → Pending → Resolved → Closed
**Special transition:** Closed → Reopened (goes back to In Progress)

| From | Action | To | Allowed Role |
|---|---|---|---|
| Draft | Submit | Open | Case Officer, Supervisor |
| Open | Assign | Assigned | Supervisor |
| Assigned | Start Work | In Progress | Case Officer (if assigned to self) |
| In Progress | Mark Pending | Pending | Case Officer (if assigned to self) |
| Pending | Resume | In Progress | Case Officer (if assigned to self) |
| In Progress / Pending | Resolve | Resolved | Case Officer (if assigned to self) |
| Resolved | Close | Closed | Supervisor |
| Closed | Reopen | In Progress | Supervisor |

Closed cases are read-only for everyone except System Manager and the explicit Reopen action.

## 4. Roles & Permission Matrix

| DocType | Case Officer | Supervisor | System Manager |
|---|---|---|---|
| Case | Create; Read/Update own assigned only | Create/Read/Update/Delete all | Full |
| Case Activity | Create/Read on own assigned cases | Read/Create all | Full |
| Case Note | Create/Read on own assigned cases (excl. Confidential) | Read/Create all incl. Confidential | Full |
| Assignment | Read only | Create/Read/Update | Full |
| Person | Create/Read | Create/Read/Update | Full |
| Organization | Read | Create/Read/Update | Full |
| Workflow transitions | Normal actions only (per table above) | All transitions incl. Close/Reopen | All |

Enforcement is server-side via Frappe's permission engine (role permissions + `if_owner`/assignment-based restrictions) and re-validated in controller `validate()`/`before_save()` hooks — never trust client-side state alone. This dual enforcement is a good interview point on defense-in-depth.

## 5. SLA Targets (for reference)

| Priority | Target |
|---|---:|
| Critical | 24 hours |
| High | 3 days |
| Medium | 7 days |
| Low | 14 days |

`target_resolution_date` is computed in a Python controller from `opened_date` + this table. A scheduled job (daily, or hourly for Critical) flags cases as **Approaching Deadline** or **Overdue** and can trigger a notification.

## 6. API Design

### Standard REST (Frappe default)
- `GET /api/resource/Case`
- `GET /api/resource/Case/{name}`
- `POST /api/resource/Case`
- `PUT /api/resource/Case/{name}`

### Custom endpoint: assign_case
`POST /api/method/case_management.api.assign_case`

Request body:
```json
{
  "case": "CASE-2026-00001",
  "assign_to": "officer@example.com",
  "role": "Primary Officer"
}
```

Server-side validation before doing anything:
1. Caller has Supervisor or System Manager role (or is the current assigned officer reassigning within their own scope, if we choose to allow that later).
2. Case exists and is not Closed.
3. `assign_to` user has the Case Officer role.
4. No existing Active assignment with the same case+role (or explicitly supersede it).

On success: creates an Assignment record, updates `Case.assigned_officer`, writes a Case Activity entry of type "Assignment Change", and returns:
```json
{
  "success": true,
  "assignment": "ASSIGN-00042",
  "case_status": "Assigned"
}
```
On failure: raises `frappe.PermissionError` or `frappe.ValidationError` with a specific message — never a bare 500.

## 7. Milestones (ordered, not calendar-dated)

1. DocTypes created and linked (no logic yet) — seed demo data
2. Controllers: case-number generation, SLA calculation, validation rules
3. Workflow wired up and manually testable in Desk
4. Roles + permissions applied, verified by testing as each role
5. `assign_case` custom endpoint + standard REST verified via curl/Postman
6. Automated tests for controllers, workflow transitions, and the custom endpoint
7. Vue/Frappe UI dashboard
8. Docker Compose + CI/CD pipeline
9. Documentation + demo data + polish
