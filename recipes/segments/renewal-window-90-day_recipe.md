---
name: renewal-window-90-day
description: |
  Use when a user mentions "renewal window — 90 days", or asks for related help. Subscriptions ending in next 90 days — foundation for renewal-flow journeys and NRR plays.
arguments: []
intempt:
  id: renewal-window-90-day
  version: 1.0.0
  slashCommand: /renewal-window-90-day
  group: Segments
  shortDescription: 'Subscriptions ending in next 90 days: foundation for renewal-flow journeys and NRR plays.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas]
    object: users
    complexity: standard
    executionMode: live
    tags: [users-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
  procedure:
    - step: 1
      title: "Configure Segment Rule"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Open the segment authoring surface, name the segment, and apply the rule below."
      prompt: |
        Create a segment called "Renewal Window — 90 Days".

        Object: Users

        Rules (all conditions joined by AND):
        - Attribute: end_date is within next 90 days
        - AND Attribute: end_date is in the future
        - AND Attribute: plan_name is not "free"

        Description: Users with active paid subscriptions ending in the next 90 days. The renewal-targeting cohort — foundation for QBR-style ROI emails, renewal-conversation triggers, and NRR-driven CSM outreach. NRR is the single most important SaaS metric in 2026; this segment makes the renewal pipeline actionable.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Renewal Window — 90 Days

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Renewal Window — 90 Days".

   Object: Users

   Rules (all conditions joined by AND):
   - Attribute: end_date is within next 90 days
   - AND Attribute: end_date is in the future
   - AND Attribute: plan_name is not "free"

   Description: Users with active paid subscriptions ending in the next 90 days. The renewal-targeting cohort — foundation for QBR-style ROI emails, renewal-conversation triggers, and NRR-driven CSM outreach. NRR is the single most important SaaS metric in 2026; this segment makes the renewal pipeline actionable.
   ```

## Taxonomy notes

- end_date is canonical Users attribute (subscription end timestamp).
- plan_name is canonical (excludes free-tier users who don't have renewal events).
- The "in the future" filter ensures we don't include subscriptions that have already lapsed — those belong in different cohorts (recently-churned-users or subscription-expired flows).
- Tighter renewal-window variants are common: 60-day cohort for late-stage CSM outreach, 30-day cohort for at-risk-renewal escalation. Clone this recipe per cadence the merchant runs.
- Pair with account_health and engagement_score on the Accounts side for a renewal-risk tier (healthy renewals get light-touch reminders; at-risk renewals get high-touch CSM intervention).
