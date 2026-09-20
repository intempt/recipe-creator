---
name: meeting-deal-linking-audit
description: Use when a user mentions "meeting deal linking", "unlinked meetings audit", "meeting CRM hygiene", or asks for related help. Find meetings not linked to a deal but that should be (account has an open deal, meeting type is revenue-impacting), AI-suggest the right deal, and batch-link via review. Closes a chronic gap that makes meeting analytics unreliable.
arguments: []
intempt:
  id: meeting-deal-linking-audit
  version: 1.0.0
  slashCommand: /meeting-deal-linking-audit
  group: Meetings
  title: "Link meetings to the right deal"
  shortDescription: "Finds sales calls from the last 60 days with no deal attached, suggests the right one, and keeps new meetings linked automatically from then on."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: meeting-notetaker
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [meeting-hygiene, crm-sync]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - list_meetings
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Find meetings with no deal"
      command: list_meetings
      produces: meeting_list
      bindsAs: unlinked_meetings
      description: "Revenue-impacting meetings from the last 60 days with no deal attached, listed with date, host, attendees and any open deals on their accounts."
      prompt: 'List all meetings from the last 60 days that have no linked deal. Filter to meetings where the meeting type is revenue-impacting (Discovery, Demo, Proposal, Close, Renewal: exclude internal sync, 1:1, interview). For each unlinked meeting, surface: meeting date, host, attendees (with company), and any open deals on attendees'' accounts. The output is the working set for the linking action.'
    - step: 2
      title: "Keep new meetings linked"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - unlinked_meetings
      description: "Runs daily over new unlinked meetings: links automatically when one deal clearly matches, asks the host to confirm when several could, and flags the rest."
      prompt: 'Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from the audit). For each: (1) compute the most-likely deal match: same account + open stage + attendees overlap with deal contacts; (2) if confidence is high (single clear match), auto-link via link_meeting_to_deal; (3) if confidence is medium (multiple plausible matches or attendees-don''t-overlap-deal-contacts), create a task for the meeting host asking them to confirm the right deal; (4) if no plausible match exists (account has no open deals), log to the dashboard for review (likely a new opp that needs a deal record).'
    - step: 3
      title: "Track linking coverage"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - unlinked_meetings
      - workflow
      description: "Share of revenue-impacting meetings linked to a deal, the split between automatic and manual links, and the hosts with the most unlinked meetings."
      prompt: 'Compose a meeting-deal-linking hygiene dashboard: % of revenue-impacting meetings linked to deals (target: 95%+; below 85% means the linking workflow is failing or reps aren''t acting on confirmation tasks); count of meetings auto-linked vs. manually-linked vs. unlinked-needing-review; top 5 hosts with most unlinked meetings (coaching signal); recent meetings where ''no plausible deal match'' was flagged (likely missing opportunities). Trend over time: falling linking-rate is a leading indicator of pipeline visibility decay.'
  outputs:
    - { name: meeting_list, type: meeting_list, cardinality: single, description: "Meeting List produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Link meetings to the right deal

Finds sales calls from the last 60 days with no deal attached, suggests the right one, and keeps new meetings linked automatically from then on.

## What it does

1. **Find meetings with no deal** (`list_meetings`)

   Revenue-impacting meetings from the last 60 days with no deal attached, listed with date, host, attendees and any open deals on their accounts.

2. **Keep new meetings linked** (`create_workflow`)

   Runs daily over new unlinked meetings: links automatically when one deal clearly matches, asks the host to confirm when several could, and flags the rest.

3. **Track linking coverage** (`create_dashboard`)

   Share of revenue-impacting meetings linked to a deal, the split between automatic and manual links, and the hosts with the most unlinked meetings.

## What you end up with

- **meeting_list** (meeting_list): Meeting List produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
