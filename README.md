
# AlphaX HRMS FC

A Frappe Cloud–ready HRMS frontend that integrates with ERPNext HR.

## Features
- Inline Leave Application (create + submit)
- Attendance check-in/out with IP + optional geolocation
- Geo-fence policies by Branch / Warehouse / Location / Project
- Multiple policy assignments per day
- QR-locked policies + built-in QR scanner (configurable)
- Payslip viewer with secure PDF download
- Role guards (Employee vs HR Manager)
- ESS Portal (`/ess`)
- Theming from `My Theme` DocType
- Settings panel to toggle all features

## Install (Frappe Cloud)
1. Create a site (or pick an existing one).
2. Apps → **Install from Repository** → paste this repo URL.
3. After install, open **AlphaX HRMS Settings** and configure:
   - Active Theme Name (e.g., `Default`)
   - Enable QR Scanner on Desk/Portal (optional)
   - Require Geolocation (optional)
   - Prefer Employee Defaults / Allow Manual Policy Choice
   - (Legacy) Global Geo Fence options
4. Open the **AlphaX HRMS** page from the Awesome Bar.
5. ESS Portal at `/ess` (requires login).

### Notes on QR library
This template bundles a vendor placeholder at:
`/assets/alphax_hrms_fc/js/vendor/html5-qrcode.min.js`

> Replace this file with the real `html5-qrcode` minified build if you want camera scanning to work without CDN.  
> Or point **AlphaX HRMS Settings → QR Library URL** to a CDN like `https://unpkg.com/html5-qrcode`.

## Development (local)
```bash
bench get-app /path/to/alphax_hrms_fc
bench --site your.site install-app alphax_hrms_fc
bench build && bench migrate
```

## Versioning
- v0.1.0 – Initial public release

License: MIT
