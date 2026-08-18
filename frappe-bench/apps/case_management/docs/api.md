# API

## Standard REST (Frappe default, no code required)

```
GET    /api/resource/Case
GET    /api/resource/Case/{name}
POST   /api/resource/Case
PUT    /api/resource/Case/{name}
```
Same pattern for Person, Organization, Case Activity, Assignment, Case Note. Filtering/pagination via query params, e.g. `GET /api/resource/Case?filters=[["priority","=","Critical"]]`.

Auth: token-based (`Authorization: token <api_key>:<api_secret>`, generated per-User in Desk) or session cookie if already logged in.

## Custom endpoint: assign_case

```
POST /api/method/case_management.api.assign_case
Content-Type: application/json

{
  "case": "CASE-2026-00001",
  "assign_to": "officer@example.com",
  "role": "Primary Officer"
}
```

Success (200):
```json
{"message": {"success": true, "assignment": "ASSIGN-00042", "case_status": "Assigned"}}
```

Failure modes, all returned as structured errors rather than a bare 500:
| Condition | Exception |
|---|---|
| Caller isn't Supervisor/System Manager | `frappe.PermissionError` (403) |
| Case doesn't exist | `frappe.DoesNotExistError` (404) |
| Case is Closed | `frappe.ValidationError` (417) |
| Target user lacks Case Officer role | `frappe.ValidationError` (417) |

See `case_management/api.py` for the implementation and `case_management/tests/test_api.py` for the behavior under test.
