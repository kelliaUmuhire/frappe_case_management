import frappe
from frappe.model.document import Document


class Assignment(Document):
	def validate(self):
		self.validate_case_not_closed()

	def validate_case_not_closed(self):
		case_status = frappe.db.get_value("Case", self.case, "workflow_state")
		if case_status == "Closed":
			frappe.throw(f"Cannot create or modify an assignment for {self.case} because it is Closed.")

	def after_insert(self):
		if self.status == "Active":
			self.sync_to_case()
		self.log_activity()

	def sync_to_case(self):
		frappe.db.set_value("Case", self.case, "assigned_officer", self.assigned_user)

	def log_activity(self):
		frappe.get_doc({
			"doctype": "Case Activity",
			"case": self.case,
			"activity_type": "Assignment Change",
			"actor": frappe.session.user,
			"notes": f"{self.assigned_user} assigned as {self.role} (assignment {self.name}).",
		}).insert(ignore_permissions=True)
