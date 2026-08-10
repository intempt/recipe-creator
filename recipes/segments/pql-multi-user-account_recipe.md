---
name: pql-multi-user-account
description: |
  Use when a user mentions "pql — multi-user account", or asks for related help. Free/trial accounts with 2+ engaged users from same company — enterprise PQL signal.
arguments: []
intempt:
  id: pql-multi-user-account
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Free/trial accounts with 2+ engaged users from same company — enterprise PQL signal."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [saas]
    object: accounts
    complexity: standard
    executionMode: live
    tags: [accounts-segment]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
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
        Create a segment called "PQL — Multi-User Account".

        Object: Accounts

        Rules (all conditions joined by AND):
        - Attribute: users_count >= 2
        - AND Event (across users in account): session_start occurred >= 3 times in last 14 days
        - AND Event (across users in account): goal_completed_in_journey occurred >= 1 time in last 14 days

        Description: Accounts where 2+ users from the same company are actively engaged in trial or free plan. The enterprise PQL signal — distinguishes team-buying behavior from individual-trial signups. Highest-converting PQL cohort: when multiple stakeholders test the product, they convert at 2-3x the rate of individual-trial PQLs.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# PQL — Multi-User Account

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "PQL — Multi-User Account".

   Object: Accounts

   Rules (all conditions joined by AND):
   - Attribute: users_count >= 2
   - AND Event (across users in account): session_start occurred >= 3 times in last 14 days
   - AND Event (across users in account): goal_completed_in_journey occurred >= 1 time in last 14 days

   Description: Accounts where 2+ users from the same company are actively engaged in trial or free plan. The enterprise PQL signal — distinguishes team-buying behavior from individual-trial signups. Highest-converting PQL cohort: when multiple stakeholders test the product, they convert at 2-3x the rate of individual-trial PQLs.
   ```

## Taxonomy notes

- users_count is canonical Accounts attribute.
- session_start, goal_completed_in_journey are canonical events.
- This is the canonical Slack/Dropbox/Figma PQL pattern — the "team adoption" signal that distinguishes self-service paid conversions from enterprise upgrade paths.
- For workspaces tracking specific feature events (e.g., file_uploaded, document_shared, comment_added), layer with those feature-specific events for sharper team-collaboration signal.
- Distinct from generic engaged-free-users (single-user level) — this segment requires multiple users from the SAME company engaging together, which is the canonical team-PQL signal that warrants AE outreach rather than self-serve nurture.
