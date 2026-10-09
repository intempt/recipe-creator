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
1. Event "Form submitted" where form_id matches a demo-request form: "Requested Demo"
 (alternative: Deal created with stage matching "Discovery" or similar)
2. Event "Meeting scheduled" linked to the user (via primary_user_id or user_ids): "Scheduled Demo"
3. Event "Meeting scheduled" where canceled_at is null AND end_time < now (i.e. meeting actually happened, no subsequent meeting_canceled): "Completed Demo"
4. Event "Deal stage changed" where new_stage matches a "Proposal" pattern: "Proposal Sent"
5. Event "Deal won": "Deal Closed"
Conversion window: 60 days
Breakdown: By Users.UTM source attribute (first-touch lead source on the User record). Top 8 sources.
Compare: Previous period (prior 60 days)
For each step, also surface:
- Median time-to-convert from previous step (stage velocity)
- Per-source conversion rate at each stage
- Forecast revenue: Sum of Deal created.amount (or current Deal stage changed.amount) for deals currently at this stage × historical conversion-to-won rate
Annotations:
- Flag the lead source with highest end-to-end win rate AND volume: invest more there.
- Flag any stage where median velocity exceeded 14 days (deal-stalled signal).
- Highlight any source with rising volume but falling win rate (lead-quality erosion).
Surface the projected closed-won revenue for the period based on current pipeline volumes.
Taxonomy notes:
- "demo_requested", "demo_completed", "proposal_sent" as standalone events do not exist. They are derived from Form submitted, Meeting scheduled, and Deal stage changed.new_stage respectively.
- Deal stage changed has previous_stage and new_stage properties; deal stages are project-configured (the Deals object has stage as a relation attribute).
- Meeting scheduled has canceled_at, start_time, end_time: completion is derived from these.
- Users.UTM source is the canonical lead-source User attribute.
