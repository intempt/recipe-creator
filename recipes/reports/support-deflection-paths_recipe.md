---
name: support-deflection-paths
description: |
  Use when a user mentions "support deflection paths", or asks for related help. Backward path from ticket_created: surfaces in-product paths that immediately precede support tickets.
arguments: []
intempt:
  id: support-deflection-paths
  version: 1.0.0
  slashCommand: /support-deflection-paths
  group: Reports
  title: "Paths before a support ticket"
  shortDescription: "Shows what people were doing in the product just before they raised a ticket, and which page they gave up on."
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
      title: "Trace what leads to a ticket"
      command: build_paths_report
      produces: report
      bindsAs: report
      description: "The 7 steps before each ticket in the preceding 30 minutes, over the last 60 days and grouped by ticket theme or priority. Names the page people abandon most, any feature behind more than 5% of tickets, and tickets raised after a help page visit."
      prompt: |
        Create a Path report called "Support Deflection Paths".

        Anchor event: ticket_created
        Direction: backward
        Depth: 7 steps backward
        Window: 30 minutes before the ticket
        Loop compression: on
        Time range: Last 60 days
        Breakdown: By "subject" or "priority" property on ticket_created (cluster ticket subjects into ~6-10 thematic groups before breakdown)

        Surface:
        - The top 10 most-common in-product paths that precede a support ticket
        - For each path, the most common page_url visited last (the "page where the user gave up")
        - The % of tickets that follow a "/help" or "/docs" page_viewed (users tried self-help and failed) vs. tickets where users went straight from a feature failure to a ticket

        Annotations:
        - Flag the page where users most frequently "give up" before filing a ticket: this is the highest-value page to add inline help, tooltips, or improve UX.
        - Flag any in-product feature whose use precedes >5% of all tickets (the feature is generating disproportionate support load: investigate UX or documentation).
        - Highlight tickets where users visited /help OR /docs but still filed a ticket: these are documentation gaps; the existing help content didn't answer their question.
        - Flag if a meaningful share of tickets follow zero in-product activity (users contacted support without trying the product first: likely a top-of-funnel education issue).

        Industry benchmarks: 30-50% of support tickets are deflectable through better in-product help. Per the Feature Discovery / DEV Community literature, support ticket categorization showing "requests for functionality that already exists" is pure margin opportunity.

        Use case: identifies the specific in-product moments that generate support load. Each pattern is an opportunity for either UX fix, inline help, contextual tooltip, or documentation improvement: all of which deflect tickets at near-zero marginal cost.

        Taxonomy notes:
        - ticket_created is canonical with priority, subject, status, source_type properties.
        - page_viewed and click_on provide the in-product context preceding the ticket.
  outputs:
    - { name: report, type: report, cardinality: single, description: "Report produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Paths before a support ticket

Shows what people were doing in the product just before they raised a ticket, and which page they gave up on.

## What it does

1. **Trace what leads to a ticket** (`build_paths_report`)

   The 7 steps before each ticket in the preceding 30 minutes, over the last 60 days and grouped by ticket theme or priority. Names the page people abandon most, any feature behind more than 5% of tickets, and tickets raised after a help page visit.

## What you end up with

- **report** (report): Report produced by this recipe.
