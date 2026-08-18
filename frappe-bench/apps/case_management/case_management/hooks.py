app_name = "case_management"
app_title = "Case Management"
app_publisher = "Kellia U."
app_description = "Case management project"
app_email = "kellumuhire@gmail.com"
app_license = "mit"

# Send non-GET requests for this app's endpoints as native `application/json`
# bodies instead of form-encoded, per-key JSON-stringified values.
use_json_request_body = True

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "case_management",
# 		"logo": "/assets/case_management/logo.png",
# 		"title": "Case Management",
# 		"route": "/case_management",
# 		"has_permission": "case_management.api.permission.has_app_permission",
# 	}
# ]

# Companion apps that extend a host app (instead of taking their own apps-screen icon) can pin
# their workspaces into the host app's workspace dock (rail) with this hook. Declaring it keeps
# the app off the apps screen, so it takes precedence over any add_to_apps_screen above. Who can
# see a pinned workspace is controlled by that workspace's own Roles table.
# add_to_workspace_dock = [
# 	{
# 		"app": "erpnext",
# 		"workspace": "My Workspace",
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/case_management/css/case_management.css"
# app_include_js = "/assets/case_management/js/case_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/case_management/css/case_management.css"
# web_include_js = "/assets/case_management/js/case_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "case_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "case_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Setup Wizard
# ------------

# open a fresh site's setup in this app's own UI instead of the desk wizard.
# must be a non-desk route (not under /desk or /app); to customize setup within
# desk, use setup_wizard_stages / setup_wizard_complete instead.
# setup_wizard_url = "/case_management/setup"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "case_management.utils.jinja_methods",
# 	"filters": "case_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "case_management.install.before_install"
# after_install = "case_management.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "case_management.uninstall.before_uninstall"
# after_uninstall = "case_management.uninstall.after_uninstall"

# Disable / Enable
# ----------------
# Called when this app is logically disabled or re-enabled on a site,
# without uninstalling it. Use this to hide/restore fields this app adds
# to other apps' doctypes.

# before_disable = "case_management.uninstall.before_disable"
# after_disable = "case_management.uninstall.after_disable"
# before_enable = "case_management.install.before_enable"
# after_enable = "case_management.install.after_enable"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "case_management.utils.before_app_install"
# after_app_install = "case_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "case_management.utils.before_app_uninstall"
# after_app_uninstall = "case_management.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "case_management.build.after_build"

# To hook into the build process of other apps
# The list of apps being built is passed as an argument

# after_app_build = "case_management.build.after_app_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "case_management.notifications.get_notification_config"

# Awesome Bar
# -----------
# Extra search results: list of dicts with label, description, route, index.
# route: ["List", "ToDo"], "/desk/docs/some/page", or "https://example.com"
# awesomebar_search = ["case_management.search.awesomebar_results"]

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"case_management.tasks.all"
# 	],
# 	"daily": [
# 		"case_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"case_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"case_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"case_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "case_management.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "case_management.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "case_management.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "case_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["case_management.utils.before_request"]
# after_request = ["case_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["case_management.utils.before_job"]
# after_job = ["case_management.utils.after_job"]

# after_file_upload = ["case_management.utils.after_file_upload"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"case_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

# Require all whitelisted methods to have type annotations
require_type_annotated_api_methods = True

# Fixtures
# --------
# Ships the Case Officer / Supervisor roles and the Case Workflow (states +
# transitions) with the app so a fresh `bench install-app case_management`
# reproduces the locked design doc without manual clicking.

fixtures = [
	{"doctype": "Role", "filters": [["name", "in", ["Case Officer", "Supervisor"]]]},
	{"doctype": "Workflow", "filters": [["name", "=", "Case Workflow"]]},
]

# Permissions
# -----------
# Row-level restriction on top of the DocType-level role permissions: a Case
# Officer only sees Cases (and non-Confidential Case Notes) they're assigned
# to; Supervisor/System Manager see everything. See case_management/permissions.py.

permission_query_conditions = {
	"Case": "case_management.case_management.permissions.get_case_permission_query_conditions",
	"Case Note": "case_management.case_management.permissions.get_case_note_permission_query_conditions",
}

has_permission = {
	"Case": "case_management.case_management.permissions.has_case_permission",
	"Case Note": "case_management.case_management.permissions.has_case_note_permission",
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"daily": [
		"case_management.case_management.tasks.check_overdue_cases",
	],
}

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

