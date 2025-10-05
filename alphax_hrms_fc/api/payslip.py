
import frappe
from frappe import _
from frappe.utils.pdf import get_pdf

@frappe.whitelist()
def get_my_payslips(limit: int = 50):
    if frappe.session.user == "Guest":
        frappe.throw("Login required")
    emp = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
    if not emp:
        return []
    return frappe.get_all(
        "Salary Slip",
        filters={"employee": emp},
        fields=["name","start_date","end_date","status","gross_pay","net_pay"],
        order_by="start_date desc",
        limit=limit,
    )

@frappe.whitelist()
def download_payslip_pdf(salary_slip: str):
    if frappe.has_role("HR Manager"):
        pass
    elif frappe.has_role("Employee"):
        emp = frappe.db.get_value("Salary Slip", salary_slip, "employee")
        user_emp = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
        if not user_emp or user_emp != emp:
            frappe.throw(_("Not permitted to view this payslip"), frappe.PermissionError)
    else:
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    html = frappe.get_print("Salary Slip", salary_slip)
    pdf = get_pdf(html)
    filedoc = frappe.get_doc({
        "doctype": "File",
        "file_name": f"SalarySlip-{salary_slip}.pdf",
        "content": pdf,
        "is_private": 1
    })
    filedoc.insert()
    return {"file_url": filedoc.file_url}
