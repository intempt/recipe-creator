---
name: first-session-paths-after-signup
description: |
  Use when a user mentions "first-session paths after signup", or asks for related help. Forward path from user_created showing what new users actually do in their first session vs. the intended onboarding flow.
arguments: []
intempt:
  id: first-session-paths-after-signup
  version: 1.0.0
  slashCommand: /first-session-paths-after-signup
  group: Reports
  shortDescription: "Forward path from user_created showing what new users actually do in their first session vs. the intended onboarding flow."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas, ecommerce]
    complexity: quick
    executionMode: live
    tags: [path]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - build_paths_report
  procedure:
    - step: 1
      title: "Build Path Report"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "Configure and materialize the report described below."
      prompt: |
        Create a Path report called "First-Session Paths After Signup".

        Anchor event: user_created
        Direction: forward
        Depth: 7 steps
        Window: 24 hours after user_created
        Loop compression: on
        Time range: Last 30 days of new signups
        Breakdown: By Users.utm_source (top 6 sources)

        Surface:
        - The top 10 most-common 7-step paths emerging from user_created within the first 24 hours
        - For each emerging path, the % of users who took it and the % of those users who later reached an activation goal_completed_in_journey within 14 days
        - Compare against the intended onboarding flow (configurable as the canonical path the recipe operator expects users to take)

        Annotations:
        - Flag the top 3 emerging paths that diverge from the intended onboarding flow — these are signals that the in-product path doesn't match the designed experience.
        - Flag any emerging path with >10% volume share but <15% downstream activation rate (high-traffic dead end).
        - Highlight emerging paths with >25% downstream activation rate — these are the natural successful flows; promote them as the default.
        - Surface the most common "first action" event after user_created (often surprising — users may go to settings/help/pricing instead of the intended next step).

        Use case: identify gaps between intended and actual onboarding behavior. Most product teams design an onboarding flow but never validate whether users follow it. The PLG community considers this the highest-leverage path analysis a SaaS product can run.

        Taxonomy notes:
        - user_created is canonical. session_start, click_on, page_viewed, goal_completed_in_journey all carry the relevant context properties for this analysis.
        - Users.utm_source is the canonical first-touch source attribute.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# First-Session Paths After Signup

## Procedure

1. **Build Path Report** [`build_paths_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Path report called "First-Session Paths After Signup".

   Anchor event: user_created
   Direction: forward
   Depth: 7 steps
   Window: 24 hours after user_created
   Loop compression: on
   Time range: Last 30 days of new signups
   Breakdown: By Users.utm_source (top 6 sources)

   Surface:
   - The top 10 most-common 7-step paths emerging from user_created within the first 24 hours
   - For each emerging path, the % of users who took it and the % of those users who later reached an activation goal_completed_in_journey within 14 days
   - Compare against the intended onboarding flow (configurable as the canonical path the recipe operator expects users to take)

   Annotations:
   - Flag the top 3 emerging paths that diverge from the intended onboarding flow — these are signals that the in-product path doesn't match the designed experience.
   - Flag any emerging path with >10% volume share but <15% downstream activation rate (high-traffic dead end).
   - Highlight emerging paths with >25% downstream activation rate — these are the natural successful flows; promote them as the default.
   - Surface the most common "first action" event after user_created (often surprising — users may go to settings/help/pricing instead of the intended next step).

   Use case: identify gaps between intended and actual onboarding behavior. Most product teams design an onboarding flow but never validate whether users follow it. The PLG community considers this the highest-leverage path analysis a SaaS product can run.

   Taxonomy notes:
   - user_created is canonical. session_start, click_on, page_viewed, goal_completed_in_journey all carry the relevant context properties for this analysis.
   - Users.utm_source is the canonical first-touch source attribute.
   ```
