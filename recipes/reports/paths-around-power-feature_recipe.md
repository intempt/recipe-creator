---
name: paths-around-power-feature
description: |
  Use when a user mentions "paths around a power feature", or asks for related help. Bidirectional path bracketing a high-value feature interaction — surfaces what leads to discovery and what users do after.
arguments: []
intempt:
  id: paths-around-power-feature
  version: 1.0.0
  slashCommand: /paths-around-power-feature
  group: Reports
  shortDescription: "Bidirectional path bracketing a high-value feature interaction — surfaces what leads to discovery and what users do after."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [analytics]
    agent: data-analyst
    mode: [saas]
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
        Create a Path report called "Paths Around a Power Feature".

        This is a TWO-PATH report (forward and backward) bracketing a configurable target feature, identified by click_on.target_id.

        Path A — Backward (what leads users to the feature):
        - Anchor event: click_on where target_id matches the target feature pattern
        - Direction: backward
        - Depth: 5 steps backward
        - Window: 30 minutes before the feature interaction
        - Loop compression: on

        Path B — Forward (what users do after using the feature):
        - Anchor event: same click_on
        - Direction: forward
        - Depth: 5 steps forward
        - Window: 30 minutes after the feature interaction
        - Loop compression: on

        Time range: Last 30 days
        Breakdown: By plan_name (resolved from each user's most-recent active subscription_created.plan_name)

        Surface for both paths:
        - The top 10 most-common precursor paths (Path A) and follow-on paths (Path B)
        - The % of users who arrived via each path (intentional discovery vs. accidental)
        - The % of users for whom this was their FIRST interaction with the feature in the trailing 90 days

        Annotations:
        - Path A — flag if the dominant precursor is "page_viewed on /help" or "click_on a tooltip" (feature is being discovered through help, not natural workflow — discoverability issue).
        - Path A — flag if the dominant precursor is from settings/admin (advanced feature only used by admins, not the broader user base).
        - Path B — flag if the dominant follow-on is session_end (users disengage after using the feature — signals confusion or completion of a single task, not workflow integration).
        - Path B — flag if the feature leads to repeated use of itself within session (sticky / habit-forming pattern).

        Use case: when prioritizing investment in a feature, knowing how users arrive at it AND what they do after reveals whether the feature is well-positioned in the product workflow or sits in isolation. The KISSmetrics product analytics literature flags this as one of the most-overlooked path use cases.

        Taxonomy notes:
        - click_on is canonical with target_id, target_text, hierarchy, path properties.
        - session_end is the canonical session-disengagement marker.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---

# Paths Around a Power Feature

## Procedure

1. **Build Path Report** [`build_paths_report`] — Configure and materialize the report described below. → produces: report

   ```text
   Create a Path report called "Paths Around a Power Feature".

   This is a TWO-PATH report (forward and backward) bracketing a configurable target feature, identified by click_on.target_id.

   Path A — Backward (what leads users to the feature):
   - Anchor event: click_on where target_id matches the target feature pattern
   - Direction: backward
   - Depth: 5 steps backward
   - Window: 30 minutes before the feature interaction
   - Loop compression: on

   Path B — Forward (what users do after using the feature):
   - Anchor event: same click_on
   - Direction: forward
   - Depth: 5 steps forward
   - Window: 30 minutes after the feature interaction
   - Loop compression: on

   Time range: Last 30 days
   Breakdown: By plan_name (resolved from each user's most-recent active subscription_created.plan_name)

   Surface for both paths:
   - The top 10 most-common precursor paths (Path A) and follow-on paths (Path B)
   - The % of users who arrived via each path (intentional discovery vs. accidental)
   - The % of users for whom this was their FIRST interaction with the feature in the trailing 90 days

   Annotations:
   - Path A — flag if the dominant precursor is "page_viewed on /help" or "click_on a tooltip" (feature is being discovered through help, not natural workflow — discoverability issue).
   - Path A — flag if the dominant precursor is from settings/admin (advanced feature only used by admins, not the broader user base).
   - Path B — flag if the dominant follow-on is session_end (users disengage after using the feature — signals confusion or completion of a single task, not workflow integration).
   - Path B — flag if the feature leads to repeated use of itself within session (sticky / habit-forming pattern).

   Use case: when prioritizing investment in a feature, knowing how users arrive at it AND what they do after reveals whether the feature is well-positioned in the product workflow or sits in isolation. The KISSmetrics product analytics literature flags this as one of the most-overlooked path use cases.

   Taxonomy notes:
   - click_on is canonical with target_id, target_text, hierarchy, path properties.
   - session_end is the canonical session-disengagement marker.
   ```
