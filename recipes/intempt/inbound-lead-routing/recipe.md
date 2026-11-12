---
frontmatter_id: inbound-lead-routing
slash_command: /inbound-lead-routing
description: Enriches and scores every inbound lead, then assigns it by named account, territory or round robin so nothing rots in an unassigned queue.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores and routes every inbound lead to a rep by named account, territory or round robin, with a task and Slack
    alert, and sends cold leads to nurture.
  parameters:
  - name: hot_threshold
    type: number
    label: Score at or above which a lead is hot
    default: 70
    required: false
  - name: warm_threshold
    type: number
    label: Score at or above which a lead is warm
    default: 40
    required: false
  - name: hot_first_touch_sla
    type: duration
    label: First-touch SLA for hot leads
    default: 2 h
    required: false
  - name: warm_first_touch_sla
    type: duration
    label: First-touch SLA for warm leads
    default: 24 h
    required: false
  - name: rep_variance_limit
    type: number
    label: Maximum rep-to-rep routing variance (%)
    default: 15
    required: false
  requirements:
  - slot: inbound_form_submitted
    kind: event
    meaning: A prospect submitted a form on the website
    properties:
    - name: form_type
      type: text
      meaning: Type of form submitted (demo, content, newsletter)
      optional: false
    - name: source
      type: text
      meaning: Lead source; self-serve-only leads are excluded
      optional: true
  - slot: user_signed_up
    kind: event
    meaning: A new user signed up for the product
    properties:
    - name: source
      type: text
      meaning: Signup source; self-serve-only signups are excluded
      optional: true
  - slot: lead_user
    kind: attribute
    meaning: The lead's user record holding contact, firmographic and geo details
  - slot: target_account_list
    kind: segment
    meaning: Named target accounts with an assigned account owner
  - slot: rep_territories
    kind: attribute
    meaning: Territory definitions mapping geography, industry and segment to a rep pool
  - slot: sales_rep_team
    kind: segment
    meaning: Sales reps eligible to receive routed leads, grouped by territory
  - slot: sales_slack
    kind: integration
    meaning: Slack workspace used to notify reps of newly routed leads
    channel: slack
  - slot: enrichment_provider
    kind: integration
    meaning: Data source that supplies firmographics, technographics and decision-maker contacts for accounts
    channel: email
  - slot: lead_routing_dashboard_source
    kind: event
    meaning: Lead lifecycle events (arrival, first touch, meeting, engagement) used for routing reporting
    properties:
    - name: tier
      type: text
      meaning: Lead tier (hot, warm, cold)
      optional: false
    - name: assigned_rep
      type: text
      meaning: Rep the lead was routed to
      optional: false
  steps:
  - id: s1
    builds: attribute
    uses:
    - lead_user
    - inbound_form_submitted
    - user_signed_up
    - hot_threshold
    - warm_threshold
    instruction: 'Create an AI-derived attribute ''lead score'' on the user record. Score from 0 to 100 by summing: (a) ICP
      fit, 0-40 points, from firmographic match on industry, employee count and geography; (b) intent signal, 0-30 points,
      from form type (demo scores highest, then content, then newsletter), pricing-page views and product activity in the
      last week; (c) buyer signal, 0-20 points, from title seniority and role relevance; (d) brand engagement, 0-10 points,
      from prior touchpoints on the same account. Output the 0-100 score with a tier label: hot at {hot_threshold} or above,
      warm from {warm_threshold} to below {hot_threshold}, cold below {warm_threshold}.'
  - id: s2
    builds: automation
    uses:
    - inbound_form_submitted
    - user_signed_up
    - enrichment_provider
    - target_account_list
    - rep_territories
    - sales_rep_team
    - sales_slack
    - s1
    instruction: 'Create a workflow that fires on {inbound_form_submitted} or {user_signed_up}, excluding records where source
      is self-serve-only. Steps in order: (1) enrich the account with firmographics, technographics and decision-maker contacts
      from {enrichment_provider}; (2) compute the lead score from "Score the lead out of 100"; (3) apply routing rules in
      priority order: (i) named-account override: if the account is on {target_account_list}, route to its assigned account
      owner; (ii) territory match on geography, industry and segment using {rep_territories}; (iii) round-robin within the
      matched territory pool from {sales_rep_team}, to keep rep load balanced; (4) create a task for the determined rep containing
      the lead context, the score and the routing reason; (5) post a Slack notification to that rep in {sales_slack}; (6)
      if the score is cold and no named-account match exists, enroll the lead in self serve nurture journey instead of the
      human queue.'
  - id: s3
    builds: dashboard
    uses:
    - lead_routing_dashboard_source
    - s1
    - s2
    - rep_variance_limit
    - hot_first_touch_sla
    - warm_first_touch_sla
    instruction: 'Build a lead routing performance dashboard showing: lead volume by tier (hot, warm, cold) from "Score the
      lead out of 100"; routing distribution by rep as a round-robin balance check, where rep-to-rep variance should stay
      under {rep_variance_limit}%; median time from lead arrival to first touch against SLAs of {hot_first_touch_sla} for
      hot leads and {warm_first_touch_sla} for warm leads; tier conversion rates of hot-to-meeting, warm-to-meeting and cold-to-engaged.
      Flag any rep whose first-touch SLA is significantly worse than peers.'
---

# Inbound lead routing

Slash command: /inbound-lead-routing

## Step 1: Score the lead out of 100

Create an AI-derived attribute 'lead_score' on the User object. Composite: (a) ICP fit (firmographics match (industry, employee count, geo), 0-40 points; (b) intent signal) form type (demo > content > newsletter), pricing-page views, last-week product activity, 0-30 points; (c) buyer signal (title seniority + role relevance, 0-20 points; (d) brand engagement) prior touchpoints on this account, 0-10 points. Output: 0-100 score with tier label (hot 70+, warm 40-69, cold <40).

## Step 2: Assign it to the right rep

Create a workflow firing on Form submitted OR user_signed_up (where source != self-serve-only). Step sequence: (1) enrich the account (firmographics, technographics, decision-maker contacts); (2) compute lead_score; (3) apply routing rules in priority order: (i) named-account override (if account is on target-account list, route to assigned account owner); (ii) territory match (geography, industry, segment); (iii) round-robin within territory pool (preserves balanced rep load); (4) create task assigned to the determined rep with lead context, score, and routing reason explained; (5) post Slack notification to rep; (6) IF score = cold AND no named-account match, route to self-serve nurture journey instead of human queue. Use the result of "Score the lead out of 100".

## Step 3: Check the balance and the SLA

Compose a lead routing performance dashboard: lead volume by tier (hot/warm/cold), routing distribution by rep (round-robin balance check: variance should be <15% rep-to-rep), median time from lead-arrival to first-touch (SLA: <2hr hot, <24hr warm), tier-conversion: hot-to-meeting / warm-to-meeting / cold-to-engaged rates. Flag any rep with significantly worse first-touch SLA than peers. Use the result of "Score the lead out of 100", "Assign it to the right rep".
