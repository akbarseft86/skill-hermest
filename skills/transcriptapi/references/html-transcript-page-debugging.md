# Debugging Generated Transcript HTML Pages

Use when a prior TranscriptAPI batch generated an HTML page and a later task needs to re-parse, analyze, or augment that page.

## Durable lesson

Do not assume the saved JSON file is still the source of truth. Verify the actual data-bearing artifact before analysis:

1. Check the HTML page for embedded transcript blocks.
2. Count entries, successful transcript blocks, and error blocks.
3. Only then synthesize summaries/titles or update the page.

## Robust extraction pattern

Generated transcript pages may contain entries shaped like:

```html
<div class="entry" id="ent-...">
  ...
  <div class="transcript-text" id="text-...">FULL TRANSCRIPT</div>
</div>
```

Pitfall: `transcript-text` may have extra attributes (`id=...`). Do **not** use a regex that only matches `<div class="transcript-text">` exactly.

Safer transcript regex inside an already-isolated entry:

```python
re.search(r'<div class="transcript-text"[^>]*>([\s\S]*?)</div>', entry_html)
```

## Robust entry isolation

Do not rely on comments like `<!-- /entry -->`; generated pages may not include them.

Safer approach:

1. Find all opening entry positions:
   ```python
   positions = list(re.finditer(r'<div class="entry(?:\s+error)?" id="(ent-[^"]+)">', html))
   ```
2. For each entry, slice from this opening position to the next entry opening position.
3. For the last entry, use simple div-depth counting or slice to the end of the known transcript section.

This avoids brittle assumptions about closing comments or exact nesting.

## Verification checklist before claiming analysis is complete

Print and inspect:

- total entry positions found
- count of non-error entries
- count of error entries
- transcript character length per entry
- list of video IDs/titles for error entries

Example acceptable proof:

```text
Found 51 entry positions
OK: 46, Error: 5
1. ✅ [2023] Title... | 94851 chars | VIDEO_ID
...
30. ❌ [2025] Title... | 94 chars | VIDEO_ID
```

If a generated JSON contains downloader/bot-detection errors while the HTML contains full transcripts, treat the HTML as the data source and overwrite/regenerate the JSON from the verified HTML extraction.

## Communication style for this class of task

When the user asks to “debug teliti / senior programmer / make no mistake,” respond with concise root-cause proof, not broad explanations. State:

1. exact bug,
2. exact fix,
3. verification counts,
4. remaining unavailable items.

Do not say titles/analysis are complete until the HTML or output artifact has actually been updated and verified.