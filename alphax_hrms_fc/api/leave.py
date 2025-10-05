
import frappe
from frappe import _

REQUIRED_ROLE_EMP = "Employee"

@frappe.whitelist()
def create_leave_application(employee: str, leave_type: str, from_date: str, to_date: str, description: str = ""):
    if not (frappe.has_role(REQUIRED_ROLE_EMP) or frappe.has_role("HR Manager")):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    doc = frappe.new_doc("Leave Application")
    doc.employee = employee
    doc.leave_type = leave_type
    doc.from_date = from_date
    doc.to_date = to_date
    doc.description = description
    doc.insert()
    return {"name": doc.name}

@frappe.whitelist()
def submit_leave_application(name: str):
    if not (frappe.has_role(REQUIRED_ROLE_EMP) or frappe.has_role("HR Manager")):
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    doc = frappe.get_doc("Leave Application", name)
    doc.submit()
    return {"name": doc.name, "status": doc.status}
