
from frappe import _

def get_data():
    return [
        {
            "label": _("AlphaX HRMS"),
            "items": [
                {
                    "type": "page",
                    "name": "alphax-hrms",
                    "icon": "octicon octicon-people",
                    "label": _("AlphaX HRMS"),
                },
            ],
        }
    ]
