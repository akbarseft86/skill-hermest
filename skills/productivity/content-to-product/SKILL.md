---
name: content-to-product
description: "Transform educational/training content (transcripts, webinar recordings, articles) into digital product concepts with marketable titles. Use when user has a body of educational content — video series, podcast episodes, training modules — and wants to monetize it as a digital product (course, workbook, ebook, membership). Covers batch content analysis, theme extraction, title creation from the '5 bombastic titles' formula."
version: 1.0.0
tags: [content, product, monetization, titles, marketing, digital-product]
---

# Content to Digital Product

Transform a body of educational/training content into marketable digital product concepts with punchy, sellable titles.

## When to Use

Use this skill when the user has:
- A library of video transcripts / webinar recordings / podcast episodes
- Training course content (recorded sessions, modules)
- Blog posts / articles on a specific topic
- Any collection of educational material they want to monetize

The output is typically: 5 high-impact product titles + brief descriptions per title + an HTML/landing page presenting the products.

## The Workflow

### Step 1: Load & Understand the Content

```python
# Load all content into a list
entries = [{"id": "...", "title": "...", "year": "...", "text": "..."}]
```

For each piece of content, note:
- **Core teaching**: What is the single most important lesson?
- **Problem solved**: What specific pain point does this address?
- **Emotional hook**: What feeling does this content evoke?
- **Target audience**: Who is this for?

### Step 2: Analyze Per Content (Batch via Subagent or Direct)

Analyze each transcript/content piece individually:

```python
# Output structure per item
{
  "video_id": "...",
  "year": "...",
  "title": "...",
  "inti": "2-3 sentence summary of core message, problem solved, and key technique taught"
}
```

**Key questions for each item:**
- What is the MAIN problem this addresses?
- What technique/solution is taught?
- What transformation does the user experience?
- What makes this different from generic advice?

**Pitfall:** If content is in transcript form and you already have the transcripts locally, DO NOT ask subagents to re-fetch from YouTube. They will overwrite your data file. Either:
- (a) Pass transcript text directly in subagent context (but watch token limits — 46 transcripts × 60K chars ≈ 2.8M chars is too much)
- (b) Save transcripts to unique subagent-scoped files
- (c) Use `exec_code` to batch-read and process in the parent agent context

### Step 3: Identify Recurring Themes

After all content is analyzed, aggregate across all entries:

```
DOMINANT THEMES (rank by frequency):
1. Theme A — appears in X/Y videos → key insight
2. Theme B — appears in X/Y videos → key insight
3. Theme C — appears in X/Y videos → key insight
...
```

Group themes into categories:
- **Pain points**: What problems keep appearing? (e.g. anxiety, overthinking, physical ailments)
- **Techniques**: What methods/methodologies are taught? (e.g. setup phrases, tapping, tune-in)
- **Transformations**: What outcomes do users achieve? (e.g. instant healing, abundance, emotional freedom)
- **Spiritual/Emotional**: What deeper layer is addressed? (e.g. surrender, trauma, acceptance)

### Step 4: Map Themes to Product Angles

For each dominant theme cluster, identify a product angle:

| Theme Cluster | Product Angle | Target Audience |
|---|---|---|
| Setup phrases | "Rahasia Kalimat" — quick access tool | Beginners who struggle with wording |
| Overthinking/anxiety | "Zero Overthinking" — mental reset | High-stress individuals |
| Emotional trauma | "Emotional Freedom" — deep healing | Those with past trauma |
| Physical healing | "Instant Healing" — specific ailments | People with health issues |
| Abundance | "Wealth Flow" — mindset + action | Entrepreneurs, salespeople |

**Core principle:** Each product should solve ONE specific, visceral problem. Don't mix healing and abundance in one product unless the content framework explicitly supports it.

### Step 5: Create 5 Bombastic Titles

Use the **MAGIC formula** (adapted from $100M Offers):

**M** — Make a Magnetic Reason Why
**A** — Announce Your Avatar
**G** — Give Them a Goal
**I** — Indicate a Time Interval
**C** — Complete with a Container Word

**Container words (bombastis/Indonesia-friendly):**
- Rahasia / Formula / Sistem / Blueprint / Kunci / Mastery / Puncak / Ledakan
- PRO / MAX / X / Zero / Instan / Power / Ultimate

**Title creation criteria:**
1. **Stops the scroll**: Grabs attention immediately
2. **Solves a problem**: Tells the prospect what they'll get
3. **Feels urgent**: Creates FOMO or desire
4. **Specific not vague**: Numbers, timeframes, outcomes
5. **True to content**: Based on what's actually in the source material

### Step 6: Package with Descriptions

For each of the 5 titles, provide:

```markdown
## PRODUCT N: [BOMBASTIC TITLE]

**Super hook:** 1-line hook that explains the product (max 15 words)

**Apa yang kamu dapatkan:**
- Benefit 1 (specific, outcome-focused)
- Benefit 2 (specific, outcome-focused)
- Benefit 3 (specific, outcome-focused)

**Untuk siapa:**
- Target persona 1
- Target persona 2

**Inspirasi dari konten:** Link/X video references dari konten sumber
```

### Step 7: Present in HTML

Update/create an HTML page with:

1. **Hero section**: "5 Produk Digital dari X Pelatihan" atau brandable
2. **Product cards**: Each product as a distinct card/section with:
   - Bombastic title (large, accent color)
   - Hook (subtitle)
   - Benefits (checklist)
   - Target audience
   - Source content links (expandable)
3. **Theme analysis section**: Visual breakdown of themes found (bar chart or list)
4. **Mobile-responsive**: Must work on phone screens
5. **Color scheme**: Dark theme (#0f0f0f bg, bright accent color, white text)

See `references/html-template.md` for the base template.

## Target Framework (for Indonesia market)

When targeting Indonesian users with SEFT/islamic-spiritual content:

- **Tone**: Confident, transformative, slightly mystical but grounded
- **Language**: Indonesian, with natural mix of English buzzwords sparingly
- **Pain points to hit**: Anxiety (cemas), overthinking, physical pain (GERD, insomnia, diabetes), financial blockage, family trauma, lack of confidence
- **Trust triggers**: Testimoni, praktik langsung, spiritual (doa, pasrah Allah), ilmu dari trainer/praktisi berpengalaman
- **Price anchoring**: Compare to therapy costs, medical bills, lost productivity

## Common Pitfalls

1. **Mixing healing and abundance in one product**: The content repeatedly warns that you must heal first before pursuing abundance. Don't sell a product that promises both in one shot unless the content explicitly supports it.
2. **Too many benefits dilutes the message**: Pick ONE core transformation per product, not everything.
3. **Generic titles without substance**: Every bombastic claim must be traceable back to actual content. If you promise "sembuh dalam 1 sesi", there must be a transcript proving it.
4. **Subagent data corruption**: When using `delegate_task` for parallel analysis, subagents share the filesystem. If you saved transcripts to `/root/transcripts_data.json`, a subagent that writes to that path will overwrite your data. Use unique paths per subagent (e.g. `/root/subagent_1_output.json`) and instruct them not to write to parent-controlled paths.
5. **Token limits with subagents**: 46 transcripts × ~7K chars each = ~322K chars. You can't pass all in one subagent context. Batch: 9-12 per subagent.
6. **Forgetting content without transcripts**: Some videos have no captions. Mark these clearly and don't skip tracking them or the final count will be wrong.

## Verification Checklist

After completing the workflow:

- [ ] All content items analyzed (note how many failed/skipped)
- [ ] Theme frequency counted
- [ ] Each product title maps to actual content themes
- [ ] HTML page renders correctly on mobile
- [ ] HTML includes source links back to content
- [ ] HTML is served publicly (e.g. `/var/www/html/`)
- [ ] User can copy/share individual product descriptions
