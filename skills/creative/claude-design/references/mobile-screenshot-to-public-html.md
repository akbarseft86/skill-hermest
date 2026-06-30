# Mobile screenshot → public HTML artifact pattern

Use this when the user sends a mobile app/social screenshot and asks to “bikin/pasang hasilnya di HTML”.

## What worked in session
- Treat the screenshot as a visual reference, not just an image caption. Use vision to extract:
  - screen ratio/frame
  - status bar details
  - layered structure (video/background + bottom sheet/modal)
  - exact visible text
  - typography scale, weight, line-height
  - accent colors and interaction elements
- Build a single self-contained HTML file with inline CSS/JS unless the user asks for a repo implementation.
- For Akbar/Hermest public artifacts, default publish path is `/var/www/html/<slug>/index.html` and public URL is `https://hermest.gerbangduid.my.id/<slug>/`.
- Verify in three layers before responding:
  1. file exists + expected text exists
  2. local nginx HTTP 200 (`http://127.0.0.1/<slug>/`)
  3. public HTTPS domain HTTP 200 (`https://hermest.gerbangduid.my.id/<slug>/`)
- Browser-check the artifact when possible and inspect DOM/console for core elements, especially title, heading/caption, and important sections.

## Design notes for mobile screenshots
- On desktop, center a realistic phone frame instead of stretching the mobile UI full-width.
- On mobile viewport, let the phone fill the viewport and remove outer rounded frame if needed.
- For screenshot reconstructions, include the visible UI affordances (status bar, close button, floating input, dividers, thumbnails) even if they are decorative.
- If the original UI has a fixed/floating input bar, add enough bottom padding to the scrollable sheet so important content is not permanently hidden.
- If first visual pass shows key lower sections hidden, reduce type/spacing or make the sheet scrollable; do not claim pixel-perfect if only faithful reconstruction was made.

## Final response pattern
Keep it short:
- public link
- file path
- verification status

Example:
`Sudah dipasang jadi HTML: https://hermest.gerbangduid.my.id/<slug>/ — file: /var/www/html/<slug>/index.html — verified HTTP 200.`