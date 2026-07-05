# Gmail Application Monitor

This directory is for a future Gmail status monitor that checks Aryan's inbox for job-application updates and updates `application-management/application-tracker.md`.

The monitor should run on a schedule, not continuously. Current desired cadence: **4 times per day**.

Suggested local times:

- 8:00 AM
- 12:00 PM
- 4:00 PM
- 8:00 PM

## Recommended Architecture

Use scheduled Gmail API polling:

1. Authenticate with Gmail API using OAuth.
2. Search recent messages using the query from `application-management/email-rules.md`.
3. Classify messages as:
   - Confirmation
   - Assessment
   - Recruiter Response
   - Interview
   - Rejection
   - Offer
   - Unknown / Needs Review
4. Update `application-management/application-tracker.md`.
5. Optionally append sanitized updates to `applications/<Company>/<Role>/email-updates.md`.

## Privacy Rules

Do not commit:

- `credentials.json`
- `token.json`
- OAuth refresh tokens
- raw Gmail message dumps
- full email bodies

Store only sanitized metadata by default:

- sender
- subject
- date
- detected company
- detected role
- classified status
- short note

## Setup Notes

Use official Gmail API OAuth flow when implementing the monitor.

Initial dependencies will likely include:

```text
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```

Do not install dependencies or create credentials until Aryan explicitly asks to implement the working monitor.

## Scheduling Options

### macOS launchd

Use launchd if running on Aryan's Mac. The job can be scheduled four times per day and run a local Python script.

### cron

Equivalent cron schedule:

```cron
0 8,12,16,20 * * * cd /path/to/My-Resume && /path/to/python scripts/gmail_application_monitor/check_gmail.py
```

### Manual

For early testing, run the monitor manually before enabling any schedule.
