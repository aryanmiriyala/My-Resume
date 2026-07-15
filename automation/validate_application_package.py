#!/usr/bin/env python3
"""Validate a tailored application package against the repo pipeline rules."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = [
    "job-description.md",
    "tailoring-notes.md",
    "resume.tex",
    "resume.pdf",
    "cover-letter.md",
]

TAILORING_NOTE_MARKERS = [
    "## Job Keyword Map",
    "## Bullet Audit",
    "Job Alignment & Evidence Score:",
    "Internal estimate only; not a predicted ATS score.",
    "Strong matches",
    "Gaps / intentionally omitted unsupported keywords",
    "Recommended improvements",
]

RESUME_TEXT_MARKERS = [
    "Experience",
    "Projects",
    "Technical Skills",
    "SmartSolve",
    "American Association of Insurance Services",
    "Alliance for Paired Kidney Donation",
]

BUILD_ARTIFACT_SUFFIXES = {".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk", ".synctex.gz"}


def run_command(command: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def check_file_exists(app_dir: Path, rel_path: str, errors: list[str]) -> None:
    if not (app_dir / rel_path).is_file():
        errors.append(f"Missing required file: {rel_path}")


def check_cover_letter_artifact(app_dir: Path, errors: list[str]) -> None:
    if not any((app_dir / name).is_file() for name in ("cover-letter.pdf", "cover-letter.docx")):
        errors.append("Missing cover-letter submission artifact: cover-letter.pdf or cover-letter.docx")


def check_tailoring_notes(app_dir: Path, errors: list[str]) -> None:
    notes_path = app_dir / "tailoring-notes.md"
    if not notes_path.is_file():
        return

    text = notes_path.read_text(encoding="utf-8", errors="replace")
    for marker in TAILORING_NOTE_MARKERS:
        if marker not in text:
            errors.append(f"tailoring-notes.md missing marker: {marker}")

    score_match = re.search(r"Job Alignment & Evidence Score:\s*(\d{1,3})/100", text)
    if not score_match:
        errors.append(
            "tailoring-notes.md must record the internal score as "
            "`Job Alignment & Evidence Score: X/100`"
        )
    elif not 0 <= int(score_match.group(1)) <= 100:
        errors.append("Job Alignment & Evidence Score must be between 0 and 100")

    if re.search(r"\b(TODO|TBD|FIXME)\b", text, re.IGNORECASE):
        errors.append("tailoring-notes.md contains TODO/TBD/FIXME placeholder text")


def check_resume_pdf(app_dir: Path, errors: list[str], warnings: list[str]) -> None:
    resume_pdf = app_dir / "resume.pdf"
    if not resume_pdf.is_file():
        return

    if shutil.which("pdfinfo"):
        code, stdout, stderr = run_command(["pdfinfo", str(resume_pdf)])
        if code != 0:
            errors.append(f"pdfinfo failed for resume.pdf: {stderr.strip()}")
        else:
            page_match = re.search(r"^Pages:\s+(\d+)", stdout, re.MULTILINE)
            if not page_match:
                errors.append("Could not determine resume.pdf page count")
            elif int(page_match.group(1)) != 1:
                errors.append(f"resume.pdf must be exactly 1 page; found {page_match.group(1)}")
    else:
        warnings.append("pdfinfo not found; skipped resume page-count validation")

    if shutil.which("pdftotext"):
        code, stdout, stderr = run_command(["pdftotext", str(resume_pdf), "-"])
        if code != 0:
            errors.append(f"pdftotext failed for resume.pdf: {stderr.strip()}")
        else:
            for marker in RESUME_TEXT_MARKERS:
                if marker not in stdout:
                    errors.append(f"resume.pdf text missing expected marker: {marker}")
    else:
        warnings.append("pdftotext not found; skipped resume text validation")


def check_build_artifacts(app_dir: Path, errors: list[str]) -> None:
    for path in app_dir.iterdir():
        if path.is_file() and any(path.name.endswith(suffix) for suffix in BUILD_ARTIFACT_SUFFIXES):
            errors.append(f"Generated build artifact still present: {path.name}")


def validate(app_dir: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not app_dir.is_dir():
        print(f"FAIL: application directory does not exist: {app_dir}")
        return 2

    for rel_path in REQUIRED_FILES:
        check_file_exists(app_dir, rel_path, errors)

    check_cover_letter_artifact(app_dir, errors)
    check_tailoring_notes(app_dir, errors)
    check_resume_pdf(app_dir, errors, warnings)
    check_build_artifacts(app_dir, errors)

    for warning in warnings:
        print(f"WARN: {warning}")

    if errors:
        print(f"FAIL: {app_dir}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: {app_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a tailored application package.")
    parser.add_argument("application_dir", help="Path like application-packages/Company/Role")
    args = parser.parse_args()
    return validate(Path(args.application_dir))


if __name__ == "__main__":
    sys.exit(main())
