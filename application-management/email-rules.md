# Application Email Rules

Use these rules when classifying Gmail messages related to job applications. Prefer conservative classification: if uncertain, mark `Needs Review`.

## Search Scope

Default Gmail search should prioritize likely application messages:

```text
newer_than:30d (application OR applied OR interview OR recruiter OR assessment OR "thank you for applying" OR "not selected" OR "unfortunately" OR "next steps")
```

Search can also include common ATS/recruiting domains and senders as they appear in real emails.

## Status Classification

### Confirmation

Signals:

- "application received"
- "we received your application"
- "thank you for applying"
- "your application has been submitted"
- "successfully submitted"

Tracker action:

- Set status to `Confirmation` or `Applied`.
- Add sender, subject, and email date to notes.

### Assessment

Signals:

- "coding assessment"
- "technical assessment"
- "online assessment"
- "HackerRank"
- "CodeSignal"
- "take-home"
- "challenge"

Tracker action:

- Set status to `Assessment`.
- Add deadline if present.
- Mark `Needs Review` if action is required.

### Recruiter Response

Signals:

- "recruiter"
- "talent acquisition"
- "following up"
- "next steps"
- "availability"

Tracker action:

- Set status to `Recruiter Response`.
- Mark `Needs Review`.

### Interview

Signals:

- "schedule an interview"
- "interview invitation"
- "availability for a call"
- "meet with"
- "phone screen"
- "technical interview"

Tracker action:

- Set status to `Interviewing`.
- Add date/time/deadline if present.
- Mark `Needs Review`.

### Rejection

Signals:

- "unfortunately"
- "not selected"
- "not move forward"
- "pursue other candidates"
- "after careful consideration"
- "we will not be proceeding"

Tracker action:

- Set status to `Rejected`.
- Do not delete application materials automatically.

### Offer

Signals:

- "offer"
- "congratulations"
- "pleased to offer"
- "employment offer"

Tracker action:

- Set status to `Offer`.
- Mark `Needs Review`.

## Privacy Rules

- Do not store raw full email bodies by default.
- Store only sanitized metadata:
  - date
  - sender
  - subject
  - detected company
  - detected role
  - classified status
  - short note
- Never commit Gmail credentials, OAuth tokens, refresh tokens, or downloaded message bodies.

