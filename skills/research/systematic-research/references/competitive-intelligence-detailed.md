# Domain B: Competitor Social Media Intelligence — Detailed Methodology

Absorbed from: `competitive-intelligence` (archived)

## Trigger Conditions

Use this when the user asks you to:
- Analyze competitor social media accounts
- Identify content formats, hooks, offers, and CTAs used by competitors
- Create competitor content audits and strategy recommendations
- Apply ATM methodology (Ambil, Tiru, Modifikasi)

## Data Quality Hierarchy

```
VERIFIED ── Seen with own eyes. Feed browsed. Format confirmed.
INFERRED ── From search snippets, cache, metadata. Format UNKNOWN.
ASSUMED  ── Guessing based on niche knowledge. NOT data.
```

**NEVER present inferred or assumed data as verified fact.**

## ATM Methodology (Ambil, Tiru, Modifikasi)

### ✅ Yang benar di-ATM:
- **Strategy** — offer structure, positioning, funnel, value prop, closing mechanism
- **Angle** — pain points, hooks, audience targeting
- **CTA pattern** — DM keyword, WhatsApp, comment keyword
- **Offer structure** — outright vs subscription, price anchoring, tenor

### ❌ Yang TIDAK boleh di-ATM buta:
- Format postingan (carousel / reels / single image) — unless VERIFIED
- Visual style blindly — adapt to own brand
- Copy-paste caption — always rewrite in your voice

**ATM = copy the strategy, not the surface.**

## Research Workflow

### Phase 1: Data Collection

#### Step 1 — Try direct access first
```python
browser_navigate("https://www.instagram.com/competitorhandle/")
# If 403/login wall → proceed to step 2
```

#### Step 2 — Try alternative viewers
- `ddinstagram.com/handle`
- `imginn.com/handle`
- `pixwox.com/handle`
- `gramhir.com/handle`

Most are blocked from VPS. Say so honestly.

#### Step 3 — Try search engines
Query patterns:
- `site:instagram.com/p competitorhandle`
- `site:instagram.com/reel competitorhandle`
- `"competitorhandle" harga produk`

These return snippets only — metadata, NOT format data.

#### Step 4 — Try Apify actors (if APIFY_TOKEN available)
1. Search Apify Store first to find working actors — slugs may change.
2. Run a small test (3 items) to verify before full scrape.
3. Use the actor ID returned by Store search, not guessed slugs.
4. Fetch dataset with `clean=true`.
5. Validate returned posts actually belong to the requested handle/niche (check `ownerUsername`/`user.username`, caption coherence).
6. If user says "cek di atas" / "kan udah semua", recover context from screenshots/session recall before asking again.

#### Step 5 — If ALL blocked, be honest
- "I cannot verify the visual feed from this VPS environment."
- "What I have is metadata/search snippets: [list]."
- "What I DON'T have: format data, visual style, post-by-post classification."
- Offer alternatives: user provides screenshots, or work with available data.

### Phase 2: Classification

For each post you CAN see, classify:
```
Format:      single_image / carousel / reel / video
Hook type:   problem / curiosity / stat / question / relatable
Offer:       price / promo / free trial / consultation / bundle
CTA:         DM keyword / WhatsApp / link in bio / comment
Product:     which specific product variant
Visual:      flyer / lifestyle / demo / testimonial / screenshot chat
```

Minimum sample: 20–30 posts for reliable pattern detection.

### Phase 3: Pattern Recognition

After classifying the sample:
1. **Format dominance** — what % of posts is each format?
2. **CTA consistency** — is there one CTA they repeat?
3. **Offer frequency** — what offer appears most?
4. **Product focus** — which product gets most posts?
5. **Posting cadence** — how often do they post?

### Phase 4: Derive Recommendations

Only AFTER Phase 1–3, answer:
- PRIMARY format = competitor's dominant format (verified)
- PRIMARY offer = adapted from their winning offer
- Posting frequency = match or exceed
- CTA pattern = test their proven model

## The Golden Rule

> **If you haven't seen the feed, you don't know the format.**
>
> Theories are secondary. Competitor evidence is primary. When they conflict, evidence wins. When there IS no evidence, say so.

## Reporting Template

```
## Data Quality
- Visual feed verified: Yes/No/Partial
- Source: Direct access / Search snippets / User screenshots
- Limitation: [what couldn't be confirmed]

## Per-Post Classification
| # | Format | Hook | Offer | CTA | Notes |
|---|--------|------|-------|-----|-------|

## Format Dominance
- [Format]: [count] posts ([XX]%)

## ATM Recommendations
From verified data: [specific formats/angles to copy]
Not yet verified: [what we're still unsure about]
```

## Pitfalls

### DO NOT
- ❌ Say "competitor uses X format" unless you SAW the feed
- ❌ Recommend format based on theory when data is incomplete
- ❌ Present search snippets as format evidence
- ❌ Overclaim scraping capability when tools are blocked
- ❌ Copy format without understanding offer/funnel behind it

### DO
- ✅ Label every claim: "verified" / "from snippets" / "assumption"
- ✅ Be transparent when you can't access Instagram from server
- ✅ Ask user for screenshots when stuck
- ✅ Let competitor data drive format — not your intuition
