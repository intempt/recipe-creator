---
id: closed-lost-revival
title: Closed lost revival
slash_command: /closed-lost-revival
group: Workflows
owner: intempt
summary: Goes back to deals lost 90 days ago, checks what has changed at the account, and reopens the
  conversation where the reason for losing may have expired.
description: >-
  Revive closed-lost deals 90 days after loss with a fresh re-evaluation outreach: context has likely
  changed (new initiatives, leadership, budget cycle). Typical revival rates: 5-10%, with low cost of
  outreach.
version: 2.0.0
classification:
  product:
    - sales
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - closed-lost-revival
    - pipeline-resurrection
prerequisites:
  events:
    - value: deal_lost
      severity: blocking
steps:
  - id: s1
    title: Find losses worth revisiting
    summary: >-
      Deals lost between 90 and 180 days ago where the reason was timing, budget, no decision, resourcing
      or a postponement. Wrong fit and a firm commitment to a competitor are left out, as is any account
      already lost three times.
    builds: segment
    description: >-
      Build a segment 'Closed-lost revival candidates' capturing deals where deal_lost event fired 90-180
      days ago AND lost_reason is NOT 'wrong-fit' or 'competitor-won-firm-commitment' (those won't revive).
      Includes deals lost to: timing, budget, no-decision, internal-resourcing, postponed. Excludes accounts
      that have entered closed-lost more than twice (3-strikes rule: stop pestering).
  - id: s2
    title: Write two revival emails
    summary: >-
      Day 0 refers to the actual reason they gave last time and asks whether anything has changed. Day
      14 shares a product update or a customer story that answers that original objection. From the AE
      who owned it, warm and low pressure, acknowledging the earlier no.
    builds: email_html
    description: >-
      Generate 2-touch revival email content. Touch 1 (Day 0): 'It's been a few months: wanted to check
      in. Last time we talked, [original_lost_reason]. Has anything changed?' Reference specific prior
      conversation context. Soft re-open, not a sales pitch. Touch 2 (Day 14, if no reply): share a relevant
      product update or customer story from a similar account that addresses their original objection.
      Send-from: the original AE owner. Tone: warm, low-pressure, acknowledging the prior 'no'. Use the
      result of "Find losses worth revisiting".
    dependsOn:
      - s1
  - id: s3
    title: Check what changed first
    summary: >-
      Daily, for each newly eligible deal, it refreshes the account: is the champion still there, is there
      new leadership, was there funding, did they launch something. A significant change raises an urgent
      AE task to reach out personally. Everything else goes into the two email sequence, and any response
      is logged on the original deal.
    builds: workflow
    description: >-
      Create a workflow firing daily for newly-eligible revival candidates. Step sequence: (1) refresh
      account enrichment (champion still there? new leadership? funding announced? product launched?);
      (2) IF significant change detected (new champion-role hire, funding round, etc.): create urgent
      AE task to manually reach out; ELSE trigger the standard 2-touch revival journey. Track responses
      and any new meeting bookings as revival_signal events on the original closed-lost deal record. Use
      the result of "Find losses worth revisiting", "Write two revival emails".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Send at day 0 and day 14
    summary: >-
      Both go to the original contact, with the second skipped if they reply or book. It ends on a booked
      meeting, which opens a new deal, on a reply, which goes to the AE, on unsubscribe, or after 30 days.
    builds: journey
    description: >-
      Build a 2-touch journey triggered by the revival workflow. Touch 1 at Day 0, Touch 2 at Day 14 (skipped
      if user replies or books meeting). Audience: the original deal's primary contact. Exit on: meeting_scheduled
      (revival success: open new deal), email_replied (warm handoff to AE), unsubscribe, or 30-day max
      duration. Use the result of "Find losses worth revisiting", "Write two revival emails", "Check what
      changed first".
    dependsOn:
      - s1
      - s2
      - s3
  - id: s5
    title: See what comes back to life
    summary: >-
      Deals entering revival each month, the reply rate, how many meetings come out of it, how many revived
      deals are won, and the ARR recovered this quarter, split by the original reason for losing.
    builds: dashboard
    description: >-
      Compose a revival performance dashboard: closed-lost deals entering revival per month, reply rate
      to revival outreach, meeting-booked rate from revival, revived-deal-to-win rate (final conversion),
      and ARR resurrected this quarter from revival pipeline. Break down by original lost_reason: which
      lost-reasons most often turn into revivals (informs sales coaching on when 'no' was actually 'not
      yet'). Use the result of "Find losses worth revisiting", "Write two revival emails", "Check what
      changed first", "Send at day 0 and day 14".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: workflow
    producedByStep: s3
    type: workflow
    description: Workflow produced by this recipe.
  - key: journey
    producedByStep: s4
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s5
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Closed lost revival

Goes back to deals lost 90 days ago, checks what has changed at the account, and reopens the conversation where the reason for losing may have expired.

## Steps

1. **Find losses worth revisiting** (builds segment)

   Deals lost between 90 and 180 days ago where the reason was timing, budget, no decision, resourcing or a postponement. Wrong fit and a firm commitment to a competitor are left out, as is any account already lost three times.

2. **Write two revival emails** (builds email_html)

   Day 0 refers to the actual reason they gave last time and asks whether anything has changed. Day 14 shares a product update or a customer story that answers that original objection. From the AE who owned it, warm and low pressure, acknowledging the earlier no.

3. **Check what changed first** (builds workflow)

   Daily, for each newly eligible deal, it refreshes the account: is the champion still there, is there new leadership, was there funding, did they launch something. A significant change raises an urgent AE task to reach out personally. Everything else goes into the two email sequence, and any response is logged on the original deal.

4. **Send at day 0 and day 14** (builds journey)

   Both go to the original contact, with the second skipped if they reply or book. It ends on a booked meeting, which opens a new deal, on a reply, which goes to the AE, on unsubscribe, or after 30 days.

5. **See what comes back to life** (builds dashboard)

   Deals entering revival each month, the reply rate, how many meetings come out of it, how many revived deals are won, and the ARR recovered this quarter, split by the original reason for losing.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, workflow.
