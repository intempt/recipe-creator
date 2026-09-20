---
name: exit-paths-pre-cancellation
description: |
  Use when a user mentions "exit paths before cancellation", or asks for related help. Forward path from a /cancel page visit: surfaces what saves vs. kills retention attempts in the cancellation moment.
arguments: []
intempt:
  id: exit-paths-pre-cancellation
  version: 1.0.0
  slashCommand: /exit-paths-pre-cancellation
  group: Reports
  title: "Exit paths before cancellation"
  shortDescription: "Shows what people do after they land on your cancel page, and which of those paths end in a save rather than a cancellation."
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
      title: "Compare saved and lost cancels"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "The 5 steps after a cancel page visit inside a 60 minute window over the last 90 days, split into users who cancelled and users who did not, with a save rate per plan and the pages that show up on saved journeys but not on lost ones."
      prompt: |
        Create a Path report called "Exit Paths Before Cancellation".

        Anchor event: page_viewed where page_url contains "/cancel" OR "/account/billing" with cancellation intent (configurable URL pattern)
        Direction: forward
        Depth: 5 steps forward
        Window: 60 minutes after the cancel-page visit
        Loop compression: on
        Time range: Last 90 days
        Breakdown: By plan_name (resolved from the user's active subscription_created)

        Outcome split: render two side-by-side path views:
          - Path A: Users whose visit ended in subscription_cancelled within the window (lost)
          - Path B: Users whose visit ended in any non-cancellation outcome (saved)

        Surface:
        - For each outcome group, the top 10 most-common 5-step paths
        - The "save rate" overall and per plan: % of users who visited /cancel but did NOT cancel within 24 hours
        - The most common page_viewed events between /cancel page and session_end / cancellation (the "save plays" vs. "death paths")

        Annotations:
        - Flag any in-product surface (FAQ, plan-comparison, downgrade flow, contact-support) that meaningfully appears in Path B (saved) but not Path A (lost): these are working save plays; promote them more aggressively.
        - Flag any path step that appears in Path A immediately before cancellation (the "last straw" interactions: billing pages, plan limit messages, support-contact attempts).
        - Highlight the difference in path length between A and B: saved users typically take longer paths (consider alternatives, browse plans), lost users take shorter paths (decided before arriving). If save paths are short, the save-flow itself is too easy to escape.

        Use case: distinct from the existing pre-churn-behavioral-signals recipe (which looks 30 days back from cancellation). This recipe focuses on the LAST-SESSION moment when the user is actively considering canceling: the highest-leverage, highest-urgency intervention window.

        Taxonomy notes:
        - subscription_cancelled is canonical (British spelling). The "considering cancellation" trigger is derived from page_viewed.page_url patterns; if the workspace emits a custom event for cancellation-intent (e.g. cancel_clicked), it can be substituted.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Exit paths before cancellation

Shows what people do after they land on your cancel page, and which of those paths end in a save rather than a cancellation.

## What it does

1. **Compare saved and lost cancels** (`build_paths_report`)

   The 5 steps after a cancel page visit inside a 60 minute window over the last 90 days, split into users who cancelled and users who did not, with a save rate per plan and the pages that show up on saved journeys but not on lost ones.

## What you end up with

- **report** (report): Report produced by this recipe.
