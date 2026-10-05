---
name: meeting-deal-linking-audit
description: Use when a user mentions "meeting deal linking", "unlinked meetings audit", "meeting CRM hygiene", or asks for related help. Find meetings not linked to a deal but that should be (account has an open deal, meeting type is revenue-impacting), AI-suggest the right deal, and batch-link via review. Closes a chronic gap that makes meeting analytics unreliable.
arguments: []
intempt:
  id: meeting-deal-linking-audit
  version: 1.0.0
  slashCommand: /meeting-deal-linking-audit
  group: Meetings
  shortDescription: "Produces a reviewed list of unlinked revenue-impacting meetings plus a daily workflow that suggests and links the correct open deal."
  availability: coming-soon
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
      title: Find Unlinked Meetings
      command: list_meetings
      produces: meeting_list
      bindsAs: unlinked_meetings
      description: 'List all meetings from the last 60 days that have no linked deal. Filter to meetings where the meeting type is revenue-impacting (Discovery, Demo, Proposal, Close, Renewal — exclude internal sync, 1:1, interview). For each unlinked meeting, surface: meeting date, host, attendees (with company), and any open deals on attendees'' accounts. The output is the working set for the linking action.'
      prompt: 'List all meetings from the last 60 days that have no linked deal. Filter to meetings where the meeting type is revenue-impacting (Discovery, Demo, Proposal, Close, Renewal — exclude internal sync, 1:1, interview). For each unlinked meeting, surface: meeting date, host, attendees (with company), and any open deals on attendees'' accounts. The output is the working set for the linking action.'
    - step: 2
      title: Build Linking Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - unlinked_meetings
      description: 'Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from the audit). For each: (1) compute the most-likely deal match — same account + open stage + attendees overlap with deal contacts; (2) if confidence is high (single clear match), auto-link via link_meeting_to_deal; (3) if confidence is medium (multiple plausible matches or attendees-don''t-overlap-deal-contacts), create a task for the meeting host asking them to confirm the right deal; (4) if no plausible match exists (account has no open deals), log to the dashboard for review (likely a new opp that needs a deal record).'
      prompt: 'Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from the audit). For each: (1) compute the most-likely deal match — same account + open stage + attendees overlap with deal contacts; (2) if confidence is high (single clear match), auto-link via link_meeting_to_deal; (3) if confidence is medium (multiple plausible matches or attendees-don''t-overlap-deal-contacts), create a task for the meeting host asking them to confirm the right deal; (4) if no plausible match exists (account has no open deals), log to the dashboard for review (likely a new opp that needs a deal record).'
    - step: 3
      title: Build Linking Hygiene Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - unlinked_meetings
      - workflow
      description: 'Compose a meeting-deal-linking hygiene dashboard: % of revenue-impacting meetings linked to deals (target: 95%+; below 85% means the linking workflow is failing or reps aren''t acting on confirmation tasks); count of meetings auto-linked vs. manually-linked vs. unlinked-needing-review; top 5 hosts with most unlinked meetings (coaching signal); recent meetings where ''no plausible deal match'' was flagged (likely missing opportunities). Trend over time — falling linking-rate is a leading indicator of pipeline visibility decay.'
      prompt: 'Compose a meeting-deal-linking hygiene dashboard: % of revenue-impacting meetings linked to deals (target: 95%+; below 85% means the linking workflow is failing or reps aren''t acting on confirmation tasks); count of meetings auto-linked vs. manually-linked vs. unlinked-needing-review; top 5 hosts with most unlinked meetings (coaching signal); recent meetings where ''no plausible deal match'' was flagged (likely missing opportunities). Trend over time — falling linking-rate is a leading indicator of pipeline visibility decay.'
  outputs:
    - { name: meeting_list, type: meeting_list, cardinality: single, description: "Meeting List produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Meeting Deal Linking Audit

## Procedure

1. **Find Unlinked Meetings** [`list_meetings`] — List all meetings from the last 60 days that have no linked deal. Filter to meetings where the meeting type is revenue-impacting (Discovery, Demo, Proposal, Close, Renewal — exclude internal sync, 1:1, interview). For each unlinked meeting, surface: meeting date, host, attendees (with company), and any open deals on attendees' accounts. The output is the working set for the linking action. → produces: meeting_list
2. **Build Linking Workflow** [`create_workflow`] — Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from the audit). For each: (1) compute the most-likely deal match — same account + open stage + attendees overlap with deal contacts; (2) if confidence is high (single clear match), auto-link via link_meeting_to_deal; (3) if confidence is medium (multiple plausible matches or attendees-don't-overlap-deal-contacts), create a task for the meeting host asking them to confirm the right deal; (4) if no plausible match exists (account has no open deals), log to the dashboard for review (likely a new opp that needs a deal record). → produces: workflow
3. **Build Linking Hygiene Dashboard** [`create_dashboard`] — Compose a meeting-deal-linking hygiene dashboard: % of revenue-impacting meetings linked to deals (target: 95%+; below 85% means the linking workflow is failing or reps aren't acting on confirmation tasks); count of meetings auto-linked vs. manually-linked vs. unlinked-needing-review; top 5 hosts with most unlinked meetings (coaching signal); recent meetings where 'no plausible deal match' was flagged (likely missing opportunities). Trend over time — falling linking-rate is a leading indicator of pipeline visibility decay. → produces: dashboard
