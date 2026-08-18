import frappe
from frappe.tests import IntegrationTestCase


class TestAssignment(IntegrationTestCase):
	def setUp(self):
		self.person = frappe.db.get_value("Person", {"first_name": "Assign", "last_name": "Tester"})
		if not self.person:
			self.person = frappe.get_doc({
				"doctype": "Person", "first_name": "Assign", "last_name": "Tester",
			}).insert(ignore_permissions=True).name

		if not frappe.db.exists("User", "assignment.officer@example.com"):
			frappe.get_doc({
				"doctype": "User",
				"email": "assignment.officer@example.com",
				"first_name": "Assignment",
				"send_welcome_email": 0,
				"roles": [{"role": "Case Officer"}],
			}).insert(ignore_permissions=True)

		self.case = frappe.get_doc({
			"doctype": "Case",
			"title": "Assignment sync test",
			"case_type": "Inquiry",
			"priority": "Medium",
			"person": self.person,
			"description": "Created by automated test.",
		}).insert(ignore_permissions=True).name

	def test_assignment_syncs_assigned_officer_onto_case(self):
		frappe.get_doc({
			"doctype": "Assignment",
			"case": self.case,
			"assigned_user": "assignment.officer@example.com",
			"role": "Primary Officer",
		}).insert(ignore_permissions=True)

		self.assertEqual(
			frappe.db.get_value("Case", self.case, "assigned_officer"),
			"assignment.officer@example.com",
		)

	def test_assignment_creates_case_activity_entry(self):
		before = frappe.db.count("Case Activity", {"case": self.case, "activity_type": "Assignment Change"})
		frappe.get_doc({
			"doctype": "Assignment",
			"case": self.case,
			"assigned_user": "assignment.officer@example.com",
			"role": "Reviewer",
		}).insert(ignore_permissions=True)
		after = frappe.db.count("Case Activity", {"case": self.case, "activity_type": "Assignment Change"})
		self.assertEqual(after, before + 1)

	def test_cannot_assign_to_closed_case(self):
		frappe.db.set_value("Case", self.case, "workflow_state", "Closed")
		doc = frappe.get_doc({
			"doctype": "Assignment",
			"case": self.case,
			"assigned_user": "assignment.officer@example.com",
			"role": "Primary Officer",
		})
		self.assertRaises(frappe.ValidationError, doc.insert, ignore_permissions=True)
