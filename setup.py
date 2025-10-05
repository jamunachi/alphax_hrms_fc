
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="alphax_hrms_fc",
    version="0.1.0",
    description="AlphaX HRMS for Frappe Cloud (Leave, Attendance, Payslip, ESS, Policies, QR)",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="AlphaX",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
