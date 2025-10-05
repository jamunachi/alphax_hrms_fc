
import frappe
from frappe import _
from datetime import datetime, date
import math

_DEF_EARTH_R = 6371000.0

def _haversine_m(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlmb/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return _DEF_EARTH_R * c

@frappe.whitelist()
def checkin(employee: str, log_type: str = "IN", latitude: float | None = None, longitude: float | None = None,
            shift_type: str | None = None, branch: str | None = None, warehouse: str | None = None,
            location: str | None = None, project: str | None = None,
            policy: str | None = None, qr_token: str | None = None):
    if not (frappe.has_role("Employee") or frappe.has_role("HR Manager")):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    settings = frappe.get_single("AlphaX HRMS Settings")
    today = date.today()

    ass = frappe.get_all("AlphaX Checkin Policy Assignment",
        filters={"employee": employee, "from_date": ["<=", today], "to_date": ["in", [None, "", 0, today]]},
        fields=["policy","allow_outside"]
    )
    assigned = {a.policy: a for a in ass}

    candidates = []
    if ass:
        candidates = frappe.get_all("AlphaX Checkin Policy",
            filters={"name": ["in", list(assigned.keys())], "active": 1},
            fields=["name","scope_type","scope","latitude","longitude","radius_m","qr_required","qr_token"]
        )

    chosen = None
    if policy:
        chosen = next((p for p in candidates if p.name == policy), None)
        if not chosen:
            frappe.throw(_("Selected policy is not assigned / not active."))

    if not chosen:
        pref = None
        if branch:   pref = ("Branch", branch)
        if warehouse: pref = ("Warehouse", warehouse)
        if location:  pref = ("Location", location)
        if project:   pref = ("Project", project)
        if pref:
            chosen = next((p for p in candidates if p.scope_type == pref[0] and p.scope == pref[1]), None)

    if not chosen and getattr(settings, "prefer_employee_defaults", 0):
        emp = frappe.get_doc("Employee", employee)
        defaults = [("Branch", getattr(emp, "branch", None)), ("Project", getattr(emp, "project", None))]
        for st, sc in defaults:
            if sc:
                chosen = next((p for p in candidates if p.scope_type == st and p.scope == sc), None)
                if chosen: break

    if not chosen and candidates:
        chosen = candidates[0]

    if not chosen and candidates == [] and not frappe.has_role("HR Manager"):
        frappe.throw(_("No active policy assigned for you today."))

    if chosen and chosen.qr_required and not frappe.has_role("HR Manager"):
        if not qr_token or qr_token != (chosen.qr_token or ""):
            frappe.throw(_("QR validation failed for this policy."))

    if chosen and latitude is not None and longitude is not None:
        dist = _haversine_m(float(latitude), float(longitude), float(chosen.latitude), float(chosen.longitude))
        allowed = dist <= float(chosen.radius_m)
        if not allowed and not frappe.has_role("HR Manager"):
            allow_outside = 0
            a = assigned.get(chosen.name)
            if isinstance(a, dict):
                allow_outside = a.get("allow_outside") or 0
            else:
                try: allow_outside = a.allow_outside
                except Exception: pass
            if not allow_outside:
                frappe.throw(_(f"Outside allowed zone for policy {chosen.name} (distance {int(dist)}m)"))

    ip = getattr(frappe.local, "request_ip", None) or (getattr(frappe.local, "request", None) and frappe.local.request_ip) or None
    meta = []
    if ip: meta.append(f"IP:{ip}")
    if latitude is not None and longitude is not None:
        meta.append(f"GEO:{latitude},{longitude}")
    if chosen:
        meta.append(f"POLICY:{chosen.name}")

    doc = frappe.new_doc("Employee Checkin")
    doc.employee = employee
    doc.time = datetime.now()
    doc.log_type = (log_type or "IN").upper()
    doc.device_id = ", ".join(meta) if meta else "AlphaX HRMS FC"

    for k, v in {"branch":branch, "warehouse":warehouse, "location":location, "project":project, "shift":shift_type}.items():
        if v and hasattr(doc, "meta") and getattr(doc.meta, "fields_map", None) and k in doc.meta.fields_map:
            setattr(doc, k, v)

    doc.insert()
    return {"name": doc.name, "time": doc.time, "policy": getattr(chosen, 'name', None)}
