---
id: meeting-deal-linking-audit
title: Link meetings to the right deal
slash_command: /meeting-deal-linking-audit
group: Meetings
owner: intempt
summary: Finds sales calls from the last 60 days with no deal attached, suggests the right one, and keeps
  new meetings linked automatically from then on.
description: >-
  Find meetings not linked to a deal but that should be (account has an open deal, meeting type is revenue-impacting),
  AI-suggest the right deal, and batch-link via review. Closes a chronic gap that makes meeting analytics
  unreliable.
version: 2.0.0
classification:
  product:
    - sales
  agent: meeting-notetaker
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - meeting-hygiene
    - crm-sync
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A meeting action, from step 1 "Find meetings with no deal"
    - A new workflow, from step 2 "Keep new meetings linked"
    - A new dashboard, from step 3 "Track linking coverage"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find meetings with no deal
    summary: >-
      Revenue-impacting meetings from the last 60 days with no deal attached, listed with date, host,
      attendees and any open deals on their accounts.
    builds: meeting
    description: >-
      List all meetings from the last 60 days that have no linked deal. Filter to meetings where the meeting
      type is revenue-impacting (Discovery, Demo, Proposal, Close, Renewal: exclude internal sync, 1:1,
      interview). For each unlinked meeting, surface: meeting date, host, attendees (with company), and
      any open deals on attendees' accounts. The output is the working set for the linking action.
  - id: s2
    title: Keep new meetings linked
    summary: >-
      Runs daily over new unlinked meetings: links automatically when one deal clearly matches, asks the
      host to confirm when several could, and flags the rest.
    builds: workflow
    description: >-
      Create a workflow firing daily that finds new unlinked revenue-impacting meetings (incremental from
      the audit). For each: (1) compute the most-likely deal match: same account + open stage + attendees
      overlap with deal contacts; (2) if confidence is high (single clear match), auto-link via link_meeting_to_deal;
      (3) if confidence is medium (multiple plausible matches or attendees-don't-overlap-deal-contacts),
      create a task for the meeting host asking them to confirm the right deal; (4) if no plausible match
      exists (account has no open deals), log to the dashboard for review (likely a new opp that needs
      a deal record). Use the result of "Find meetings with no deal".
    dependsOn:
      - s1
  - id: s3
    title: Track linking coverage
    summary: >-
      Share of revenue-impacting meetings linked to a deal, the split between automatic and manual links,
      and the hosts with the most unlinked meetings.
    builds: dashboard
    description: >-
      Compose a meeting-deal-linking hygiene dashboard: % of revenue-impacting meetings linked to deals
      (target: 95%+; below 85% means the linking workflow is failing or reps aren't acting on confirmation
      tasks); count of meetings auto-linked vs. manually-linked vs. unlinked-needing-review; top 5 hosts
      with most unlinked meetings (coaching signal); recent meetings where 'no plausible deal match' was
      flagged (likely missing opportunities). Trend over time: falling linking-rate is a leading indicator
      of pipeline visibility decay. Use the result of "Find meetings with no deal", "Keep new meetings
      linked".
    dependsOn:
      - s1
      - s2
outputs:
  - key: meeting_list
    producedByStep: s1
    type: meeting_list
    description: Meeting List produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Link meetings to the right deal

Finds sales calls from the last 60 days with no deal attached, suggests the right one, and keeps new meetings linked automatically from then on.

## Steps

1. **Find meetings with no deal** (builds meeting)

   Revenue-impacting meetings from the last 60 days with no deal attached, listed with date, host, attendees and any open deals on their accounts.

2. **Keep new meetings linked** (builds workflow)

   Runs daily over new unlinked meetings: links automatically when one deal clearly matches, asks the host to confirm when several could, and flags the rest.

3. **Track linking coverage** (builds dashboard)

   Share of revenue-impacting meetings linked to a deal, the split between automatic and manual links, and the hosts with the most unlinked meetings.

## What you end up with

- **meeting_list** (meeting_list): Meeting List produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A meeting action, from step 1 "Find meetings with no deal"
- A new workflow, from step 2 "Keep new meetings linked"
- A new dashboard, from step 3 "Track linking coverage"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, meeting, workflow.
