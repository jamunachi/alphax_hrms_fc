from setuptools import setup, find_packages

setup(
    name="alphax_hrms_fc",
    version="0.1.31",
    description="HRMS utilities for ERPNext/Frappe Cloud",
    author="AlphaX",
    author_email="support@example.com",
    license="MIT",
    packages=find_packages(),     # MUST include alphax_hrms_fc
    include_package_data=True,
    install_requires=[],
    zip_safe=False,
)
