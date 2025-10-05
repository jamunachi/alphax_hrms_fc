# alphax_hrms_fc/alphax_hrms_fc/hooks.py
from __future__ import unicode_literals

app_name = "alphax_hrms_fc"
app_title = "AlphaX HRMS FC"
app_publisher = "AlphaX"
app_description = "HRMS utilities for ERPNext/Frappe Cloud"
app_email = "support@example.com"
app_license = "MIT"

# IMPORTANT: use lists only; do not return None anywhere.
# Keep these empty for now; we'll let build.json exist but not include from hooks.
app_include_css = []
app_include_js  = []
web_include_css = []
web_include_js  = []

# Omit website_theme_scss entirely (don’t set it to "" or None)

# Avoid optional hooks that could return None
# (leave out page_js / doctype_js dicts unless you actually use them)
