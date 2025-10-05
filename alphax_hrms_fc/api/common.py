
import frappe
from datetime import date

@frappe.whitelist()
def get_current_employee():
    user = frappe.session.user
    if user == "Guest":
        return None
    return frappe.db.get_value("Employee", {"user_id": user}, "name")

@frappe.whitelist()
def get_employee_defaults(employee: str):
    if not employee:
        return {}
    doc = frappe.get_doc("Employee", employee)
    return {
        "default_branch": getattr(doc, "branch", None),
        "default_project": getattr(doc, "project", None),
    }

@frappe.whitelist()
def get_policies_for_today(employee: str):
    today = date.today()
    ass = frappe.get_all("AlphaX Checkin Policy Assignment",
        filters={"employee": employee, "from_date": ["<=", today], "to_date": ["in", [None, "", 0, today]]},
        fields=["policy"]
    )
    if not ass:
        return []
    policies = frappe.get_all("AlphaX Checkin Policy",
        filters={"name": ["in", [a.policy for a in ass]], "active": 1},
        fields=["name","scope_type","scope","latitude","longitude","radius_m","qr_required"]
    )
    return policies
