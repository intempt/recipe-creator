---
name: champion-change-detection
description: Use when a user mentions "champion change detection", "champion departure alert", "stakeholder turnover workflow", or asks for related help. Detect when a deal's identified champion changes role, departs the company, or stops responding, the highest-leverage early-warning signal for stalled deals. Trigger stakeholder re-engagement workflow before the deal silently dies.
arguments: []
intempt:
  id: champion-change-detection
  title: "Champion change detection"
  version: 1.0.0
  slashCommand: /champion-change-detection
  group: Workflows
  shortDescription: "Notices when the person backing a deal goes quiet or leaves, names who could replace them, and gets the rep moving before the deal dies quietly."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [champion-tracking, deal-health, early-warning]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: email_bounced, severity: recommended }
      - { value: user_identified, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Track the champion daily"
      command: create_ai_attribute
      produces: attribute
      bindsAs: champion_status
      description: "Active means they replied in the last 21 days, quiet means 21 to 45 days of silence, and gone means a bounced email, a departure signal, or enrichment showing a new company or a new title. Deals with nobody identified are flagged separately."
      prompt: 'Create an AI-derived attribute ''champion status'' on the Deal object. Compute the deal''s current champion status: ACTIVE (responding to outreach in last 21 days), QUIET (no response 21-45 days), GONE (bounced email OR explicit departure signal OR LinkedIn enrichment shows new company OR new title at same company), or UNCLEAR (deal has no identified champion: separate flag). Refreshed daily. The GONE detection combines: hard email bounces, opened-but-no-reply patterns, enrichment data refresh, and account-domain consistency checks.'
    - step: 2
      title: "Find deals that lost theirs"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - champion_status
      description: "Open deals whose champion went to gone in the last 7 days, plus deals quiet for 45 days or more, which amounts to the same thing. Closed lost deals are handled elsewhere."
      prompt: Build a segment 'Champion-change deals' capturing open deals where champion status transitioned to GONE in the last 7 days. Also includes deals where status is QUIET for 45+ days (effectively gone). Excludes deals already in closed-lost (handled separately).
    - step: 3
      title: "Get the rep moving"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - champion_status
      - segment
      description: "It pulls replacement candidates from the account, peers, a manager or the same role elsewhere, raises an urgent task for the AE with that list and the deal history, alerts the AE and their manager in Slack, tags the deal as at risk so the forecast tells the truth, and points at any other contact active in the last 30 days as the warm way in. No email goes out automatically: the rep reaches out personally."
      prompt: 'Create a workflow firing when champion status transitions to GONE. Step sequence: (1) identify replacement-champion candidates from the account (similar role, peer, manager up: pulled from enrichment); (2) create an urgent task for the AE: ''Champion gone: re-engage stakeholders'' with the candidate list and prior deal context; (3) post critical-tier Slack alert to the AE and their manager (this is a deal-saving moment); (4) flag the deal in CRM with champion-risk tag so forecast calls reflect reality; (5) IF account has any other active contact (engagement signal in last 30 days), prioritize that contact as warm-handoff. Don''t auto-send email: rep must reach out personally.'
    - step: 4
      title: "See the ARR behind the risk"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - champion_status
      - segment
      - workflow
      description: "Open deals by champion status, the ARR sitting behind departed champions, how often champions leave, how many deals survive it, and how quickly reps act, with anything left 14 days without action pulled out."
      prompt: 'Compose a champion risk dashboard: count of open deals by champion status, total ARR with GONE champions (the at-risk forecast), champion-departure rate trend, re-engagement success rate (deals that recovered after champion-change vs. died), and time-to-rep-action on champion-gone alerts. Surface deals where champion has been GONE 14+ days with no rep action (escalation pile).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Champion change detection

Notices when the person backing a deal goes quiet or leaves, names who could replace them, and gets the rep moving before the deal dies quietly.

## Before you run it

- Connect slack
- Send the `email_bounced` event
- Send the `user_identified` event

## What it does

1. **Track the champion daily** (`create_ai_attribute`)

   Active means they replied in the last 21 days, quiet means 21 to 45 days of silence, and gone means a bounced email, a departure signal, or enrichment showing a new company or a new title. Deals with nobody identified are flagged separately.

2. **Find deals that lost theirs** (`create_segment`)

   Open deals whose champion went to gone in the last 7 days, plus deals quiet for 45 days or more, which amounts to the same thing. Closed lost deals are handled elsewhere.

3. **Get the rep moving** (`create_workflow`)

   It pulls replacement candidates from the account, peers, a manager or the same role elsewhere, raises an urgent task for the AE with that list and the deal history, alerts the AE and their manager in Slack, tags the deal as at risk so the forecast tells the truth, and points at any other contact active in the last 30 days as the warm way in. No email goes out automatically: the rep reaches out personally.

4. **See the ARR behind the risk** (`create_dashboard`)

   Open deals by champion status, the ARR sitting behind departed champions, how often champions leave, how many deals survive it, and how quickly reps act, with anything left 14 days without action pulled out.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
