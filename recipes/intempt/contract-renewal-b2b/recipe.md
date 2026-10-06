---
id: contract-renewal-b2b
title: B2B contract renewal
slash_command: /contract-renewal-b2b
group: Journeys
owner: intempt
curator: somya
summary: >-
  For B2B accounts approaching contract end, run a renewal journey at 90, 60, and 30 days to the enrolled
  profile.
description: >-
  For B2B accounts approaching contract end, enroll a profile and send renewal emails at 90, 60, and 30 days
  before expiration. Tailor content using account and role attributes, and track engagement and health in a
  dashboard. The journey messages one enrolled profile; it does not switch recipients per touch.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  industry:
    - ai
    - b2b-saas
    - finance
  vertical: []
  complexity: advanced
  executionMode: live
  tags:
    - b2b-renewal
    - multi-stakeholder
    - enterprise
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new segment, from step 1 "Find renewals inside 90 days"
    - A new attribute, from step 2 "Read the renewal health"
    - A new designed email, from step 3 "Write one email per role"
    - A new journey, from step 4 "Reach each stakeholder in turn"
    - A new dashboard, from step 5 "Forecast the renewal book"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find renewals inside 90 days
    summary: >-
      Active enterprise and mid market accounts whose contract ends between 30 and 90 days from now. Each
      one has several contacts, and the journey reaches them by role.
    builds: segment
    description: >-
      Build a segment 'Upcoming B2B contract renewals - next 90 days' capturing accounts where contract_end_date
      is between 30 and 90 days from now AND account_tier is enterprise or mid-market AND subscription_status
      is active. Each account in the segment has multiple touched users, the journey reaches different
      contacts at the account with role-appropriate messaging.
  - id: s2
    title: Read the renewal health
    summary: >-
      Taken when the account enters the renewal window: whether usage grew, flattened or fell over 12
      months, what outcomes and ROI you can show, whether the champion is still in role and the budget
      holder is reachable, the tone of six months of support tickets, and any competitor mentions in meeting
      notes.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'renewal_health_snapshot' on the Account object, computed at renewal-window
      entry. Aggregates: (a) usage trajectory over past 12 months (growing / flat / declining); (b) value
      delivered (key outcomes, milestones reached, ROI metric if tracked); (c) stakeholder health: champion
      still in role and engaged? economic buyer reachable? new stakeholders identified?; (d) support ticket
      sentiment over past 6 months; (e) competitor mentions in any meeting summaries. Output: composite
      health score + structured content for the renewal emails. Use the result of "Find renewals inside
      90 days".
    dependsOn:
      - s1
  - id: s3
    title: Write one email per role
    summary: >-
      The champion gets a value recap of the year and a request to help line up the renewal conversation.
      The budget holder gets business value, ROI and terms. Security or IT gets documentation and certification
      updates. At 30 days everyone gets a consolidated reminder with the proposed terms attached. Business
      formal, not marketing chat.
    builds: email_html
    description: >-
      Generate role-tailored renewal content. (a) User-champion (Day 90): 'Quick value-recap of the past
      year (what's working and what's next') focuses on product wins, usage stats, asks for help to coordinate
      the upcoming renewal conversation. (b) Economic buyer (Day 60): 'Your team's renewal is up in 60
      days (let's connect on terms') focuses on business value, ROI, growth opportunity, available terms.
      (c) IT/security stakeholder if known (Day 60): 'Security/compliance update for your upcoming renewal':
      proactive on documentation, certifications, any changes. (d) Late reminder (Day 30): consolidated
      reminder to all stakeholders with proposed contract terms attached. Tone: business-formal, value-substantive,
      not marketing-chatty. Use the result of "Find renewals inside 90 days", "Read the renewal health".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Reach each stakeholder in turn
    summary: >-
      Champion at 90 days, budget holder at 60, security at 60 in parallel, and all of them at 30. The
      moment a CSM or AE books a renewal meeting the journey pauses and the human takes over. Accounts
      with weak health or any churn signal also get an urgent CSM task at day 90.
    builds: journey
    description: >-
      Build a multi-touch multi-stakeholder journey triggered at renewal-window entry. Each touch goes
      to a DIFFERENT contact at the account based on their role: Touch 1 (Day 90 before contract_end):
      champion. Touch 2 (Day 60): economic buyer. Touch 3 (Day 60, parallel): IT/security if applicable.
      Touch 4 (Day 30): all stakeholders. Add a renewal-meeting-scheduled branch: if CSM/AE schedules
      a renewal meeting at any point, journey pauses (human-led from here). For high-risk accounts (renewal_health
      composite low or any churn signal), additionally create urgent CSM task at Day 90: automation alone
      won't save at-risk renewals. Use the result of "Find renewals inside 90 days", "Read the renewal
      health", "Write one email per role".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: Forecast the renewal book
    summary: >-
      Renewals and ARR by quarter, the health split, what falls due when, how many renewals involved a
      human conversation, how many grew rather than held flat or shrank, and the renewal rate over time.
    builds: dashboard
    description: >-
      Compose a B2B renewal pipeline dashboard: renewal forecast by quarter (account count + ARR at risk),
      renewal health distribution (green/yellow/red), days-to-renewal pipeline (which renewals are coming
      up when), CSM/AE engagement rate (% of renewals where a human conversation happened: target: 100%
      for accounts >$50K ARR), expansion-during-renewal rate (renewals that grow vs. flat vs. shrink),
      and renewal-rate trend over time. The strategic view that gives leadership confidence in NRR. Use
      the result of "Find renewals inside 90 days", "Read the renewal health", "Write one email per role",
      "Reach each stakeholder in turn".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: attribute
    producedByStep: s2
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: asset
    producedByStep: s3
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# B2B contract renewal

For B2B accounts approaching contract end, run a renewal journey at 90, 60, and 30 days to the enrolled profile.

## Steps

1. **Find renewals inside 90 days** (builds segment)

   Active enterprise and mid market accounts whose contract ends between 30 and 90 days from now. Each one has several contacts, and the journey reaches them by role.

2. **Read the renewal health** (builds attribute)

   Taken when the account enters the renewal window: whether usage grew, flattened or fell over 12 months, what outcomes and ROI you can show, whether the champion is still in role and the budget holder is reachable, the tone of six months of support tickets, and any competitor mentions in meeting notes.

3. **Write one email per role** (builds email_html)

   The champion gets a value recap of the year and a request to help line up the renewal conversation. The budget holder gets business value, ROI and terms. Security or IT gets documentation and certification updates. At 30 days everyone gets a consolidated reminder with the proposed terms attached. Business formal, not marketing chat.

4. **Reach each stakeholder in turn** (builds journey)

   Champion at 90 days, budget holder at 60, security at 60 in parallel, and all of them at 30. The moment a CSM or AE books a renewal meeting the journey pauses and the human takes over. Accounts with weak health or any churn signal also get an urgent CSM task at day 90.

5. **Forecast the renewal book** (builds dashboard)

   Renewals and ARR by quarter, the health split, what falls due when, how many renewals involved a human conversation, how many grew rather than held flat or shrank, and the renewal rate over time.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new segment, from step 1 "Find renewals inside 90 days"
- A new attribute, from step 2 "Read the renewal health"
- A new designed email, from step 3 "Write one email per role"
- A new journey, from step 4 "Reach each stakeholder in turn"
- A new dashboard, from step 5 "Forecast the renewal book"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
