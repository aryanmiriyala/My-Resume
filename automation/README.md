# Automation

Validation and local helper scripts for the application pipeline.

- `validate_application_package.py`: checks that a selected application package has the expected files, one-page resume PDF, internal alignment notes, cover-letter artifact, ATS-safe resume source structure, extractable PDF text, bottom-page utilization when `pdftotext -bbox` is available, and clean generated LaTeX state.

This folder should stay focused on repo/application validation only.
