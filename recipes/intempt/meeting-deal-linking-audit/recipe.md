---
frontmatter_id: meeting-deal-linking-audit
slash_command: /meeting-deal-linking-audit
description: Displays meetings in widgets so teams can review meeting activity in one place.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Automatically links revenue-impacting meetings to the right deal, routes uncertain matches to hosts for confirmation,
    and tracks linking coverage on a hygiene dashboard.
  parameters:
  - name: lookback_window
    type: duration
    label: Audit lookback window
    default: 60 d
    required: false
  - name: revenue_meeting_types
    type: enum
    label: Revenue-impacting meeting types
    default: discovery_demo_proposal_close_renewal
    required: false
    options:
    - discovery_demo_proposal_close_renewal
  - name: high_target_linking_rate
    type: number
    label: Target linking rate (%)
    default: 95
    required: false
  - name: warning_linking_rate
    type: number
    label: Warning linking rate threshold (%)
    default: 85
    required: false
  requirements:
  - slot: meeting_logged
    kind: event
    meaning: A customer meeting was logged or synced to the CRM
    properties:
    - name: meeting_date
      type: date
      meaning: Date the meeting took place
      optional: false
    - name: meeting_type
      type: string
      meaning: Type of meeting (Discovery, Demo, Proposal, Close, Renewal, internal sync, 1:1, interview)
      optional: false
    - name: host
      type: string
      meaning: Person who hosted the meeting
      optional: false
    - name: attendees
      type: text
      meaning: Attendees with their company
      optional: false
    - name: linked_deal
      type: string
      meaning: Deal the meeting is linked to, empty if none
      optional: true
  - slot: open_deal
    kind: attribute
    meaning: An open deal on a customer account, with its stage and contacts
  - slot: account_contacts
    kind: attribute
    meaning: Contacts associated with a deal or account
  - slot: unlinked_revenue_meetings
    kind: segment
    meaning: Revenue-impacting meetings with no linked deal
  - slot: link_meeting_to_deal
    kind: integration
    meaning: Ability to link a meeting record to a deal record in the CRM
    channel: hubspot
  - slot: host_task_queue
    kind: destination
    meaning: Task system where meeting hosts receive tasks
    channel: hubspot
  - slot: linking_dashboard
    kind: destination
    meaning: Dashboard for meeting-deal linking hygiene
    channel: email
  steps:
  - id: s1
    builds: report
    uses:
    - meeting_logged
    - open_deal
    - account_contacts
    - unlinked_revenue_meetings
    - lookback_window
    - revenue_meeting_types
    instruction: 'List all meetings from the last {lookback_window} that have no linked deal. Filter to meetings where the
      meeting type is revenue-impacting ({revenue_meeting_types}: Discovery, Demo, Proposal, Close, Renewal; exclude internal
      sync, 1:1, interview). For each unlinked meeting, surface: meeting date ({meeting_logged.meeting_date}), host ({meeting_logged.host}),
      attendees with company ({meeting_logged.attendees}), and any open deals on attendees'' accounts ({open_deal}). The output
      is the working set for the linking action.'
  - id: s2
    builds: automation
    uses:
    - meeting_logged
    - open_deal
    - account_contacts
    - link_meeting_to_deal
    - host_task_queue
    - linking_dashboard
    - s1
    instruction: 'Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from the
      audit in "Find meetings with no deal"). For each: (1) compute the most-likely deal match: same account, open stage,
      and attendees overlapping deal contacts ({account_contacts}); (2) if confidence is high (single clear match), auto-link
      via {link_meeting_to_deal}; (3) if confidence is medium (multiple plausible matches or attendees do not overlap deal
      contacts), create a task for the meeting host ({meeting_logged.host}) in {host_task_queue} asking them to confirm the
      right deal; (4) if no plausible match exists (account has no open deals), log to {linking_dashboard} for review as a
      likely new opportunity needing a deal record.'
  - id: s3
    builds: dashboard
    uses:
    - meeting_logged
    - linking_dashboard
    - high_target_linking_rate
    - warning_linking_rate
    - s1
    - s2
    instruction: 'Compose a meeting-deal-linking hygiene dashboard showing: percent of revenue-impacting meetings linked to
      deals (target {high_target_linking_rate}%+; below {warning_linking_rate}% means the linking workflow is failing or reps
      are not acting on confirmation tasks); count of meetings auto-linked vs. manually linked vs. unlinked and needing review;
      top 5 hosts ({meeting_logged.host}) with the most unlinked meetings as a coaching signal; and recent meetings where
      no plausible deal match was flagged in "Keep new meetings linked" as likely missing opportunities. Include a trend of
      the linking rate over time, since a falling rate is a leading indicator of pipeline visibility decay. Use the results
      of "Find meetings with no deal" and "Keep new meetings linked".'
---

# Link meetings to the right deal

Slash command: /meeting-deal-linking-audit

## Step 1: Find meetings with no deal

List all meetings from the last 60 days that have no linked deal. Filter to meetings where the meeting type is revenue-impacting (Discovery, Demo, Proposal, Close, Renewal: exclude internal sync, 1:1, interview). For each unlinked meeting, surface: meeting date, host, attendees (with company), and any open deals on attendees' accounts. The output is the working set for the linking action.

## Step 2: Keep new meetings linked

Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from the audit). For each: (1) compute the most-likely deal match: same account + open stage + attendees overlap with deal contacts; (2) if confidence is high (single clear match), auto-link via link_meeting_to_deal; (3) if confidence is medium (multiple plausible matches or attendees-don't-overlap-deal-contacts), create a task for the meeting host asking them to confirm the right deal; (4) if no plausible match exists (account has no open deals), log to the dashboard for review (likely a new opp that needs a deal record). Use the result of "Find meetings with no deal".

## Step 3: Track linking coverage

Compose a meeting-deal-linking hygiene dashboard: % of revenue-impacting meetings linked to deals (target: 95%+; below 85% means the linking workflow is failing or reps aren't acting on confirmation tasks); count of meetings auto-linked vs. manually-linked vs. unlinked-needing-review; top 5 hosts with most unlinked meetings (coaching signal); recent meetings where 'no plausible deal match' was flagged (likely missing opportunities). Trend over time: falling linking-rate is a leading indicator of pipeline visibility decay. Use the result of "Find meetings with no deal", "Keep new meetings linked".
