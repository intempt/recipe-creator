---
name: recently-signed-up-users
description: |
  Use when a user mentions "recently signed-up users", or asks for related help. Users who created an account in the last 30 days — onboarding cohort.
arguments: []
intempt:
  id: recently-signed-up-users
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a Users segment named Recently Signed-Up Users where first_seen_at is within the last 30 days."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas, ecommerce]
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
        Create a segment called "Recently Signed-Up Users".

        Object: Users

        Rules:
        - Attribute: first_seen_at is within last 30 days

        Description: Onboarding cohort. Use as the audience for first-week activation campaigns, welcome journeys, and onboarding email sequences.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Recently Signed-Up Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Recently Signed-Up Users".

   Object: Users

   Rules:
   - Attribute: first_seen_at is within last 30 days

   Description: Onboarding cohort. Use as the audience for first-week activation campaigns, welcome journeys, and onboarding email sequences.
   ```

## Taxonomy notes

- first_seen_at is canonical Users attribute (timestamp of first identification).
- Single-rule segment by design — keep it broad and let downstream journeys/personalizations narrow further.
- For SaaS specifically, layer with plan_name = "trial" or "free" to focus on non-paying signups during onboarding.
