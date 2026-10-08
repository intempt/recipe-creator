---
description: Shows how leads move through MQL, SQL, demo and closed won, where they stall, and how long the whole cycle takes.
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

# Lead qualification funnel

Slash command: /lead-to-mql-to-sql-funnel

## Step 1: Track leads through qualification

Create a Funnel report called "Lead Qualification Funnel".
Steps:
1. Event "user_created" where Users.utm_source is not empty: "Lead Created"
2. Event "lead_stage_changed" where new_stage indicates MQL (lead_stage relation matches MQL stage in the project's lead-stage configuration), aggregation: Count Unique Users per lead: "Reached MQL"
3. Event "deal_created" linked to the user (via primary_user_id or user_ids): "SQL Created"
4. Event "meeting_scheduled" where canceled_at is null AND end_time < now: "Demo Completed"
5. Event "deal_won": "Closed Won"
Conversion window: 90 days
Breakdown: By Users.utm_source (top 6 sources)
Compare: Previous period (prior 90 days)
For each step, also surface:
- Median time-to-convert from previous step
- Per-source conversion rate at each stage
- Stage velocity from Step 1 to Step 5 (full sales-cycle length)
Annotations:
- Flag the largest stage drop-off.
- Flag any source where MQL-to-SQL conversion is below 20% (MQL definition issue for that source).
- Flag any source where SQL-to-Closed-Won is below 15% (deal-execution issue).
- Highlight sources with high volume AND end-to-end conversion >5%.
Surface the median sales-cycle length and whether it's increasing or decreasing.
Taxonomy notes:
- "lead_score" as a property is not canonical. Lead progression is tracked via lead_stage_changed events (which include score, intent_trend, stage_changed_by properties). The lead_stage relation on the User points to a configured lead-stage record.
- The MQL/SQL boundary is project-specific; the recipe uses the lead_stage_changed.new_stage relation against the project's stage configuration.
