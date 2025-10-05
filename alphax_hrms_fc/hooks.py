
app_name = "alphax_hrms_fc"
app_title = "AlphaX HRMS FC"
app_publisher = "AlphaX"
app_description = "HRMS add-on: Leave, Attendance, Payslip, ESS, Theming, Policies, QR"
app_email = "support@example.com"
app_license = "MIT"

app_include_css = []
app_include_js  = []
    "alphax_hrms_fc/public/js/boot.js",
    "alphax_hrms_fc/public/js/qr_loader.js"
]

fixtures = [
    {"doctype": "Page", "filters": [["name", "=", "alphax-hrms"]]},
    {"doctype": "AlphaX HRMS Settings"},
    {"doctype": "AlphaX Checkin Policy"},
    {"doctype": "AlphaX Checkin Policy Assignment"}
]

