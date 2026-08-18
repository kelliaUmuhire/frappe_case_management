"""Scheduled jobs. Registered in hooks.py under scheduler_events."""

import frappe
from frappe.utils import add_days, getdate, today

OPEN_WORKFLOW_STATES = ("Open", "Assigned", "In Progress", "Pending")
APPROACHING_WINDOW_DAYS = 2


def check_overdue_cases() -> None:
	"""Daily job: recompute each open Case's SLA status from target_resolution_date,
	and raise a Notification Log for the assigned officer the moment a case tips
	over into Overdue.
	"""
	today_date = getdate(today())
	cases = frappe.get_all(
		"Case",
		filters={"workflow_state": ["in", OPEN_WORKFLOW_STATES]},
		fields=["name", "target_resolution_date", "sla_status", "assigned_officer"],
	)

	for case in cases:
		if not case.target_resolution_date:
			continue

		target = getdate(case.target_resolution_date)
		if target < today_date:
			new_status = "Overdue"
		elif target <= add_days(today_date, APPROACHING_WINDOW_DAYS):
			new_status = "Approaching Deadline"
		else:
			new_status = "On Track"

		if new_status == case.sla_status:
			continue

		frappe.db.set_value("Case", case.name, "sla_status", new_status)

		if new_status == "Overdue" and case.assigned_officer:
			_notify_overdue(case.name, case.assigned_officer)

	frappe.db.commit()


def _notify_overdue(case_name: str, assigned_officer: str) -> None:
	frappe.get_doc({
		"doctype": "Notification Log",
		"for_user": assigned_officer,
		"type": "Alert",
		"subject": f"Case {case_name} is now overdue",
		"document_type": "Case",
		"document_name": case_name,
	}).insert(ignore_permissions=True)
