# Domain A: Tools/System Comparison — Detailed Methodology

Absorbed from: `comparative-analysis` (archived)

## Trigger Conditions

Use this when the user:
- Asks to compare, contrast, or evaluate systems/tools
- Says "bandingkan X dan Y" or "cek yang ini vs yang itu"
- Asks "mana yang lebih baik" or "mana yang lebih lengkap"
- Requests evaluation with "cek dalamnya" (check the depth)
- Wants to understand differences between two or more things

## The Process

### Step 1: Map the Landscape

Identify exactly what is being compared. Get the names, versions, and locations of each item. Confirm scope with the user if ambiguous.

### Step 2: Read Actual Content (THE CORE STEP)

For each system/tool:
1. **Load the skill or source** — use `skill_view()` for skills, browse/curl for external projects
2. **Read the full content** — not just the title/description
3. **Check provenance metadata** — author, version, `adapted from` notes, attribution fields
4. **Examine the structure** — files, directory layout, supporting references/templates/scripts
5. **Identify the actual mechanism** — what does it DO, not what does it SAY it does

### Step 3: Compare Dimension by Dimension

Create a comparison table covering:
- **Feature parity** — what each has
- **Implementation differences** — how they approach the same problem
- **Gaps** — what X has that Y doesn't (and vice versa)
- **Provenance** — is one derived from the other?
- **Depth** — which is more thorough: rules, anti-patterns, verification steps, warnings
- **Integration** — how each connects to the broader ecosystem

### Step 4: Verify Claims

- Cross-reference README statements with actual file contents
- Check for hidden assumptions or outdated docs
- Distinguish between claimed capability and actual implementation
- If a claim seems too good to be true, verify it from raw source

### Step 5: Conclude with Evidence

- Present a clear verdict
- Support EVERY claim with specific evidence (file paths, line ranges, metadata fields)
- Note trade-offs and context
- Factor in user preferences (thoroughness vs speed, etc.)
- Propose concrete action items if applicable

## Pricing Comparison (Special Case Extension)

When comparing pricing (subscription tiers, credits, per-unit costs):

### Step 1: Fetch Live Data (NEVER rely on session memory)
- Navigate to the actual pricing page. Session memory is unreliable for pricing.
- Extract: plan names/prices, credit allowances, per-unit costs, active promos, model access restrictions.

### Step 2: Calculate Both Methods
1. **Normal credit pricing**: Plan price ÷ credits ÷ per-generation cost
2. **Promo/bundle pricing**: Plan price ÷ estimated generations from promo
Present BOTH in a table. Users commonly reference the promo method — verify which before correcting.

### Step 3: Calculate Per-Unit Cost in User's Currency
Convert USD → IDR using a live exchange rate. Show price per plan, credits per plan, generations per plan, cost per generation in IDR.

### Step 4: Note Model Access Restrictions
A plan having credits does NOT mean it can use every model. Explicitly note which models are available/excluded per plan.

## Example Table (from Higgsfield Seedance 2.0 comparison)

| Plan | Price/mo | Credits | Seedance 2.0 access | Cost/video (promo) | Cost/video (normal) |
|------|----------|---------|---------------------|--------------------|--------------------|
| Starter | $15 | 200 | Fast only | ~Rp2.000 | ~Rp24.000 |
| Plus | $39 | 1.000 | Full + Fast | ~Rp700 | ~Rp15.000 |

## Anti-Patterns

- **Title-Only Comparison**: Comparing by name alone. "System X has debugging, System Y has debugging, therefore they're equal."
- **README-Level Paraphrasing**: Copying descriptions from README pages. READMEs are marketing, not evidence.
- **Assumption-Based Claims**: Claiming "X does Y" without source verification.
- **False Symmetry**: Forcing equal-depth comparison when one system is derived from the other.
- **Forced Balance**: Presenting "each has strengths" when genuinely one-sided.
