"""Row-level permission rules that go beyond what DocType-level role
permissions can express: which specific Case (and Case Note) records a
Case Officer may see, versus a Supervisor/System Manager who sees everything.

Registered in hooks.py under permission_query_conditions / has_permission.
"""

import frappe


def _is_privileged(user: str) -> bool:
	roles = frappe.get_roles(user)
	return user == "Administrator" or "System Manager" in roles or "Supervisor" in roles


def get_case_permission_query_conditions(user: str | None = None) -> str:
	"""Restrict the Case list/report view: Case Officers only see cases
	where they are the assigned officer. Supervisors/System Manager see all.
	"""
	user = user or frappe.session.user
	if _is_privileged(user):
		return ""
	return f"(`tabCase`.assigned_officer = {frappe.db.escape(user)})"


def has_case_permission(doc, ptype: str = "read", user: str | None = None) -> bool:
	user = user or frappe.session.user
	if _is_privileged(user):
		return True
	return doc.assigned_officer == user


def get_case_note_permission_query_conditions(user: str | None = None) -> str:
	"""Case Officers can see General/Internal notes on their own cases, but
	not Confidential notes unless one was explicitly opened up to their role.
	"""
	user = user or frappe.session.user
	if _is_privileged(user):
		return ""
	own_cases = f"""`tabCase Note`.case in (
		select name from `tabCase` where assigned_officer = {frappe.db.escape(user)}
	)"""
	not_confidential = "`tabCase Note`.note_type != 'Confidential'"
	return f"({own_cases} and {not_confidential})"


def has_case_note_permission(doc, ptype: str = "read", user: str | None = None) -> bool:
	user = user or frappe.session.user
	if _is_privileged(user):
		return True
	case_owner = frappe.db.get_value("Case", doc.case, "assigned_officer")
	if doc.note_type == "Confidential":
		return False
	return case_owner == user
