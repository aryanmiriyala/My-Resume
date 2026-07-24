#!/usr/bin/env python3
"""Validate a tailored application package against the repo pipeline rules."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
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
    "## Scoring Methodology",
    "Job Alignment & Evidence Score:",
    "Internal estimate only; not a predicted ATS score.",
    "Score breakdown",
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
MIN_ALIGNMENT_SCORE = 90
SUB_90_WAIVER_MARKER = "Sub-90 Readiness Waiver"
MIN_EXPERIENCE_BULLETS = 11
EXPERIENCE_BULLET_WAIVER_MARKER = "Experience Bullet Count Waiver"
MAX_PROFESSIONAL_SUMMARY_LINES = 2
MAX_UNUSED_BOTTOM_POINTS = 90.0
WARN_UNUSED_BOTTOM_POINTS = 72.0
MAX_SUBMISSION_ARTIFACT_BYTES = 5 * 1024 * 1024

TAILORING_GATE_RULES = [
    ("ATS source gate checked", ("Pass",)),
    ("Visual consistency gate checked", ("Pass",)),
    ("Page utilization gate checked", ("Pass", "Waived")),
    ("Cover-letter artifact checked", ("Pass",)),
]

FORBIDDEN_RESUME_SOURCE_PATTERNS = [
    (r"\\begin\{tabular\*?\}", "LaTeX tabular/tabular* constructs are not ATS-safe for application resumes"),
    (r"\\usepackage(?:\[[^\]]*\])?\{tabularx\}", "tabularx is not allowed in application resume source"),
    (r"\\includegraphics\b", "images/graphics are not allowed in application resumes"),
    (r"\\usepackage(?:\[[^\]]*\])?\{graphicx\}", "graphicx is not allowed in application resume source"),
    (r"\\begin\{multicols\}", "multi-column resume layouts are not allowed"),
    (r"\\twocolumn\b", "two-column resume layouts are not allowed"),
    (r"\\begin\{textblock\*?\}", "text boxes/positioned text blocks are not allowed"),
    (r"\\usepackage(?:\[[^\]]*\])?\{textpos\}", "textpos/text boxes are not allowed in application resume source"),
    (r"\\usepackage(?:\[[^\]]*\])?\{fontawesome5?\}", "icons are not allowed in application resumes"),
    (r"\\usepackage(?:\[[^\]]*\])?\{fancyhdr\}", "resume content must not rely on headers or footers"),
    (r"\\pagestyle\{fancy\}", "resume content must not rely on headers or footers"),
    (r"\\fancy(?:head|foot)\b", "resume content must not rely on headers or footers"),
]

REQUIRED_RESUME_SOURCE_PATTERNS = [
    (r"\\documentclass\[[^\]]*\b11pt\b[^\]]*\]\{article\}", "resume.tex must use the canonical 11pt article class"),
    (r"\\usepackage\[[^\]]*letterpaper[^\]]*\]\{geometry\}", "resume.tex must use explicit letterpaper geometry"),
    (r"\\input\{glyphtounicode\}", "resume.tex must input glyphtounicode for text extraction"),
    (r"\\pdfgentounicode=1", "resume.tex must enable unicode text extraction with \\pdfgentounicode=1"),
    (r"\\pagestyle\{empty\}", "resume.tex must avoid PDF headers and footers with \\pagestyle{empty}"),
    (r"\\linespread\{0\.92\}", "resume.tex must preserve the canonical application-resume line spread"),
    (r"\\newlist\{tightitemize\}\{itemize\}\{1\}", "resume.tex must use the canonical single-level tightitemize list"),
]

WEAK_BULLET_OPENERS = re.compile(
    r"\\item\s+(?:Responsible for|Helped(?:\s+with)?|Worked(?:\s+on)?|Assisted(?:\s+with)?)\b",
    re.IGNORECASE,
)

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\[paste\b",
    r"\[insert\b",
    r"\[company\b",
    r"\[role\b",
]


def contains_placeholder(text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in PLACEHOLDER_PATTERNS)


def run_command(command: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    return proc.returncode, proc.stdout, proc.stderr


def check_file_exists(app_dir: Path, rel_path: str, errors: list[str]) -> None:
    if not (app_dir / rel_path).is_file():
        errors.append(f"Missing required file: {rel_path}")


def check_cover_letter_artifact(app_dir: Path, errors: list[str]) -> None:
    artifacts = [app_dir / name for name in ("cover-letter.pdf", "cover-letter.docx") if (app_dir / name).is_file()]
    if not artifacts:
        errors.append("Missing cover-letter submission artifact: cover-letter.pdf or cover-letter.docx")
        return

    for artifact in artifacts:
        if artifact.stat().st_size > MAX_SUBMISSION_ARTIFACT_BYTES:
            errors.append(f"{artifact.name} exceeds the conservative 5 MB submission artifact limit")


def check_tailoring_notes(app_dir: Path, errors: list[str]) -> None:
    notes_path = app_dir / "tailoring-notes.md"
    if not notes_path.is_file():
        return

    text = notes_path.read_text(encoding="utf-8", errors="replace")
    for marker in TAILORING_NOTE_MARKERS:
        if marker not in text:
            errors.append(f"tailoring-notes.md missing marker: {marker}")

    for gate_name, allowed_values in TAILORING_GATE_RULES:
        gate_match = re.search(rf"^\s*-\s*{re.escape(gate_name)}:\s*(.+)$", text, re.MULTILINE)
        if not gate_match:
            errors.append(f"tailoring-notes.md missing verification gate: {gate_name}:")
            continue

        gate_value = gate_match.group(1).strip()
        if not gate_value:
            errors.append(f"tailoring-notes.md verification gate is blank: {gate_name}:")
        elif not gate_value.startswith(allowed_values):
            allowed_text = " or ".join(allowed_values)
            errors.append(f"tailoring-notes.md verification gate `{gate_name}` must start with {allowed_text}")
        elif gate_value.startswith("Waived") and len(gate_value.split()) < 4:
            errors.append(f"tailoring-notes.md waiver for `{gate_name}` must include a concrete reason")

    score_match = re.search(r"Job Alignment & Evidence Score:\s*(\d{1,3})/100", text)
    if not score_match:
        errors.append(
            "tailoring-notes.md must record the internal score as "
            "`Job Alignment & Evidence Score: X/100`"
        )
    elif not 0 <= int(score_match.group(1)) <= 100:
        errors.append("Job Alignment & Evidence Score must be between 0 and 100")
    else:
        score = int(score_match.group(1))
        if score < MIN_ALIGNMENT_SCORE and SUB_90_WAIVER_MARKER not in text:
            errors.append(
                "Job Alignment & Evidence Score below 90 requires a "
                "`Sub-90 Readiness Waiver` section in tailoring-notes.md"
            )

    if contains_placeholder(text):
        errors.append("tailoring-notes.md contains placeholder text")


def check_cover_letter_source(app_dir: Path, errors: list[str]) -> None:
    cover_letter = app_dir / "cover-letter.md"
    if not cover_letter.is_file():
        return

    text = cover_letter.read_text(encoding="utf-8", errors="replace")
    if contains_placeholder(text):
        errors.append("cover-letter.md contains placeholder text")
    if len(text.strip()) < 900:
        errors.append("cover-letter.md appears too thin to provide role-specific motivation and evidence")


def check_resume_source(app_dir: Path, errors: list[str]) -> None:
    resume_tex = app_dir / "resume.tex"
    if not resume_tex.is_file():
        return

    text = resume_tex.read_text(encoding="utf-8", errors="replace")
    notes_text = ""
    notes_path = app_dir / "tailoring-notes.md"
    if notes_path.is_file():
        notes_text = notes_path.read_text(encoding="utf-8", errors="replace")

    if contains_placeholder(text):
        errors.append("resume.tex contains placeholder text")
    for pattern, message in FORBIDDEN_RESUME_SOURCE_PATTERNS:
        if re.search(pattern, text):
            errors.append(f"resume.tex ATS source gate failed: {message}")
    for pattern, message in REQUIRED_RESUME_SOURCE_PATTERNS:
        if not re.search(pattern, text):
            errors.append(f"resume.tex canonical source gate failed: {message}")
    if WEAK_BULLET_OPENERS.search(text):
        errors.append(
            "resume.tex contains a bullet starting with a weak opener "
            "(Responsible for, Helped, Worked on, or Assisted)"
        )
    experience_match = re.search(
        r"\\resumesection\{Experience\}(.*?)\\resumesection\{Projects\}",
        text,
        re.DOTALL,
    )
    if experience_match:
        experience_bullets = len(re.findall(r"\\item\b", experience_match.group(1)))
        if experience_bullets < MIN_EXPERIENCE_BULLETS and EXPERIENCE_BULLET_WAIVER_MARKER not in notes_text:
            errors.append(
                "resume.tex has fewer than "
                f"{MIN_EXPERIENCE_BULLETS} experience bullets; add verified role-aligned "
                f"experience evidence or document `{EXPERIENCE_BULLET_WAIVER_MARKER}`"
            )


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def check_resume_page_utilization(app_dir: Path, errors: list[str], warnings: list[str]) -> None:
    resume_pdf = app_dir / "resume.pdf"
    if not resume_pdf.is_file() or not shutil.which("pdftotext"):
        return

    code, stdout, stderr = run_command(["pdftotext", "-bbox", str(resume_pdf), "-"])
    if code != 0:
        warnings.append(f"pdftotext -bbox failed for resume.pdf; skipped page-utilization check: {stderr.strip()}")
        return

    try:
        root = ET.fromstring(stdout)
    except ET.ParseError as exc:
        warnings.append(f"Could not parse pdftotext -bbox output; skipped page-utilization check: {exc}")
        return

    pages = [element for element in root.iter() if local_name(element.tag) == "page"]
    if not pages:
        warnings.append("pdftotext -bbox output had no page nodes; skipped page-utilization check")
        return

    page = pages[0]
    try:
        page_height = float(page.attrib["height"])
    except (KeyError, ValueError):
        warnings.append("pdftotext -bbox output had no usable page height; skipped page-utilization check")
        return

    max_y = 0.0
    for word in page.iter():
        if local_name(word.tag) != "word":
            continue
        try:
            max_y = max(max_y, float(word.attrib["yMax"]))
        except (KeyError, ValueError):
            continue

    if max_y <= 0:
        warnings.append("pdftotext -bbox output had no word positions; skipped page-utilization check")
        return

    unused_bottom = page_height - max_y
    if unused_bottom > MAX_UNUSED_BOTTOM_POINTS:
        errors.append(
            "resume.pdf appears substantially underfilled: "
            f"about {unused_bottom / 72:.1f} inches of unused bottom space"
        )
    elif unused_bottom > WARN_UNUSED_BOTTOM_POINTS:
        warnings.append(
            "resume.pdf may be underfilled: "
            f"about {unused_bottom / 72:.1f} inches of unused bottom space"
        )


def check_professional_summary_lines(resume_text: str, errors: list[str]) -> None:
    lines = [line.strip() for line in resume_text.splitlines()]
    summary_start: int | None = None
    for index, line in enumerate(lines):
        if line == "Professional Summary":
            summary_start = index + 1
            break

    if summary_start is None:
        return

    summary_lines: list[str] = []
    for line in lines[summary_start:]:
        if line == "Education":
            break
        if line:
            summary_lines.append(line)

    if len(summary_lines) > MAX_PROFESSIONAL_SUMMARY_LINES:
        errors.append(
            "Professional Summary renders/extracts as "
            f"{len(summary_lines)} lines; maximum is {MAX_PROFESSIONAL_SUMMARY_LINES} PDF lines"
        )


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
            check_professional_summary_lines(stdout, errors)
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
    check_cover_letter_source(app_dir, errors)
    check_resume_source(app_dir, errors)
    check_resume_pdf(app_dir, errors, warnings)
    check_resume_page_utilization(app_dir, errors, warnings)
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
