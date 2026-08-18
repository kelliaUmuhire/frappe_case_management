import frappe
from frappe.tests import IntegrationTestCase

from case_management.case_management.api import assign_case


def _ensure_user(email, role):
	if not frappe.db.exists("User", email):
		user = frappe.get_doc({
			"doctype": "User",
			"email": email,
			"first_name": email.split("@")[0],
			"send_welcome_email": 0,
		})
		user.append("roles", {"role": role})
		user.insert(ignore_permissions=True)
	elif not frappe.db.exists("Has Role", {"parent": email, "role": role}):
		user = frappe.get_doc("User", email)
		user.append("roles", {"role": role})
		user.save(ignore_permissions=True)
	return email


class TestAssignCaseAPI(IntegrationTestCase):
	def setUp(self):
		self.officer = _ensure_user("officer.test@example.com", "Case Officer")
		self.other_officer = _ensure_user("officer2.test@example.com", "Case Officer")
		self.supervisor = _ensure_user("supervisor.test@example.com", "Supervisor")

		self.person = frappe.db.get_value("Person", {"first_name": "API", "last_name": "Tester"})
		if not self.person:
			self.person = frappe.get_doc({
				"doctype": "Person", "first_name": "API", "last_name": "Tester",
			}).insert(ignore_permissions=True).name

		case_doc = frappe.get_doc({
			"doctype": "Case",
			"title": "API assignment test",
			"case_type": "Inquiry",
			"priority": "Medium",
			"person": self.person,
			"description": "Created by automated test.",
		})
		case_doc.insert(ignore_permissions=True)
		# Set the workflow state to Open to match the expected initial state for the API tests
		frappe.db.set_value("Case", case_doc.name, "workflow_state", "Open")
		self.case = case_doc.name

	def tearDown(self):
		frappe.set_user("Administrator")

	def test_non_supervisor_cannot_assign(self):
		frappe.set_user(self.officer)
		self.assertRaises(frappe.PermissionError, assign_case, self.case, self.other_officer)

	def test_supervisor_can_assign_and_case_moves_to_assigned(self):
		frappe.set_user(self.supervisor)
		result = assign_case(self.case, self.officer)
		self.assertTrue(result["success"])
		self.assertEqual(result["case_status"], "Assigned")
		self.assertEqual(
			frappe.db.get_value("Case", self.case, "assigned_officer"), self.officer
		)

	def test_cannot_assign_to_user_without_case_officer_role(self):
		frappe.set_user(self.supervisor)
		self.assertRaises(frappe.ValidationError, assign_case, self.case, self.supervisor)

	def test_cannot_assign_closed_case(self):
		frappe.set_user(self.supervisor)
		frappe.db.set_value("Case", self.case, "workflow_state", "Closed")
		self.assertRaises(frappe.ValidationError, assign_case, self.case, self.officer)
