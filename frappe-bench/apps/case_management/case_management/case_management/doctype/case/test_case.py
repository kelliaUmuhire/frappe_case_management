import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, getdate


class TestCase(IntegrationTestCase):
	def setUp(self):
		self.person = frappe.db.get_value("Person", {"first_name": "SLA", "last_name": "Tester"})
		if not self.person:
			self.person = frappe.get_doc({
				"doctype": "Person",
				"first_name": "SLA",
				"last_name": "Tester",
			}).insert(ignore_permissions=True).name

	def _make_case(self, priority):
		return frappe.get_doc({
			"doctype": "Case",
			"title": f"{priority} priority SLA test",
			"case_type": "Inquiry",
			"priority": priority,
			"person": self.person,
			"description": "Created by automated test.",
		}).insert(ignore_permissions=True)

	def test_target_resolution_date_for_each_priority(self):
		expected_days = {"Critical": 1, "High": 3, "Medium": 7, "Low": 14}
		for priority, days in expected_days.items():
			case = self._make_case(priority)
			self.assertEqual(
				case.target_resolution_date,
				add_days(getdate(case.opened_date), days),
				msg=f"Wrong SLA deadline for {priority} priority",
			)

	def test_highly_restricted_case_requires_assigned_officer(self):
		case = frappe.get_doc({
			"doctype": "Case",
			"title": "Highly restricted without an officer",
			"case_type": "Inquiry",
			"priority": "Medium",
			"person": self.person,
			"confidentiality_level": "Highly Restricted",
			"description": "Should be rejected by validate().",
		})
		self.assertRaises(frappe.ValidationError, case.insert, ignore_permissions=True)
