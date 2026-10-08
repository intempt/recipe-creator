---
description: Shows how many demo requests turn into booked meetings, completed demos, proposals and closed deals, and which lead sources actually convert.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
  org_name: intempt
classification:
  industry:
  - b2b-saas
---

# Lead to customer

Slash command: /lead-customer-sales

## Step 1: Trace demo requests to closed deals

Create a Funnel report called "Lead to Customer".
Steps:
1. Event "form_submitted" where form_id matches a demo-request form: "Requested Demo"
 (alternative: deal_created with stage matching "Discovery" or similar)
2. Event "meeting_scheduled" linked to the user (via primary_user_id or user_ids): "Scheduled Demo"
3. Event "meeting_scheduled" where canceled_at is null AND end_time < now (i.e. meeting actually happened, no subsequent meeting_canceled): "Completed Demo"
4. Event "deal_stage_changed" where new_stage matches a "Proposal" pattern: "Proposal Sent"
5. Event "deal_won": "Deal Closed"
Conversion window: 60 days
Breakdown: By Users.utm_source attribute (first-touch lead source on the User record). Top 8 sources.
Compare: Previous period (prior 60 days)
For each step, also surface:
- Median time-to-convert from previous step (stage velocity)
- Per-source conversion rate at each stage
- Forecast revenue: Sum of deal_created.amount (or current deal_stage_changed.amount) for deals currently at this stage × historical conversion-to-won rate
Annotations:
- Flag the lead source with highest end-to-end win rate AND volume: invest more there.
- Flag any stage where median velocity exceeded 14 days (deal-stalled signal).
- Highlight any source with rising volume but falling win rate (lead-quality erosion).
Surface the projected closed-won revenue for the period based on current pipeline volumes.
Taxonomy notes:
- "demo_requested", "demo_completed", "proposal_sent" as standalone events do not exist. They are derived from form_submitted, meeting_scheduled, and deal_stage_changed.new_stage respectively.
- deal_stage_changed has previous_stage and new_stage properties; deal stages are project-configured (the Deals object has stage as a relation attribute).
- meeting_scheduled has canceled_at, start_time, end_time: completion is derived from these.
- Users.utm_source is the canonical lead-source User attribute.
