# Manual finance dashboard pattern

Use this reference when the user asks for a lightweight finance/reconciliation dashboard from screenshots or chat-provided numbers, especially when API integration is unavailable or premature.

## Pattern

1. **Publish as static HTML when speed matters**
   - Write to `/var/www/html/<slug>/index.html` when the user wants a live browser view.
   - Verify the exact public URL with HTTP 200 before replying.
   - Keep the first version self-contained unless backend persistence is explicitly needed.

2. **Preserve source/account separation**
   - Model each source/account explicitly: `accounts = [{ id, label, earnings: [...] }]`.
   - Do not collapse different people/accounts into one bucket just because they share a period.
   - If the user corrects ownership of screenshots, move data to the corrected account and leave the old account empty/untouched until new source data arrives.

3. **Use per-account budgets**
   - Advertising spend is often manually entered and account-specific.
   - Store budget as `accountId::period`, not just by period, so Razz/Arif/etc. filters do not contaminate each other.
   - For an “All accounts” view, sum the per-account budget keys for that period.

4. **Support custom accounting periods**
   - Do not assume calendar months.
   - If the user gives cycles like `20 Mei / 19 Juni`, encode period labels exactly enough for the business logic.
   - When a user gives a nonstandard first period like `1 April / 19 Mei`, keep it as its own explicit period label instead of forcing it into a generic month if that would distort totals.

5. **Separate aggregate entries from transaction entries**
   - Screenshot-extracted payout rows can be detailed transaction entries.
   - User-provided period totals can be entered as aggregate rows with stable IDs, e.g. `RAZZ-2026-04-01-05-19`.
   - Mark aggregate rows clearly in IDs/notes if detail-vs-summary may matter later.

## Verification checklist

- Read the live file before overwriting it.
- Verify changed strings/amounts are present.
- Syntax-check extracted JavaScript where possible (`node --check` on the script block).
- Verify public URL returns HTTP 200.
- In the reply, state only verified totals/periods and the link.

## Pitfalls

- Do not let browser `localStorage` silently override newly hardcoded defaults. If the page stores manual budgets, warn that stale localStorage can affect the visible browser result or add migration logic.
- Do not mix global period budgets with account-level filters; it makes filtered ROAS/profit wrong.
- Do not over-explain after updating a dashboard; give the link, the two or three changed numbers, and the verification status.
