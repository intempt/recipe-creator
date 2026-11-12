---
frontmatter_id: single-threaded-deal-alert
slash_command: /single-threaded-deal-alert
description: Finds late stage deals where only one person on the buyer's side is engaged and gives the rep three other names to bring in.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Flags late-stage open deals where only one buyer-side contact is engaged, then gives the rep three suggested contacts
    to bring in and a dashboard tracking multi-threading.
  parameters:
  - name: lateStageNames
    type: text
    label: Late-stage deal stages
    default: Demo, Proposal, Closing
    required: false
  - name: minDealAgeDays
    type: number
    label: Minimum deal age before flagging (days)
    default: 14
    required: false
  - name: agedRiskDays
    type: number
    label: Days single-threaded before a deal counts as high-loss-risk
    default: 30
    required: false
  - name: multiThreadTarget
    type: number
    label: Target share of mid/late-stage deals multi-threaded (%)
    default: 70
    required: false
  - name: coachingGapThreshold
    type: number
    label: Coaching gap threshold for multi-threaded share (%)
    default: 50
    required: false
  - name: suggestedContactCount
    type: number
    label: Number of suggested contacts to add
    default: 3
    required: false
  requirements:
  - slot: deal_engagement_event
    kind: event
    meaning: A buyer-side contact attended a meeting on a deal or replied to an email on a deal
    properties:
    - name: contact
      type: text
      meaning: Buyer-side contact who attended or replied
      optional: false
    - name: deal
      type: text
      meaning: Deal the engagement belongs to
      optional: false
    - name: activity_type
      type: text
      meaning: Whether the activity was a meeting attendance or an email reply
      optional: false
  - slot: deal_contact_association
    kind: attribute
    meaning: A buyer-side contact was explicitly added as a contact on a deal
  - slot: deal
    kind: attribute
    meaning: Open sales deal with a stage, creation date, and an exec-buyer flag
  - slot: deal_stage
    kind: attribute
    meaning: Current pipeline stage of a deal (Demo, Proposal, Closing, etc.)
  - slot: exec_buyer_flag
    kind: attribute
    meaning: Deal is flagged as having a single executive decision-maker buyer
  - slot: account_enrichment
    kind: integration
    meaning: Account enrichment source that suggests additional contacts by role, management line and team
    channel: hubspot
  - slot: rep_slack
    kind: integration
    meaning: Slack workspace for direct messages to deal owners
    channel: slack
  - slot: rep_task
    kind: destination
    meaning: Task queue where reps receive follow-up tasks on deals
    channel: hubspot
  steps:
  - id: s1
    builds: attribute
    uses:
    - deal
    - deal_engagement_event
    - deal_contact_association
    - deal_stage
    - lateStageNames
    instruction: Create an AI-derived attribute 'threading_depth' on {deal}. Count distinct buyer-side contacts who have (a)
      attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been explicitly added as a deal contact,
      using {deal_engagement_event.contact} and {deal_contact_association}. Output an integer count. Flag the deal as 'single-threaded'
      when the count equals 1 and {deal_stage} is one of {lateStageNames}. Early-stage single-threading is normal; late-stage
      is a red flag.
  - id: s2
    builds: segment
    uses:
    - deal
    - deal_stage
    - exec_buyer_flag
    - lateStageNames
    - minDealAgeDays
    - s1
    instruction: Build a segment 'Single-threaded deals - mid+ stage' of open {deal} records where "Count who is actually
      engaged" equals 1 and {deal_stage} is one of {lateStageNames}. Exclude deals created fewer than {minDealAgeDays} days
      ago and deals where {exec_buyer_flag} is true, since a single decision-maker is genuine in some buyer profiles.
  - id: s3
    builds: automation
    uses:
    - deal
    - account_enrichment
    - rep_task
    - rep_slack
    - suggestedContactCount
    - s1
    - s2
    instruction: 'Create a workflow that runs daily for {deal} records newly added to "Find the risky ones". Steps in order:
      (1) recompute threading_depth on each deal; (2) for deals that remain genuine single-threaded mid-stage deals, fetch
      the top {suggestedContactCount} suggested additional contacts from {account_enrichment} (peer roles, manager up, related
      team members), ranked by likely buying influence; (3) create a task on the deal owner''s record labeled ''Multi-thread
      this deal: {suggestedContactCount} suggested contacts'' with the contact list attached, using {rep_task}; (4) send a
      Slack direct message to the deal owner with the deal context through {rep_slack}. Suppress the workflow when the lone
      contact is the decision-maker (for example a CEO of a small company), because that is not a single-threading risk.'
  - id: s4
    builds: dashboard
    uses:
    - deal_stage
    - multiThreadTarget
    - coachingGapThreshold
    - agedRiskDays
    - s1
    - s2
    - s3
    instruction: 'Compose a threading health dashboard with these panels: (a) percent of mid/late-stage deals that are multi-threaded,
      with a target of {multiThreadTarget}% and a coaching-gap flag below {coachingGapThreshold}%; (b) distribution of threading
      depth by {deal_stage}; (c) win rate of single-threaded deals versus multi-threaded deals; (d) rep leaderboard ranked
      by threading depth; (e) aged single-threaded deals open longer than {agedRiskDays} days, shown as the high-loss-risk
      list. Use the results of "Count who is actually engaged", "Find the risky ones" and "Give the rep three names".'
---

# Single threaded deal alert

Slash command: /single-threaded-deal-alert

## Step 1: Count who is actually engaged

Create an AI-derived attribute 'threading_depth' on the Deal object. Count distinct buyer-side contacts who have (a) attended a meeting on this deal, OR (b) replied to an email on this deal, OR (c) been explicitly added as a deal contact. Output: integer count. Flag as 'single-threaded' if count = 1 and deal is in Demo / Proposal / Closing stage (early-stage single-threading is normal; late-stage is a red flag).

## Step 2: Find the risky ones

Build a segment 'Single-threaded deals - mid+ stage' capturing open deals where threading_depth = 1 AND stage is Demo, Proposal, or Closing. Excludes deals < 14 days old (haven't had time for multi-threading naturally) and deals flagged as exec-buyer (1-person decision is genuine in some buyer profiles, e.g. founder-led SMB). Use the result of "Count who is actually engaged".

## Step 3: Give the rep three names

Create a workflow firing daily for deals newly-flagged as single-threaded. Step sequence: (1) recompute threading_depth (fresh); (2) for genuine single-threaded mid-stage deals, fetch suggested additional contacts from account enrichment (peer roles, manager up, related team members), prioritized by likely-buying-influence; (3) create a task for the rep labeled 'Multi-thread this deal: 3 suggested contacts' with the contact list pre-attached; (4) Slack DM to the rep with deal context. If lone champion is the decision-maker (CEO of a small co, etc.), suppress: that's not single-threading risk. Use the result of "Count who is actually engaged", "Find the risky ones".

## Step 4: See what threading is worth

Compose a threading health dashboard: % of mid+stage deals that are multi-threaded (target: 70%+; below 50% is a coaching gap), distribution of threading depth by stage, single-threaded-deal win rate vs. multi-threaded win rate (the proof-of-value chart), rep leaderboard on threading depth, and aged single-threaded deals (>30 days single-threaded = high-loss-risk pile). Use the result of "Count who is actually engaged", "Find the risky ones", "Give the rep three names".
