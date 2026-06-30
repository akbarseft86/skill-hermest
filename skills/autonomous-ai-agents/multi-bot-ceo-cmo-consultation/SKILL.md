---
name: multi-bot-ceo-cmo-consultation
description: Consult a separate Hermes instance/profile (for example a CMO bot) from the current agent, then synthesize the remote output into a final CEO-style recommendation or product plan. Use when the user wants Hermest to 'discuss with CMO', compare perspectives, or turn notes/transcripts into monetizable offers.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Multi-Bot CEO/CMO Consultation

Use this skill when:
- the user asks Hermest to "diskus sama CMO"
- the current bot should act as CEO/strategist while another Hermes home/profile acts as CMO/executor
- you need a second-pass commercial/product angle on notes, transcripts, or rough ideas
- you want a grounded way to consult another live bot without pretending they talked if they did not

## Core idea
Use a separate Hermes instance by setting `HERMES_HOME` explicitly and running a one-shot `hermes_cli.main chat -q ...` query. Then synthesize that output in the current conversation.

This is better than roleplaying both sides in one answer when the user explicitly wants the other bot involved.

## Proven command pattern
For a dedicated CMO bot living under `/root/.hermes-cmo`:

```bash
HERMES_HOME=/root/.hermes-cmo /root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main chat -q "<prompt>"
```

Run from a stable workdir such as:
- `/root/.Hermes/workspace`

Use a generous timeout like `300` seconds.

## Workflow

### 1. Extract the actual ask first
Before consulting the other bot, reduce the user ask into a crisp CMO brief.

Examples:
- "User wants rush cash in 7 days, legal, low capital, leveraging Telegram/WA/Threads and current AI/bot capabilities. Give 3 monetization options and pick the fastest."
- "Analyze this transcript and propose 1 digital product that can actually be sold in Indonesia."

### 2. Query the CMO instance directly
Use a direct prompt that forces structured output.

Good prompt shape:
- define the role explicitly: `Kamu adalah Hermest CMO`
- define market/context explicitly: Indonesia, UMKM, affiliate, etc.
- force exact sections: target market, problem, offer, deliverables, price, CTA, speed-to-cash
- request concise, practical Indonesian output

### 3. If needed, do a second CMO pass for assets
After choosing a direction, ask a follow-up one-shot query for execution assets such as:
- pricing tiers
- DM scripts
- follow-ups
- closing scripts
- deliverables checklist
- niche list
- product folder structure
- offer copy

This two-pass pattern worked well:
1. first pass = options and recommendation
2. second pass = assets needed to sell/build it this week

### 4. Synthesize as CEO
Do not dump raw subprocess output. Convert it into:
- one chosen recommendation
- blunt rationale
- adjusted pricing if needed for reality/speed
- next-step plan the user can execute now

Important: if the remote CMO gives overly ambitious packaging or pricing, say so plainly and adjust. Example experiential finding: for rush-cash sales, heavy agency-style pricing can be too high for fast close if proof is weak; a lower-ticket entry offer may be more realistic.

### 5. Save final structured output if useful
If the result is a reusable artifact (product blueprint, launch plan, offer doc), write it to a file in the workspace.

Example:
```bash
/root/.Hermes/workspace/output-produk-digital-real.md
```

## Prompt templates

### A. Rush-cash monetization consult
```text
Kamu adalah Hermest CMO. User Indonesia ingin RUSH CASH secepat mungkin, legal, modal kecil, memanfaatkan Telegram/Threads/WA dan kemampuan AI/bot yang sudah ada. Tugasmu: berikan 3 opsi monetisasi tercepat dalam 7 hari ke depan. Untuk tiap opsi, tulis: target market, pain point, offer, deliverables, harga awal, cara closing tercepat, 3 hook konten, CTA, dan estimasi speed to cash. Lalu pilih 1 prioritas paling realistis untuk cash tercepat. Jawab singkat, tegas, sangat praktis, tanpa teori panjang.
```

### B. Follow-up for closing assets
```text
Lanjutkan dari prioritas #1 tadi. Sekarang buat aset closing yang langsung bisa dipakai hari ini. Output wajib: 1) nama offer, 2) paket harga 3 tier, 3) DM cold outreach 3 versi, 4) script follow-up kalau tidak dibalas, 5) script closing saat prospect tertarik, 6) checklist deliverables 24 jam pertama, 7) daftar 10 niche paling enak disasar dulu di Indonesia. Jawab dalam bahasa Indonesia, singkat, tegas, siap copy-paste.
```

### C. Transcript-to-product consult
```text
Kamu adalah Hermest CMO. Analisis transkrip materi berikut lalu usulkan 1 produk digital yang REAL, bisa dijual ke market Indonesia, berdasarkan inti materi itu. <insert concise summary of transcript>. Output wajib: nama produk, siapa target marketnya, problem yang dibayar, promise utama, isi modul/komponen produk, format produk, harga jual awal, alasan kenapa orang mau beli, dan kenapa produk ini lebih real daripada sekadar course umum. Jawab ringkas tapi tajam dalam bahasa Indonesia.
```

### D. MVP packaging follow-up
```text
Lanjutkan produk tadi. Sekarang buat output MVP yang bisa benar-benar dijual minggu ini. Output wajib: 1) deliverables final yang harus ada di produk versi v1, 2) struktur folder/isi produk, 3) outline PDF playbook, 4) outline Notion template, 5) bonus yang paling masuk akal, 6) copy offer singkat untuk landing/DM, 7) siapa yang TIDAK cocok beli. Jawab praktis, siap eksekusi.
```

## Practical findings from experience
- When the user says some version of "diskus sama CMO" or "buatkan bagaimanapun caranya", it is acceptable to actually consult the alternate Hermes home rather than only simulating dialogue.
- The command above returns the full CLI banner and formatted response. You must extract the useful content and ignore the decorative wrapper.
- Skill lookup can be inconsistent by category prefix in some runtimes. If `skill_view("category:name")` fails, retry with the bare skill name.
- For strategy/product tasks, summarize noisy source material first rather than pasting a raw messy transcript verbatim into the CMO prompt.
- CEO synthesis matters: the remote CMO may give workable ideas but still need pricing/downscoping for a faster close.

## Pitfalls
- Do not claim the bots talked if you did not actually run the other instance.
- Do not send the user raw terminal output unless they asked for it.
- Do not over-trust first-pass pricing. Recalibrate for the user's likely speed-to-cash goal.
- Do not turn the result into theory. The user usually wants actionable deliverables.

## Success criteria
- A real alternate Hermes instance was queried
- Output came back structured enough to compare or package
- Final answer is decisive, practical, and tailored to the user goal
- If relevant, a reusable artifact file was created in the workspace
