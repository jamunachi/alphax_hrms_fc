
import frappe

@frappe.whitelist()
def get_active_theme():
    name = frappe.db.get_single_value("AlphaX HRMS Settings", "active_theme_name") or "Default"
    try:
        doc = frappe.get_doc("My Theme", name)
    except Exception:
        return {}
    return {
        "button_background_color": getattr(doc, "button_background_color", None),
        "button_hover_background_color": getattr(doc, "button_hover_background_color", None),
        "button_text_color": getattr(doc, "button_text_color", None),
        "heading_text_color": getattr(doc, "heading_text_color", None),
        "box_background_color": getattr(doc, "box_background_color", None),
    }
