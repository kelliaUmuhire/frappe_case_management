"""Custom whitelisted API methods for the app.

Frappe v16 requires type annotations on whitelisted method parameters
(see require_type_annotated_api_methods in hooks.py) so every public
function here is fully typed.
"""

import frappe


@frappe.whitelist()
def assign_case(case: str, assign_to: str, role: str = "Primary Officer") -> dict:
	"""Assign (or reassign) a Case to a Case Officer.

	POST /api/method/case_management.api.assign_case
	Body: {"case": "CASE-2026-00001", "assign_to": "officer@example.com", "role": "Primary Officer"}

	Only a Supervisor or System Manager may call this. Raises frappe.PermissionError,
	frappe.DoesNotExistError, or frappe.ValidationError with a specific message on failure
	rather than a bare 500.
	"""
	_ensure_caller_is_supervisor()

	if not frappe.db.exists("Case", case):
		frappe.throw(f"Case {case} does not exist.", frappe.DoesNotExistError)

	case_doc = frappe.get_doc("Case", case)
	if case_doc.workflow_state == "Closed":
		frappe.throw(f"Case {case} is Closed and cannot be (re)assigned.")

	if "Case Officer" not in frappe.get_roles(assign_to):
		frappe.throw(f"{assign_to} does not have the Case Officer role.")

	_supersede_existing_active_assignment(case, role)

	assignment = frappe.get_doc({
		"doctype": "Assignment",
		"case": case,
		"assigned_user": assign_to,
		"role": role,
		"status": "Active",
	})
	assignment.insert()

	if case_doc.workflow_state == "Open":
		frappe.db.set_value("Case", case, "workflow_state", "Assigned")

	frappe.db.commit()

	return {
		"success": True,
		"assignment": assignment.name,
		"case_status": frappe.db.get_value("Case", case, "workflow_state"),
	}


def _ensure_caller_is_supervisor() -> None:
	roles = frappe.get_roles(frappe.session.user)
	if "Supervisor" not in roles and "System Manager" not in roles:
		frappe.throw("Only a Supervisor can assign cases.", frappe.PermissionError)


def _supersede_existing_active_assignment(case: str, role: str) -> None:
	existing = frappe.db.exists("Assignment", {"case": case, "role": role, "status": "Active"})
	if existing:
		frappe.db.set_value("Assignment", existing, "status", "Reassigned")
