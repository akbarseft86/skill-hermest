---
name: systematic-research
version: 1.0.0
description: "Class-level research methodology: systematic evidence collection, data quality tiering, multi-source synthesis, and transparent limitation reporting. Covers three domains — tools/system comparison, competitor social media intelligence, and financial/industry deep research."
when_to_use: User asks to compare systems, analyze competitors, assess financial/bank health, or do any evidence-gathering task that demands systematic multi-source collection and transparent reporting.
---

# Systematic Research — Core Methodology

## Core Principle: Read Before Concluding

Never answer from title, name, or summary alone. Read actual content — source files, docs, code, feeds — before making evidence-based claims.

## The Research Hierarchy

All claims MUST be labeled with their data quality tier:

```
VERIFIED  ── Seen with own eyes. Source accessed directly. Format/numbers confirmed.
INFERRED  ── From search snippets, cache, metadata. Format UNKNOWN. Cross-checkable but not primary.
ASSUMED   ── Guessing based on domain knowledge. NOT data. Never present as fact.
```

**Golden rule:** If you haven't seen the source, you don't know the data. Don't fill gaps with theory.

## The Research Workflow

### Step 1: Map the Landscape
- Identify exactly what's being researched. Get names, versions, locations.
- Confirm scope if ambiguous.

### Step 2: Search Broadly, Not Narrowly
- Do multiple queries across different source types.
- Do not cap research to a tiny fixed website set.
- Weight by reliability: Official/primary > credible media > user chatter.
- For hotel/accommodation research, do **not** limit discovery to OTAs. Search for official/direct websites, independent booking engines, small guesthouse sites, hotel groups, and Google/Maps-visible properties that may not rank on OTA lists. If the user wants manual checking, include broad candidates with source links and uncertainty labels instead of prematurely filtering them out.

### Step 3: Read Actual Content
- Load skills, browse repos, inspect feeds. Not just titles/descriptions.
- Examine structure, provenance, and actual mechanisms.

### Step 4: Synthesize Across Sources
- Compare dimension by dimension (feature parity, gaps, depth, provenance).
- Distinguish between claimed capability and actual implementation.
- Check for hidden assumptions or outdated docs.

### Step 5: Conclude with Evidence
- Lead with the direct answer. Answer plainly first, evidence second.
- Support EVERY claim with specific evidence or a quality-tier label.
- Note trade-offs, context, and limitations transparently.

## Domain Subsections

This skill covers three research domains with specialized methodologies:

### A. Tools/System Comparison
For comparing frameworks, tools, platforms, or approaches.
- Pricing comparison (fetch live, calculate both normal and promo costs)
- Per-unit cost in user's currency
- Plan access restrictions
- See `references/comparative-analysis-detailed.md`

### B. Competitor Social Media Intelligence
For analyzing competitor social media presence and content strategy.
- ATM methodology (Ambil, Tiru, Modifikasi — copy strategy, not surface)
- Instagram data collection via Apify actors when direct browser access is blocked
- Per-post classification (format, hook, offer, CTA, product, visual)
- Minimum 20–30 post sample for pattern detection
- See `references/competitive-intelligence-detailed.md`

### C. Financial/Industry Deep Research
For bank health assessments, deposit safety, or industry risk analysis.
- Minimum research checklist (capital, asset quality, liquidity, profitability)
- Heuristic interpretation tables (NPL, LCR, CAR thresholds)
- Historical-failure comparison workflow
- Leading vs lagging indicators
- Two-layer delivery (analyst report + messaging summary)
- See `references/financial-industry-research-detailed.md`

### D. Lodging / Accommodation Audit
For hotel, villa, Airbnb, OTA, or direct-booking research that will become a user-facing shortlist/dashboard.
- Treat scraped Airbnb/OTA rows as candidates for manual checking, not final facts.
- Preserve provenance/source sections when adding new candidates; do not delete earlier lists.
- Add direct links, area labels, visible price, rough currency conversion, rating/review count, and uncertainty notes.
- Mark unverified price, final fees, exact distance, and map pin as `CEK ULANG` rather than overclaiming.
- See `references/airbnb-lodging-audit.md`

## Anti-Patterns (All Domains)

- ❌ **Title-only conclusion**: Comparing by name alone. Read content, not labels.
- ❌ **README-level paraphrasing**: READMEs are marketing, not evidence.
- ❌ **Assumption-based claims**: "X does Y" without verification.
- ❌ **False symmetry**: Forcing equal-depth comparison when one source is derived from another.
- ❌ **Forced balance**: Presenting "each has strengths" when the comparison is genuinely one-sided.
- ❌ **False certainty**: Saying "safe" without caveats about what data is/isn't available.
- ❌ **Single-source over-reliance**: One article does not prove a trend.

## Pitfalls

- **Provenance hiding**: When two systems share ideas, one may be a port/fork. Check metadata.
- **Depth illusion**: Longer doesn't mean better. Read actual mechanism, not word count.
- **Missing data**: If you can't access a source, say so — don't fill gaps.
- **Scope creep**: Stay focused on what was asked. Don't add unrelated systems.
- **Neglecting negatives**: Report flaws and missing pieces honestly.
- **Lagging-only analysis**: For monitoring tasks, leading indicators (operational complaints, product changes, unusual reports) give faster warnings than quarterly ratios.

## Verification Checklist

- [ ] All sources accessed directly where possible
- [ ] Data quality tier labeled for each claim
- [ ] Multi-source synthesis done (not one source)
- [ ] Direct answer first, evidence second
- [ ] Limitations and caveats reported transparently
- [ ] Anti-patterns checked: no assumption-based claims

## References

- `references/comparative-analysis-detailed.md` — full methodology for tools/system comparison including pricing analysis
- `references/competitive-intelligence-detailed.md` — full competitor social media research workflow with ATM methodology
- `references/instagram-apify-actors.md` — notes for using Apify actors when Instagram direct scraping is blocked
- `references/financial-industry-research-detailed.md` — full workflow for Indonesian bank health and deposit safety research
- `references/krom-century-red-flags.md` — worked example: Krom Bank vs Bank Century comparison
- `references/bank-monitoring-early-warning.md` — early-warning monitoring framework for ongoing bank radar
- `references/superpowers-vs-hermes-skills.md` — worked example: comparative analysis between skill systems
