---
frontmatter_id: contract-renewal-b2b
slash_command: /contract-renewal-b2b
description: For B2B accounts approaching contract end, run a renewal journey at 90, 60, and 30 days to the enrolled profile.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Runs a renewal journey for B2B accounts nearing contract end, sending role-tailored emails at 90, 60 and 30 days,
    pausing for human-led follow-up, and reporting renewal pipeline health.
  parameters:
  - name: renewal_window_start
    type: duration
    label: Renewal window start (days before contract end)
    default: 30 d
    required: false
  - name: renewal_window_end
    type: duration
    label: Renewal window end (days before contract end)
    default: 90 d
    required: false
  - name: champion_touch_day
    type: number
    label: Champion touch (days before contract end)
    default: 90
    required: false
  - name: economic_buyer_touch_day
    type: number
    label: Economic buyer touch (days before contract end)
    default: 60
    required: false
  - name: final_reminder_day
    type: number
    label: Final reminder (days before contract end)
    default: 30
    required: false
  - name: tone
    type: enum
    label: Email tone
    default: business_formal
    required: false
    options:
    - business_formal
    - warm
    - neutral
  - name: high_value_arr_threshold
    type: number
    label: ARR threshold for 100% human engagement target (USD)
    default: 50000
    required: false
  requirements:
  - slot: b2b_account
    kind: attribute
    meaning: A B2B account with a contract end date, account tier, and subscription status
    properties:
    - name: contract_end_date
      type: date
      meaning: Date the account's contract ends
      optional: false
    - name: account_tier
      type: enum
      meaning: Account tier such as enterprise or mid-market
      optional: false
    - name: subscription_status
      type: enum
      meaning: Whether the subscription is active
      optional: false
  - slot: renewal_window_segment
    kind: segment
    meaning: Accounts whose contract ends within the renewal window and that are enterprise or mid-market and active
    creatable: true
    definition: accounts where contract_end_date is between {renewal_window_start} and {renewal_window_end} from now AND account_tier
      is enterprise or mid-market AND subscription_status is active
  - slot: renewal_contact
    kind: segment
    meaning: Contacts at a B2B account who hold a champion, economic buyer, IT/security, or other stakeholder role
    properties:
    - name: contact_role
      type: enum
      meaning: Stakeholder role of the contact (champion, economic_buyer, it_security, other)
      optional: true
  - slot: renewal_health_score
    kind: attribute
    meaning: Composite renewal health score for an account, including usage, value, stakeholder, support sentiment and competitor
      signals
  - slot: churn_signal
    kind: attribute
    meaning: Flag indicating an account shows a churn risk signal
    optional: true
  - slot: csm_task_owner
    kind: integration
    meaning: CRM where CSM and AE tasks and meetings are recorded for human follow-up
    channel: hubspot
  - slot: renewal_email_sender
    kind: integration
    meaning: Email sending integration used to deliver renewal emails
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - b2b_account
    - renewal_window_start
    - renewal_window_end
    instruction: Build the segment 'Upcoming B2B contract renewals - next 90 days' of {b2b_account} where contract_end_date
      is between {renewal_window_start} and {renewal_window_end} from now, account_tier is enterprise or mid-market, and subscription_status
      is active. Each account in the segment has multiple touched users; the journey reaches different contacts at the account
      with role-appropriate messaging.
  - id: s2
    builds: attribute
    uses:
    - s1
    - renewal_health_score
    instruction: 'Create an AI-derived attribute ''renewal_health_snapshot'' on the {b2b_account} object, computed at renewal-window
      entry for accounts in ''Upcoming B2B contract renewals - next 90 days''. Aggregate: (a) usage trajectory over the past
      12 months (growing, flat, or declining); (b) value delivered (key outcomes, milestones reached, ROI metric if tracked);
      (c) stakeholder health (is the champion still in role and engaged, is the economic buyer reachable, are new stakeholders
      identified); (d) support ticket sentiment over the past 6 months; (e) competitor mentions in any meeting summaries.
      Output a composite health score and structured content for the renewal emails.'
  - id: s3
    builds: email
    uses:
    - s1
    - s2
    - champion_touch_day
    - economic_buyer_touch_day
    - final_reminder_day
    - tone
    instruction: 'Build a designed HTML email set using the accounts in ''Upcoming B2B contract renewals - next 90 days''
      and the content from ''Read the renewal health snapshot''. Tone: {tone}, value-substantive, not marketing-chatty. Email
      (a), user-champion, sent at {champion_touch_day} days before contract end: subject ''Quick value-recap of the past year
      (what is working and what is next)''; focus on product wins and usage statistics; ask for help coordinating the upcoming
      renewal conversation. Email (b), economic buyer, sent at {economic_buyer_touch_day} days before contract end: subject
      ''Your team''s renewal is up in 60 days (let''s connect on terms)''; focus on business value, ROI, growth opportunity
      and available terms. Email (c), IT/security stakeholder if known, sent at {economic_buyer_touch_day} days before contract
      end: subject ''Security/compliance update for your upcoming renewal''; proactive on documentation, certifications and
      any changes. Email (d), late reminder sent at {final_reminder_day} days before contract end: consolidated reminder to
      all stakeholders with proposed contract terms attached.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - renewal_contact
    - renewal_email_sender
    - csm_task_owner
    - champion_touch_day
    - economic_buyer_touch_day
    - final_reminder_day
    - renewal_window_end
    instruction: 'Build a multi-touch, multi-stakeholder journey triggered when an account enters ''Upcoming B2B contract
      renewals - next 90 days''. Each touch goes to a different {renewal_contact} based on role. Touch 1 at {champion_touch_day}
      days before contract end: champion, send ''Email (a)'' from ''Write one email per role''. Touch 2 at {economic_buyer_touch_day}
      days before contract end: economic buyer, send ''Email (b)''. Touch 3 at {economic_buyer_touch_day} days before contract
      end, in parallel: IT/security contact if one is identified, send ''Email (c)''. Touch 4 at {final_reminder_day} days
      before contract end: all stakeholders, send ''Email (d)''. Branch: if a CSM or AE schedules a renewal meeting in {csm_task_owner}
      at any point, pause the journey so the renewal is human-led from that point. For high-risk accounts (low {renewal_health_score}
      composite or any {churn_signal}), also create an urgent CSM task in {csm_task_owner} at {champion_touch_day} days before
      contract end, since automation alone will not save at-risk renewals.'
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - high_value_arr_threshold
    - renewal_health_score
    instruction: 'Compose a B2B renewal pipeline dashboard for accounts in ''Upcoming B2B contract renewals - next 90 days''.
      Show: renewal forecast by quarter (account count and ARR at risk); renewal health distribution (green, yellow, red)
      from {renewal_health_score}; days-to-renewal pipeline showing which renewals fall due when; CSM and AE engagement rate
      (percent of renewals with a human conversation, target 100% for accounts above {high_value_arr_threshold} ARR); expansion-during-renewal
      rate (renewals that grow, stay flat, or shrink); and renewal-rate trend over time.'
---

# B2B contract renewal

Slash command: /contract-renewal-b2b

## Step 1: Find renewals inside 90 days

Build a segment 'Upcoming B2B contract renewals - next 90 days' capturing accounts where contract_end_date is between 30 and 90 days from now AND account_tier is enterprise or mid-market AND subscription_status is active. Each account in the segment has multiple touched users, the journey reaches different contacts at the account with role-appropriate messaging.

## Step 2: Read the renewal health

Create an AI-derived attribute 'renewal_health_snapshot' on the Account object, computed at renewal-window entry. Aggregates: (a) usage trajectory over past 12 months (growing / flat / declining); (b) value delivered (key outcomes, milestones reached, ROI metric if tracked); (c) stakeholder health: champion still in role and engaged? economic buyer reachable? new stakeholders identified?; (d) support ticket sentiment over past 6 months; (e) competitor mentions in any meeting summaries. Output: composite health score + structured content for the renewal emails. Use the result of "Find renewals inside 90 days".

## Step 3: Write one email per role

This step builds a designed marketing email (HTML).
Generate role-tailored renewal content. (a) User-champion (Day 90): 'Quick value-recap of the past year (what's working and what's next') focuses on product wins, usage stats, asks for help to coordinate the upcoming renewal conversation. (b) Economic buyer (Day 60): 'Your team's renewal is up in 60 days (let's connect on terms') focuses on business value, ROI, growth opportunity, available terms. (c) IT/security stakeholder if known (Day 60): 'Security/compliance update for your upcoming renewal': proactive on documentation, certifications, any changes. (d) Late reminder (Day 30): consolidated reminder to all stakeholders with proposed contract terms attached. Tone: business-formal, value-substantive, not marketing-chatty. Use the result of "Find renewals inside 90 days", "Read the renewal health".

## Step 4: Reach each stakeholder in turn

Build a multi-touch multi-stakeholder journey triggered at renewal-window entry. Each touch goes to a DIFFERENT contact at the account based on their role: Touch 1 (Day 90 before contract_end): champion. Touch 2 (Day 60): economic buyer. Touch 3 (Day 60, parallel): IT/security if applicable. Touch 4 (Day 30): all stakeholders. Add a renewal-meeting-scheduled branch: if CSM/AE schedules a renewal meeting at any point, journey pauses (human-led from here). For high-risk accounts (renewal_health composite low or any churn signal), additionally create urgent CSM task at Day 90: automation alone won't save at-risk renewals. Use the result of "Find renewals inside 90 days", "Read the renewal health", "Write one email per role".

## Step 5: Forecast the renewal book

Compose a B2B renewal pipeline dashboard: renewal forecast by quarter (account count + ARR at risk), renewal health distribution (green/yellow/red), days-to-renewal pipeline (which renewals are coming up when), CSM/AE engagement rate (% of renewals where a human conversation happened: target: 100% for accounts >$50K ARR), expansion-during-renewal rate (renewals that grow vs. flat vs. shrink), and renewal-rate trend over time. The strategic view that gives leadership confidence in NRR. Use the result of "Find renewals inside 90 days", "Read the renewal health", "Write one email per role", "Reach each stakeholder in turn".
