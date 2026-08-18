import frappe
from frappe.model.document import Document
from frappe.utils import add_days, getdate

# Section 6 of the project plan: SLA target expressed in days from opened_date.
# Critical's "24 hours" is treated as 1 day at Date-field granularity.
SLA_DAYS_BY_PRIORITY = {
	"Critical": 1,
	"High": 3,
	"Medium": 7,
	"Low": 14,
}

# States in which a case is still "in flight" and should be SLA-tracked.
OPEN_WORKFLOW_STATES = ("Open", "Assigned", "In Progress", "Pending")


class Case(Document):
	def validate(self):
		self.set_target_resolution_date()
		self.validate_confidentiality()

	def set_target_resolution_date(self):
		"""Recalculate the SLA deadline whenever priority or opened_date change."""
		if not self.opened_date:
			return
		days = SLA_DAYS_BY_PRIORITY.get(self.priority, 7)
		self.target_resolution_date = add_days(getdate(self.opened_date), days)

	def validate_confidentiality(self):
		"""Highly Restricted cases must always have a named officer accountable for them."""
		if self.confidentiality_level == "Highly Restricted" and not self.assigned_officer:
			frappe.throw("Highly Restricted cases must have an Assigned Officer before saving.")
