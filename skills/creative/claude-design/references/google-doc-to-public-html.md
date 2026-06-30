# Google Doc → Public HTML Artifact

Use this when the user gives a Google Docs URL and asks to make it HTML.

## Pattern

1. Extract the document ID from the URL:
   - `https://docs.google.com/document/d/<DOC_ID>/edit...`
2. Try the public export endpoint first:
   - `https://docs.google.com/document/d/<DOC_ID>/export?format=html`
   - If it returns document HTML, Google Workspace OAuth is not needed.
   - If it fails with auth/permission, then fall back to the Google Workspace skill/setup or ask user for access/export.
3. Preserve content order by parsing paragraph/list elements from the export HTML. If `bs4` is unavailable, Python stdlib `html.parser` is enough for a simple ordered text extraction.
   - Practical fallback pattern: extract only `h1/h2/h3/h4/p/li` blocks, normalize whitespace, wrap consecutive `li` as `<ul>`, and generate section navigation from `h2` anchors.
   - Verification check: a large export size alone is not proof of access. Inspect for login/access markers (`show-login-page`, `Sign in`, `Request access`) and sample actual document headings before building.
4. Do not merely republish the raw Google export unless user asks for faithful conversion. For user-facing deliverables, turn the doc into a designed artifact:
   - clear title/hero
   - section navigation
   - cards/tables/callouts that match the content structure
   - print/PDF affordance if it reads like a memo/report/deck
5. Publish to the user-controlled webroot when appropriate:
   - `/var/www/html/<slug>/index.html`
   - Public URL: `https://hermest.gerbangduid.my.id/<slug>/index.html`

## Verification Pitfall

Always verify the exact URL you will send. On this VPS/nginx setup, the folder URL (`/<slug>/`) may return 403 externally even when `/index.html` returns 200. Prefer sending the full `/index.html` URL unless the folder URL is confirmed public.

Minimum verification:
- File exists and has non-trivial byte size.
- `http://localhost/<slug>/` or `/index.html` returns 200.
- Public `https://hermest.gerbangduid.my.id/<slug>/index.html` returns 200.
- If the first Doc URL fails with sign-in/access but the user sends a new `?usp=sharing` URL, rerun the public export immediately; don't assume the previous access failure still applies.

## Final Response

Keep it short: public link, what changed, and verification status. Mention caveat only if relevant (for example folder URL 403, full index URL works).