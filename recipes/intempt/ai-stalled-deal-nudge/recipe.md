---
description: Drafts a personalized re-engagement email for stalled deals using CRM deal context, leaving it for the rep to review and send.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# AI nudge for a stalled deal

Slash command: /ai-stalled-deal-nudge

## Step 1: Recall why it stalled

Create an AI-derived attribute 'nudge_context' on the Deal object, computed when the deal enters stalled status. Aggregates: (a) which stage stalled (Discovery / Demo / Proposal / Closing (each requires different nudge angle); (b) last meeting_summary if available) most useful is the 'next step' that was agreed and apparently not happening; (c) most recent objection raised (from call summaries); (d) any mentioned timeline / decision-window that may now be expiring; (e) replacement-stakeholder candidates if the original contact has gone quiet.

## Step 2: Draft a nudge that names it

Create a workflow firing when a deal is newly detected as stalled (consumer of the stalled-deal-detection workflow's output). Step sequence: (1) compute nudge_context; (2) generate AI-drafted nudge email using the context. Distinct from the template-based nudge in stalled-deal-detection: this version is HIGHLY personalized using meeting-summary specifics ('Last time we talked, you mentioned [verbatim objection]. Has anything changed on [specific blocker]?'); (3) save draft to rep's outbox; (4) create rep task labeled 'Review AI-drafted nudge: deal [name]' with the draft preview; (5) Slack DM with deal context. Always rep-reviewed-before-send. If deal stays stalled 14 days after first nudge draft sent, escalate to manager with manager-version draft (this needs your sign-off). Use the result of "Recall why it stalled".

## Step 3: Compare against a rep's own

Compose an AI nudge effectiveness dashboard: stalled-deals that received AI nudge drafts (vs. drafts not yet reviewed = backlog), reply rate to AI-nudge-drafted emails vs. baseline manual nudges, revival rate (deals stage-advanced after AI nudge), and ARR resurrected via this workflow. Compare to control: stalled deals where reps wrote their own nudge: typically AI-drafted personalized nudges win on reply rate by 1.5-2x. Use the result of "Recall why it stalled", "Draft a nudge that names it".
