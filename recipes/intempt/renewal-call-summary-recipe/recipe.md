---
description: Customizes AI summaries for Renewal calls, extracting usage patterns, expansion signals, churn risks, stakeholder confirmation and contract changes.
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
  - finance
  - media
---

# Renewal call summary fields

Slash command: /renewal-call-summary-recipe

## Step 1: Check the Renewal meeting type

Retrieve the Renewal meeting type from the meeting taxonomy. Confirm exists with notetaker autojoin enabled.

## Step 2: Set what renewals capture

Configure the AI summary recipe for the Renewal meeting type. Extract: (1) Usage Patterns (features the customer mentioned actively using vs. struggling with vs. never tried; (2) Expansion Signals) explicit interest in additional seats, modules, tier upgrades; budget signal for expansion (verbatim quotes); (3) Contraction Risks: explicit signals of churn intent, reduced usage, team changes affecting fit, competitor evaluation; (4) Stakeholder Confirmation: was the decision-maker present, did stakeholders confirm continued commitment, any champion changes (departures, role changes); (5) Contract Terms Discussion (pricing pushback, term length preference, payment terms, custom contractual asks; (6) Health Score Movement) sentiment shift from prior interactions; (7) Next Step: proposal needed, additional stakeholders to loop in, agreement to terms. Use the result of "Check the Renewal meeting type".

## Step 3: Track renewal risk and upside

Compose a renewal risk + expansion dashboard reading from summaries: (1) at-risk renewals (accounts with contraction signals or unresolved competitor evaluation, sorted by renewal date; (2) expansion-ready) accounts with explicit interest signals, sorted by ARR opportunity; (3) churn precursors (accounts where champion departed or stakeholders signaled disengagement; (4) renewal-call coverage) % of upcoming renewals where the call has happened (target: 100% by 60 days before renewal date); (5) win/loss patterns from past renewal-call summaries. Group by CSM owner. Use the result of "Check the Renewal meeting type", "Set what renewals capture".
