---
frontmatter_id: pql-signal-to-sdr-task
slash_command: /pql-signal-to-sdr-task
description: When a free user's behaviour says they are ready for a conversation, it creates an SDR task carrying everything needed for the first touch.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Flags free users whose product behaviour signals readiness for sales, then creates a high-priority SDR task with
    usage context, routing poor-fit accounts to self-serve nurture instead.
  parameters:
  - name: pqlThreshold
    type: number
    label: PQL score threshold (0-100)
    default: 70
    required: false
  - name: scoreLookbackWindow
    type: duration
    label: Window for crossing the threshold
    default: 7 d
    required: false
  - name: outreachCooldown
    type: duration
    label: Window with no recent outreach
    default: 30 d
    required: false
  - name: sessionWindow
    type: duration
    label: Usage depth session window
    default: 14 d
    required: false
  - name: firstTouchSla
    type: duration
    label: First touch SLA
    default: 24 h
    required: false
  - name: untouchedAlertWindow
    type: duration
    label: Untouched lead alert window
    default: 48 h
    required: false
  - name: untouchedAlertShare
    type: number
    label: Share of PQLs untouched that triggers a flag (%)
    default: 20
    required: false
  requirements:
  - slot: free_user_activity
    kind: event
    meaning: A user used a product feature
    properties:
    - name: feature_name
      type: text
      meaning: Name of the feature used
      optional: false
    - name: plan_tier
      type: string
      meaning: Account plan tier of the user
      optional: true
  - slot: user_profile
    kind: attribute
    meaning: Attributes of a user such as plan tier, email domain and opt-out status
  - slot: pql_score
    kind: attribute
    meaning: A numeric product-qualified-lead score for a user
    optional: true
  - slot: active_sdr_task
    kind: event
    meaning: An SDR task is open for a user
  - slot: outreach_event
    kind: event
    meaning: A sales or marketing outreach was sent to a user
  - slot: opt_out_list
    kind: segment
    meaning: Users who opted out of sales outreach
  - slot: paid_users
    kind: segment
    meaning: Users on a paid plan
  - slot: account_enrichment
    kind: integration
    meaning: A firmographic enrichment source for company size, industry and ICP fit
    channel: email
  - slot: sdr_territory_rules
    kind: knowledge
    meaning: Territory rules mapping geography, industry and account size to SDRs
  - slot: sdr_task_queue
    kind: destination
    meaning: Queue where SDR tasks are created and assigned
    channel: hubspot
  - slot: sdr_slack
    kind: integration
    meaning: Slack workspace used to notify SDRs by direct message
    channel: slack
  - slot: pql_dashboard_home
    kind: knowledge
    meaning: Shared reporting space where the PQL conversion dashboard is kept
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - free_user_activity
    - user_profile
    - pqlThreshold
    - sessionWindow
    instruction: 'Create an AI-derived attribute named pql_score on the user object, scored 0 to 100. Composite signal: (a)
      high-value feature usage from {free_user_activity.feature_name}, key activation events weighted highest; (b) usage depth:
      sessions in the last {sessionWindow}, features touched, and time in product; (c) account-level density: other users
      from the same email domain active. A score at or above {pqlThreshold} counts as a PQL. Refresh daily and on every feature
      usage event.'
  - id: s2
    builds: segment
    uses:
    - s1
    - pql_score
    - active_sdr_task
    - outreach_event
    - paid_users
    - opt_out_list
    - pqlThreshold
    - scoreLookbackWindow
    - outreachCooldown
    instruction: 'Build a segment named ''PQL: free users score >= {pqlThreshold}'' containing free-tier users whose pql_score
      crossed {pqlThreshold} within the last {scoreLookbackWindow}, who have no open {active_sdr_task}, and who have had no
      {outreach_event} in the last {outreachCooldown}. Exclude paid users in {paid_users} and anyone in {opt_out_list}.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - account_enrichment
    - free_user_activity
    - sdr_territory_rules
    - sdr_task_queue
    - sdr_slack
    - pqlThreshold
    instruction: 'Create a workflow that fires when a user''s pql_score crosses {pqlThreshold}. Step 1: if the account is
      not yet enriched, enrich it with firmographics and ICP fit from {account_enrichment}. Step 2: compute outreach context:
      top features used from {free_user_activity.feature_name}, usage frequency, account size, and ICP fit tier. Step 3: if
      the account is at or above the ICP threshold, create a high-priority SDR task in {sdr_task_queue} with the outreach
      context attached, assigned by {sdr_territory_rules} (geography, industry, account size). Step 4: post a brief Slack
      direct message to the assigned SDR through {sdr_slack} with a link to the task. If the account is below the ICP threshold,
      enrol the user in self serve nurture instead of creating an SDR task.'
  - id: s4
    builds: dashboard
    uses:
    - s2
    - s3
    - pqlThreshold
    - firstTouchSla
    - untouchedAlertWindow
    - untouchedAlertShare
    - pql_dashboard_home
    instruction: 'Build a PQL conversion dashboard showing: weekly PQL volume (count of free users crossing {pqlThreshold})
      with trend; median time from threshold cross to first SDR touch, with a target under {firstTouchSla}; PQL-to-meeting
      conversion rate; PQL-to-deal conversion rate by ICP tier; and an SDR leaderboard ranking reps by PQL conversion rate.
      Flag any week where more than {untouchedAlertShare}% of PQLs are still untouched after {untouchedAlertWindow}. Source
      data comes from the segment in "Find free users crossing 70" and the workflow in "Give the SDR the context".'
---

# Product qualified lead to SDR task

Slash command: /pql-signal-to-sdr-task

## Step 1: Score free users on behaviour

Create an AI-derived attribute 'pql_score' on the User object. Composite signal: (a) high-value feature usage (key activation events) weighted highest; (b) usage depth (sessions in last 14 days, features touched, time-in-product); (c) account-level density (other users from same domain active). Output: numeric score 0-100. Score >= 70 = PQL. Refreshed daily and on feature_used events.

## Step 2: Find free users crossing 70

Build a segment 'PQL: free users score >= 70' capturing free-tier users where pql_score crossed 70 in the last 7 days AND no active SDR task exists for this user AND no recent (last 30 days) outreach has occurred. Excludes paid users (different workflow) and users in opt-out list. Use the result of "Score free users on behaviour".

## Step 3: Give the SDR the context

Create a workflow firing when pql_score crosses 70. Step sequence: (1) enrich the user's account if not already enriched (firmographics, ICP fit); (2) compute outreach context: top features used, usage frequency, account size, ICP fit tier; (3) create a high-priority SDR task with the outreach context attached, assigned via territory rules (geo / industry / account size); (4) post a brief Slack notification to the assigned SDR's DM with the task link. If account is below ICP threshold, route to self-serve nurture journey instead of SDR queue. Use the result of "Score free users on behaviour", "Find free users crossing 70".

## Step 4: Hold the 24 hour first touch

Compose a PQL conversion dashboard: PQL volume (count of free users crossing threshold per week, trend), median time from threshold-cross to first SDR touch (SLA target: <24hr), PQL-to-meeting conversion rate, PQL-to-deal conversion rate by ICP tier, and rep leaderboard (SDRs converting PQLs at the highest rates). Flag any week where >20% of PQLs are untouched after 48 hours. Use the result of "Score free users on behaviour", "Find free users crossing 70", "Give the SDR the context".
