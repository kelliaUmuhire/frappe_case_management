# Security

- **Role-based access**: Case Officer / Supervisor / System Manager, enforced via each DocType's `permissions` array (see the DocType JSON files) — not just hidden in the UI.
- **Row-level enforcement**: DocType permissions alone can't express "only see cases assigned to you" — that's handled server-side in `case_management/permissions.py` via `permission_query_conditions` (filters list/report views) and `has_permission` (blocks direct access to a single record), registered in `hooks.py`. This applies even to direct REST API calls, not just Desk.
- **Server-side validation always, never trust the client**: workflow transitions are enforced by Frappe's Workflow engine (server-side), and `Case.validate()` / `Assignment.validate()` re-check business rules (Highly Restricted needs an officer; can't touch a Closed case) regardless of what the client sent.
- **Custom API defense-in-depth**: `assign_case` re-checks the caller's role itself rather than relying solely on whitelisting — whitelisting controls *who can call the function at all*, not *what they're allowed to do inside it*.
- **Secrets**: DB/Redis credentials and `ADMIN_PASSWORD` come from environment variables (`.env`, not committed) in both the devcontainer and production compose — never hardcoded.
- **Synthetic data only**: every fixture, test record, and demo dataset in this repo is fabricated. No real personal or case data, ever — this is a portfolio project, not a deployed system handling real cases.
- **Logging**: no case content, confidentiality-flagged fields, or credentials should appear in application logs — worth an explicit check before the demo/screenshot pass in Phase 7.

## What's deliberately out of scope

OIDC/SSO, encryption-at-rest configuration, network-level hardening (TLS termination, WAF), and audit-log retention policy are all real production concerns this project doesn't implement — see "What NOT to Build Initially" in the project plan. Worth naming explicitly in the interview as scoped-out rather than overlooked.
