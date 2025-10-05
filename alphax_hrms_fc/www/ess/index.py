
import frappe
from frappe import _

no_cache = 1

def get_context(context):
    if not frappe.db.get_single_value("AlphaX HRMS Settings", "allow_portal_access"):
        frappe.throw(_("ESS Portal is disabled"))
    if frappe.session.user == 'Guest':
        frappe.local.flags.redirect_location = "/login"
        raise frappe.Redirect

    context.title = "Employee Self Service"
    return context
