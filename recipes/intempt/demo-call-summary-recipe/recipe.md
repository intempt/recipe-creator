---
description: 'Built in Demo call summary recipe: one of nine fixed recipes that summarizes demo meetings.'
author:
  first_name: Sid
  last_name: Chaudhary
  job_title: Founder & CEO
  avatar: https://cdn.intempt.com/assets/author-profile-pics/sid.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Demo call summary fields

Slash command: /demo-call-summary-recipe

## Step 1: Check the Demo meeting type

Retrieve the Demo meeting type from the meeting taxonomy. Confirm it exists with notetaker autojoin enabled. If absent, halt and direct the user to /meeting-types-taxonomy.

## Step 2: Set what the demo summary captures

Configure the AI summary recipe for the Demo meeting type. Extract structured fields: (1) Features Demoed: list of product features shown, with engagement signal per feature (attendee asked questions / silent / pushed back); (2) Questions Asked (list of attendee questions with category (capability, integration, pricing, security, onboarding, other); (3) Objections) list of objections raised verbatim, with category (price/timing/competition/feature-gap/authority/trust) and resolution status (handled/parked/unresolved); (4) Technical Concerns: specific technical questions or blockers (integrations needed, data residency, SSO, compliance); (5) Decision-Maker Signal (was a decision-maker on the call, were they engaged; (6) Follow-up Requested) what attendee asked for (case study, trial, technical demo, custom proposal, references); (7) Next Step: what was agreed. Use 'not_discussed' for missing fields rather than guessing. Use the result of "Check the Demo meeting type".

## Step 3: Track what demos reveal

Compose a demo insights dashboard reading from structured summaries: top 10 features by demo frequency (which features sell themselves vs. need more pitch); top 10 objections by frequency (objection-handling content priorities); decision-maker attendance rate (low % = multi-threading problem); follow-up-requested distribution (what does the market actually want); and most-asked technical concern categories (product / engineering input). Group by rep and time period. Use the result of "Check the Demo meeting type", "Set what the demo summary captures".
