---
description: Generates an AI summary for Discovery calls from meeting data using the qualification framework in the summary recipe.
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

# Discovery call qualification fields

Slash command: /discovery-call-summary-recipe

## Step 1: Check the Discovery meeting type

Retrieve the Discovery meeting type from the project's meeting taxonomy. Confirm it exists and has notetaker autojoin enabled, both are prerequisites for the custom summary recipe to fire on real meetings. If the type doesn't exist, halt and prompt the user to run /meeting-types-taxonomy first.

## Step 2: Set what discovery captures

Configure the AI summary recipe for the Discovery meeting type. Extract structured fields: (1) Champion (name, title, level of buy-in (high/medium/low/none), explicit quotes showing commitment; (2) Pain) pain statement in prospect's own words, severity (must-solve/should-solve/nice-to-have), business impact discussed (revenue, cost, time, risk); (3) Current Solution (what they use today (vendor name + version), what works, what doesn't; (4) Decision Criteria) explicit criteria mentioned (price, features, integration, security, etc.), priority ranking if discussed; (5) Timeline (target go-live, urgency drivers; (6) Budget) explicit number, range, or signal (no budget signal = flag); (7) Next Step: what was agreed, with owner and due date. If a field is not discussed, return 'not_discussed' rather than guessing. Use the result of "Check the Discovery meeting type".

## Step 3: Check discovery quality by rep

Compose a Discovery call quality dashboard reading from the structured summaries: % of discovery calls with all 7 fields captured (target: 70%+); breakdown of most-frequently-missed fields (signals coaching opportunities); discoveries with 'no budget signal' flagged for follow-up; champion strength distribution across recent discoveries; pain severity distribution. Group by rep so managers can spot reps consistently missing qualification fields. Use the result of "Check the Discovery meeting type", "Set what discovery captures".
