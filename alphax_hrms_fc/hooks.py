from __future__ import unicode_literals

app_name = "alphax_hrms_fc"
app_title = "AlphaX HRMS FC"
app_publisher = "AlphaX"
app_description = "HRMS utilities for ERPNext/Frappe Cloud"
app_email = "noreply@example.com"
app_license = "MIT"

# --- Use RAW includes (avoid bundling) ---
# Files must exist under alphax_hrms_fc/public/** and will be served from /assets/alphax_hrms_fc/**
app_include_css = [
    "/assets/alphax_hrms_fc/css/alphax.css",
]
app_include_js = [
    "/assets/alphax_hrms_fc/js/boot.js",
    "/assets/alphax_hrms_fc/js/qr_loader.js",
]

# Keep the rest empty to avoid esbuild path resolution on undefined entries
web_include_css = []
web_include_js  = []
page_js = {}
doctype_js = {}
doctype_list_js = {}
doctype_tree_js = {}
website_theme_scss = ""
