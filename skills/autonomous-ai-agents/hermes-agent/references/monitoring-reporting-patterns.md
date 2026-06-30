# Monitoring/reporting cron patterns

Use this pattern when Hermes is asked to monitor a company, bank, service, or risk surface and send recurring human-readable reports.

## Principle

If the user wants to audit the agent's reasoning, do **not** send only a top-line status such as "green" / "safe" / "OK". The recurring report should include enough evidence for the user to judge whether the conclusion is warranted.

## Recommended report shape

1. **Status** — final classification (for example: HIJAU / KUNING / MERAH).
2. **Latest indicators** — the actual metrics and their threshold mapping.
3. **Significant developments** — concise bullets for the period being monitored.
4. **Red flags detected** — explicit list, or "none detected".
5. **Sources checked** — name the reports/pages/news sources actually consulted.
6. **Recommendation** — action + short rationale.
7. **Validation notes / limitations** — say what could not be verified because of source lag, rate limiting, blocked search pages, missing disclosures, etc.

## Prompting rules

- Tell the cron job to use the user's language.
- Require the job to distinguish **verified facts** from **inference**.
- Require the job to say when a source could not be accessed; do not silently fill gaps.
- For threshold-based monitors, require per-indicator classification, not just one overall color.
- If the transport channel is narrow (for example WhatsApp), still send the full report body unless the user explicitly asks for a short summary.

## Architecture pattern: analysis job + transport job

When the report must be delivered through a platform-specific path that is not exposed as a normal Hermes target:

1. Create the main cron job that performs the research and writes normal cron output.
2. Create a second transport-only job (`no_agent=True`) a few minutes later.
3. The transport job should read the latest output artifact, verify the platform bridge/endpoint is healthy, then forward the full body.

This keeps the research prompt and transport logic decoupled.

## Pitfalls

- A green status with no evidence reduces trust; users often want to verify the reasoning themselves.
- If external news search is partially blocked, note the limitation explicitly instead of claiming there was no news.
- Do not bury the source list; put it in every report.
- If a user rejects personal-account fields (deposit amount, account number, etc.), remove them from the monitor context entirely and keep the job focused on institution-level surveillance.
