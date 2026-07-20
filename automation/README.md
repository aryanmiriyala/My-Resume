# Automation

Validation and local helper scripts for the application pipeline.

- `validate_application_package.py`: checks that a selected application package has the expected files, one-page resume PDF, internal alignment notes, explicit pass/waiver verification gates, placeholder-free resume and cover-letter sources, cover-letter artifact, ATS-safe canonical resume source structure, extractable PDF text, bottom-page utilization when `pdftotext -bbox` is available, conservative artifact size, and clean generated LaTeX state.

This folder should stay focused on repo/application validation only.
