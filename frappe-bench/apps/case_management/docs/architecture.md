# Architecture

## Overview

```
Browser
  |
  v
Frontend (nginx) --- Websocket (Socket.IO)
  |
  v
Backend (Frappe/gunicorn)
  |
  +---- MariaDB          (single source of truth for all DocTypes)
  |
  +---- Redis (cache)    (page cache, session cache)
  |
  +---- Redis (queue)    (background job queue + pub/sub for websocket)
  |
  +---- Background workers (queue-short, queue-long)
  |
  +---- Scheduler        (daily SLA sweep — see case_management/tasks.py)
```

## Why Frappe

Frappe gives DocType-driven CRUD, role-based permissions, a workflow engine, and a REST API essentially for free, so the actual engineering effort goes into the domain model, business rules, and the custom UI — not re-building an ORM, admin panel, and auth layer from scratch. The trade-off, honestly: less flexibility than a bespoke stack, and a real learning curve on Frappe-specific conventions (naming rules, hooks, the permission system) if you haven't used it before.

## How the DocTypes map to the domain

`Case` is the aggregate root — everything else exists to describe or act on a Case. `Person` and `Organization` are reference data. `Case Activity`, `Assignment`, and `Case Note` are all deliberately standalone DocTypes linked to Case rather than child tables, trading a bit of simplicity for independent list views, independent permission rules, and independent reporting (see the design note in `02-data-model-and-design.md`).

## Where logic lives, and why

- **DocType JSON**: field shape, mandatory/read-only flags, default values (e.g. `Case Activity.actor` defaults to `session:user` — no code needed for that).
- **Controllers (`*.py` per DocType)**: logic that only concerns that one document — Case's SLA date calculation, Assignment's "don't touch a Closed case" guard.
- **`permissions.py`**: cross-cutting row-level rules (which Cases a Case Officer can see) that don't belong to any single document.
- **`tasks.py`**: time-driven logic (the daily overdue sweep) that isn't triggered by a user action at all.
- **`api.py`**: logic that spans multiple DocTypes in one transaction (assigning = create Assignment + update Case + log Activity), exposed as a single atomic operation rather than three separate REST calls a client would have to sequence and error-handle itself.

## Database

MariaDB, one table per DocType (`tabCase`, `tabPerson`, ...), managed entirely through Frappe's ORM — no hand-written migrations; `bench migrate` diffs the DocType JSON against the live schema and applies `ALTER TABLE`s.
