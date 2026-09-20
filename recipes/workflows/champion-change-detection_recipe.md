---
name: champion-change-detection
description: Use when a user mentions "champion change detection", "champion departure alert", "stakeholder turnover workflow", or asks for related help. Detect when a deal's identified champion changes role, departs the company, or stops responding — the highest-leverage early-warning signal for stalled deals. Trigger stakeholder re-engagement workflow before the deal silently dies.
arguments: []
intempt:
  id: champion-change-detection
  version: 1.0.0
  slashCommand: /champion-change-detection
  group: Workflows
  shortDescription: 'Detect when a deal''s identified champion changes role, departs the company, or stops responding: the highest-leverage early-warning signal for stalled deals. Trigger stakeholder re-engagement workflow before the deal silently dies.'
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
      title: Detect Champion Status Changes
      command: create_ai_attribute
      produces: attribute
      bindsAs: champion_status
      description: 'Create an AI-derived attribute ''champion_status'' on the Deal object. Compute the deal''s current champion status: ACTIVE (responding to outreach in last 21 days), QUIET (no response 21-45 days), GONE (bounced email OR explicit departure signal OR LinkedIn enrichment shows new company OR new title at same company), or UNCLEAR (deal has no identified champion — separate flag). Refreshed daily. The GONE detection combines: hard email bounces, opened-but-no-reply patterns, enrichment data refresh, and account-domain consistency checks.'
      prompt: 'Create an AI-derived attribute ''champion_status'' on the Deal object. Compute the deal''s current champion status: ACTIVE (responding to outreach in last 21 days), QUIET (no response 21-45 days), GONE (bounced email OR explicit departure signal OR LinkedIn enrichment shows new company OR new title at same company), or UNCLEAR (deal has no identified champion — separate flag). Refreshed daily. The GONE detection combines: hard email bounces, opened-but-no-reply patterns, enrichment data refresh, and account-domain consistency checks.'
    - step: 2
      title: Identify Champion-Change Deals
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - champion_status
      description: Build a segment 'Champion-change deals' capturing open deals where champion_status transitioned to GONE in the last 7 days. Also includes deals where status is QUIET for 45+ days (effectively gone). Excludes deals already in closed-lost (handled separately).
      prompt: Build a segment 'Champion-change deals' capturing open deals where champion_status transitioned to GONE in the last 7 days. Also includes deals where status is QUIET for 45+ days (effectively gone). Excludes deals already in closed-lost (handled separately).
    - step: 3
      title: Build Re-engagement Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - champion_status
      - segment
      description: 'Create a workflow firing when champion_status transitions to GONE. Step sequence: (1) identify replacement-champion candidates from the account (similar role, peer, manager up — pulled from enrichment); (2) create an urgent task for the AE: ''Champion gone: re-engage stakeholders'' with the candidate list and prior deal context; (3) post critical-tier Slack alert to the AE and their manager (this is a deal-saving moment); (4) flag the deal in CRM with champion-risk tag so forecast calls reflect reality; (5) IF account has any other active contact (engagement signal in last 30 days), prioritize that contact as warm-handoff. Don''t auto-send email — rep must reach out personally.'
      prompt: 'Create a workflow firing when champion_status transitions to GONE. Step sequence: (1) identify replacement-champion candidates from the account (similar role, peer, manager up — pulled from enrichment); (2) create an urgent task for the AE: ''Champion gone: re-engage stakeholders'' with the candidate list and prior deal context; (3) post critical-tier Slack alert to the AE and their manager (this is a deal-saving moment); (4) flag the deal in CRM with champion-risk tag so forecast calls reflect reality; (5) IF account has any other active contact (engagement signal in last 30 days), prioritize that contact as warm-handoff. Don''t auto-send email — rep must reach out personally.'
    - step: 4
      title: Build Champion Risk Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - champion_status
      - segment
      - workflow
      description: 'Compose a champion risk dashboard: count of open deals by champion_status, total ARR with GONE champions (the at-risk forecast), champion-departure rate trend, re-engagement success rate (deals that recovered after champion-change vs. died), and time-to-rep-action on champion-gone alerts. Surface deals where champion has been GONE 14+ days with no rep action (escalation pile).'
      prompt: 'Compose a champion risk dashboard: count of open deals by champion_status, total ARR with GONE champions (the at-risk forecast), champion-departure rate trend, re-engagement success rate (deals that recovered after champion-change vs. died), and time-to-rep-action on champion-gone alerts. Surface deals where champion has been GONE 14+ days with no rep action (escalation pile).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Champion Change Detection

## Procedure

1. **Detect Champion Status Changes** [`create_ai_attribute`] — Create an AI-derived attribute 'champion_status' on the Deal object. Compute the deal's current champion status: ACTIVE (responding to outreach in last 21 days), QUIET (no response 21-45 days), GONE (bounced email OR explicit departure signal OR LinkedIn enrichment shows new company OR new title at same company), or UNCLEAR (deal has no identified champion — separate flag). Refreshed daily. The GONE detection combines: hard email bounces, opened-but-no-reply patterns, enrichment data refresh, and account-domain consistency checks. → produces: attribute
2. **Identify Champion-Change Deals** [`create_segment`] — Build a segment 'Champion-change deals' capturing open deals where champion_status transitioned to GONE in the last 7 days. Also includes deals where status is QUIET for 45+ days (effectively gone). Excludes deals already in closed-lost (handled separately). → produces: segment
3. **Build Re-engagement Workflow** [`create_workflow`] — Create a workflow firing when champion_status transitions to GONE. Step sequence: (1) identify replacement-champion candidates from the account (similar role, peer, manager up — pulled from enrichment); (2) create an urgent task for the AE: 'Champion gone: re-engage stakeholders' with the candidate list and prior deal context; (3) post critical-tier Slack alert to the AE and their manager (this is a deal-saving moment); (4) flag the deal in CRM with champion-risk tag so forecast calls reflect reality; (5) IF account has any other active contact (engagement signal in last 30 days), prioritize that contact as warm-handoff. Don't auto-send email — rep must reach out personally. → produces: workflow
4. **Build Champion Risk Dashboard** [`create_dashboard`] — Compose a champion risk dashboard: count of open deals by champion_status, total ARR with GONE champions (the at-risk forecast), champion-departure rate trend, re-engagement success rate (deals that recovered after champion-change vs. died), and time-to-rep-action on champion-gone alerts. Surface deals where champion has been GONE 14+ days with no rep action (escalation pile). → produces: dashboard
