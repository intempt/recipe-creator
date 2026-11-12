---
frontmatter_id: multi-threading-coverage-by-deal
slash_command: /multi-threading-coverage-by-deal
description: Shows distinct stakeholders engaged per open deal from deal and contact data.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Shows how many distinct stakeholders are engaged on each open deal, buckets deals by threading level, and quantifies
    pipeline dollars at risk from single-threaded deals.
  parameters:
  - name: window_closed
    type: duration
    label: Lookback for closed deals in stage view
    default: 90 d
    required: false
  - name: win_rate_window
    type: duration
    label: Lookback for win-rate by threading level
    default: 12 mo
    required: false
  - name: threaded_benchmark_multiplier
    type: number
    label: Win-rate multiplier benchmark for 5+ stakeholder deals
    default: 1.8
    required: false
  - name: benchmark_min_stakeholders
    type: number
    label: Minimum engaged stakeholders for benchmark
    default: 5
    required: false
  - name: single_threaded_max
    type: number
    label: Max contacts counted as single-threaded
    default: 1
    required: false
  - name: lightly_threaded_max
    type: number
    label: Max contacts counted as lightly threaded
    default: 3
    required: false
  - name: multi_threaded_max
    type: number
    label: Max contacts counted as multi-threaded
    default: 6
    required: false
  requirements:
  - slot: deal_stage_event
    kind: event
    meaning: A deal's stage was changed
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
    - name: new_stage
      type: string
      meaning: Stage the deal moved to
      optional: false
    - name: user_ids
      type: text
      meaning: Users associated with the deal at the stage change
      optional: false
    - name: amount
      type: number
      meaning: Deal amount
      optional: true
  - slot: meeting_scheduled_event
    kind: event
    meaning: A meeting was scheduled with a customer
    properties:
    - name: deal_ids
      type: text
      meaning: Deals the meeting is linked to
      optional: false
    - name: user_ids
      type: text
      meaning: Users who attended the meeting
      optional: false
  - slot: deal_won_event
    kind: event
    meaning: A deal was marked won
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  - slot: deal_lost_event
    kind: event
    meaning: A deal was marked lost
    properties:
    - name: deal_id
      type: string
      meaning: Identifier of the deal
      optional: false
  - slot: call_completed_event
    kind: event
    meaning: A call with a customer was completed
    properties:
    - name: deal_id
      type: string
      meaning: Deal the call is linked to
      optional: true
  - slot: email_sent_event
    kind: event
    meaning: An email was sent to a customer about a deal
    properties:
    - name: deal_id
      type: string
      meaning: Deal the email is linked to
      optional: true
  steps:
  - id: s1
    builds: report
    uses:
    - deal_stage_event
    - meeting_scheduled_event
    - deal_won_event
    - deal_lost_event
    - window_closed
    - win_rate_window
    - threaded_benchmark_multiplier
    - benchmark_min_stakeholders
    - single_threaded_max
    - lightly_threaded_max
    - multi_threaded_max
    instruction: 'Create an Insights report named "Multi-Threading Coverage by Deal". Series A: count unique {deal_stage_event.user_ids}
      per active {deal_stage_event.deal_id}, counting distinct stakeholders attached to the deal across all stage events.
      Series B: same per-deal computation over {meeting_scheduled_event} events linked via {meeting_scheduled_event.deal_ids},
      counting distinct {meeting_scheduled_event.user_ids} who attended a meeting. Series C: bucket Series A into Single-threaded
      (1 contact), Lightly threaded (2-3), Multi-threaded (4-6), and Deeply threaded (7+) using {single_threaded_max}, {lightly_threaded_max},
      and {multi_threaded_max} as the upper bounds. Breakdown by current stage from {deal_stage_event.new_stage}, open deals
      only. Time range: all open deals plus closed deals within {window_closed}. Chart: stacked bar, one bar per stage, segments
      showing the threading-bucket distribution.'
---

# Multi threading coverage

Slash command: /multi-threading-coverage-by-deal

## Step 1: Count contacts on each deal

Create an Insights report called "Multi-Threading Coverage by Deal".
Series A: Event "Deal stage changed", scope: per active deal_id, aggregation: Count Unique users from the user_ids property (the distinct stakeholders attached to the deal across all stage events)
Series B: Same per-deal computation but counting only Meeting scheduled events linked to the deal (via deal_ids relation): distinct users who actually attended a meeting
Series C: Computed: Series A bucketed into "Single-threaded (1 contact)" / "Lightly threaded (2-3)" / "Multi-threaded (4-6)" / "Deeply threaded (7+)"
Breakdown: By deal stage (open deals only, group by current stage from Deal stage changed.new_stage)
Time range: All open deals + last 90 days of closed deals
Chart type: Stacked bar chart: bar per stage, segments showing the threading-bucket distribution
Also include a parallel "win-rate by threading level" view:
- For closed deals (Deal won + Deal lost) in the last 12 months, compute win rate by threading bucket
- Surface: single-threaded deals win X%, multi-threaded deals win Y%, with the gap quantified
Annotations:
- Flag any open deals (especially in late-stage proposal/negotiation) that are still single-threaded: these are at acute risk and need multi-threading action by the AE.
- Add the Gartner benchmark: B2B deals with 5+ engaged stakeholders close at 1.8× the rate of single-threaded deals.
- Highlight the share of pipeline value (sum of deal amount) currently sitting in single-threaded deals: this is the dollar amount at risk.
- Flag any deals where threading shrank vs. prior period (a stakeholder went silent: investigate champion-departure risk).
Use case: the standard B2B sales hygiene report. AEs are notoriously single-threaded; this report makes the risk visible and quantifies it in dollars. Top-performing sales orgs make this their #1 weekly review.
Taxonomy notes:
- Deal stage changed.user_ids is a relation (multi-value) carrying associated users.
- Meeting scheduled.user_ids and Meeting scheduled.deal_ids together let us count meeting-attended stakeholders per deal.
- Deal "current threading count" is computed across all events linked to the deal_id (Deal stage changed, Meeting scheduled, Call completed, Email sent).
