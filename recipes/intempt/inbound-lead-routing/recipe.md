---
frontmatter_id: inbound-lead-routing
slash_command: /inbound-lead-routing
description: Scores every inbound lead out of 100, picks the rep by named account owner, territory or round robin, and emails
  the team the routed lead, plus a weekly digest of balance and first-touch time.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Scores each inbound lead, emails an alert naming the rep it routes to by account owner, territory or round robin,
    and emails a weekly routing digest.
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
    label: First-touch target for hot leads
    default: 2 h
    required: false
  - name: warm_first_touch_sla
    type: duration
    label: First-touch target for warm leads
    default: 24 h
    required: false
  - name: rep_variance_limit
    type: number
    label: Maximum rep-to-rep routing variance (%)
    default: 15
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses that get the routed-lead alerts
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: inbound_form_submitted
    kind: event
    meaning: A prospect submitted a form on the website (a form on the site, never a survey or NPS answer)
    properties:
    - name: form_type
      type: string
      meaning: 'Type of form submitted: demo, content or newsletter'
      optional: false
    - name: source
      type: string
      meaning: Lead source; self-serve-only leads are excluded
      optional: true
  - slot: user_signed_up
    kind: event
    meaning: A new user signed up for the product
    properties:
    - name: source
      type: string
      meaning: Signup source; self-serve-only signups are excluded
      optional: true
  - slot: pricing_page_viewed
    kind: event
    meaning: A user viewed the pricing page
    optional: true
  - slot: job_title
    kind: attribute
    meaning: The lead's job title
  - slot: company_industry
    kind: attribute
    meaning: Industry of the lead's company
  - slot: company_size
    kind: attribute
    meaning: Employee count of the lead's company
  - slot: country
    kind: attribute
    meaning: The lead's country
  - slot: account_owner
    kind: attribute
    meaning: The rep who owns a named target account; empty when the account has no owner
  - slot: rep_territories
    kind: attribute
    meaning: The territory rep pool for the lead's country and industry
  - slot: first_touch
    kind: event
    meaning: A rep made first contact with a lead
    properties:
    - name: assigned_rep
      type: string
      meaning: Rep who made the contact
      optional: false
  - slot: meeting_scheduled
    kind: event
    meaning: A sales meeting was scheduled with a lead
  steps:
  - id: s1
    builds: attribute
    uses:
    - inbound_form_submitted
    - pricing_page_viewed
    - job_title
    - company_industry
    - company_size
    - country
    instruction: 'Build a computed attribute on users named "lead_score", a number from 0 to 100, the sum of: fit, 0-40 points,
      from {company_industry}, {company_size} and {country} matching the ideal customer; intent, 0-30 points, 30 when they
      did {inbound_form_submitted} with {inbound_form_submitted.form_type} equal to demo, 20 for content, 10 for newsletter,
      plus up to 10 for {pricing_page_viewed} in the last 7 days, capped at 30; seniority, 0-20 points, from {job_title};
      engagement, 0-10 points, from other users at the same company who did {inbound_form_submitted} in the last 90 days.'
  - id: s2
    builds: automation
    uses:
    - s1
    - inbound_form_submitted
    - user_signed_up
    - account_owner
    - rep_territories
    - hot_threshold
    - warm_threshold
    - alert_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation triggered when a user does {inbound_form_submitted} or {user_signed_up}, skipping it
      when source is self-serve-only. It reads the score from "Score the lead out of 100" and labels the lead hot at {hot_threshold}
      or more, warm from {warm_threshold}, else cold. It stops for cold leads with no {account_owner}. It picks the rep: {account_owner}
      when set; otherwise the rep in {rep_territories} with the fewest leads routed in the last 7 days. It writes the lead''s
      name, email, company, score, label, the rep and the reason, and emails these lines as an alert to {alert_recipients}.
      It never emails the lead.'
  - id: s3
    builds: automation
    uses:
    - s1
    - inbound_form_submitted
    - first_touch
    - meeting_scheduled
    - hot_threshold
    - warm_threshold
    - hot_first_touch_sla
    - warm_first_touch_sla
    - rep_variance_limit
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {inbound_form_submitted}
      in the last 7 days and writes these figures: lead counts by label from "Score the lead out of 100" (hot at {hot_threshold}
      or more, warm from {warm_threshold}, cold below); {first_touch} counts by {first_touch.assigned_rep}, and whether any
      rep is more than {rep_variance_limit}% above or below the average; median time to {first_touch} for hot leads against
      {hot_first_touch_sla} and for warm leads against {warm_first_touch_sla}; the share of hot and of warm leads that did
      {meeting_scheduled}. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      Nothing else is sent.'
---

# Inbound lead routing

Slash command: /inbound-lead-routing

## Step 1: Score the lead out of 100

Build a computed attribute on users named "lead_score", a number from 0 to 100, the sum of: fit, 0-40 points, from company industry, company size and country matching the ideal customer; intent, 0-30 points, 30 when they did inbound form submitted with form type equal to demo, 20 for content, 10 for newsletter, plus up to 10 for pricing page viewed in the last 7 days, capped at 30; seniority, 0-20 points, from job title; engagement, 0-10 points, from other users at the same company who did inbound form submitted in the last 90 days.

## Step 2: Route it to the right rep

Build an automation triggered when a user does inbound form submitted or user signed up, skipping it when source is self-serve-only. It reads the score from "Score the lead out of 100" and labels the lead hot at 70 or more, warm from 40, else cold. It stops for cold leads with no account owner. It picks the rep: account owner when set; otherwise the rep in rep territories with the fewest leads routed in the last 7 days. It writes the lead's name, email, company, score, label, the rep and the reason, and emails these lines as an alert to the email addresses that get the routed-lead alerts. It never emails the lead.

## Step 3: Email the weekly routing digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did inbound form submitted in the last 7 days and writes these figures: lead counts by label from "Score the lead out of 100" (hot at 70 or more, warm from 40, cold below); first touch counts by assigned rep, and whether any rep is more than 15% above or below the average; median time to first touch for hot leads against 2 h and for warm leads against 24 h; the share of hot and of warm leads that did meeting scheduled. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
