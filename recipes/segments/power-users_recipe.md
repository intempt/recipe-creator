---
name: power-users
description: |
  Use when a user mentions "power users", or asks for related help. Highly engaged users with frequent sessions and high activity score in the last 30 days.
arguments: []
intempt:
  id: power-users
  version: 1.0.0
  slashCommand: /segment-recipe
  group: Segments
  shortDescription: "Create a Users segment named 'Power Users' with session_start, click_on, engagement_score, and last_seen_at filters."
  availability: available
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [segments]
    agent: segment-architect
    mode: [all]
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
        Create a segment called "Power Users".

        Object: Users

        Rules (all conditions joined by AND):
        - Event: session_start occurred >= 10 times in last 30 days
        - AND Event: click_on occurred >= 20 times in last 30 days
        - AND Attribute: engagement_score = "High"
        - AND Attribute: last_seen_at is within last 7 days

        Description: Highly engaged users — frequent sessions, high engagement, recent activity. Priority cohort for advocacy programs, beta access, and case-study outreach.
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment created on /segments." }
---

# Power Users

## Procedure

1. **Configure Segment Rule** [`create_segment`] — Open the segment authoring surface, name the segment, and apply the rule below. → produces: segment

   ```text
   Create a segment called "Power Users".

   Object: Users

   Rules (all conditions joined by AND):
   - Event: session_start occurred >= 10 times in last 30 days
   - AND Event: click_on occurred >= 20 times in last 30 days
   - AND Attribute: engagement_score = "High"
   - AND Attribute: last_seen_at is within last 7 days

   Description: Highly engaged users — frequent sessions, high engagement, recent activity. Priority cohort for advocacy programs, beta access, and case-study outreach.
   ```

## Taxonomy notes

- session_start, click_on are canonical V2.1 events.
- engagement_score is canonical Users attribute and uses the enum bucket Low | Medium | High (no numeric thresholds).
- last_seen_at is canonical (replaces source template's "last_active_at" which is not canonical).
- "click_on >= 20 times" is intentionally generic. To filter clicks on a SPECIFIC feature, use click_on where target_id = "<concrete element id>" or page_url contains "<feature path>". The original source template's click_on where target = "feature" used a non-canonical property name and an over-broad value.
