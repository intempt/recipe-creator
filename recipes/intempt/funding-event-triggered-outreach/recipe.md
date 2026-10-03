---
id: funding-event-triggered-outreach
title: Outreach on a funding round
slash_command: /funding-event-triggered-outreach
group: Workflows
owner: intempt
summary: Catches an account raising money, refreshes who works there now, drafts a congratulations with
  a budget angle, and asks the AE to act within a day.
description: >-
  When an account in your CRM raises new funding (detected via web monitoring or webhook from a signal
  provider), enrich the account, identify newly-empowered decision-makers, AI-draft a congratulatory outreach
  with budget angle, and create an AE task. Signal-qualified prospecting drives 4-7x higher conversion
  than cold.
version: 2.0.0
classification:
  product:
    - sales
  agent: workflow-builder
  mode:
    - b2b
  complexity: advanced
  executionMode: live
  tags:
    - signal-triggered
    - funding-event
    - intent-data
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: external_signal_received
      severity: blocking
steps:
  - id: s1
    title: Watch for funding news
    summary: >-
      Triggered by a webhook from a signal provider, or by a scheduled scrape of funding news for your
      target domains. The aim is to be among the first to reach out while the budget is fresh.
    builds: workflow
    description: >-
      Create a workflow 'Funding-event-triggered outreach' triggered by webhook from a signal provider
      (Crunchbase, PitchBook, or scraped TechCrunch RSS) OR by a scheduled scrape of funding news for
      target-account domains. Goal: be among the first to reach out post-funding when budget is fresh
      and growth-investment mood is high.
  - id: s2
    title: Accept the funding event
    summary: >-
      The webhook takes the company domain, the round, the amount raised, the investors and the announcement
      date, and rejects anything malformed.
    builds: workflow
    description: >-
      Configure the webhook trigger to receive funding-event payloads from external sources. Expected
      payload: company_domain, round_type (seed/A/B/C/etc), amount_raised, investors, announcement_date.
      Validate payload schema; reject malformed events. Use the result of "Watch for funding news".
    dependsOn:
      - s1
  - id: s3
    title: Match it to an account
    summary: >-
      The domain is matched against your accounts. A match carries on with that record. No match creates
      a new account with the funding context attached, so the rep knows where it came from.
    builds: workflow
    description: >-
      Configure find-records step that matches the funding-event company_domain to an existing Account
      in the CRM. If match exists, proceed with that account (existing pipeline / customer / prospect).
      If no match, create a new Account record with the funding context attached so SDR/AE knows where
      this came from. Use the result of "Watch for funding news", "Accept the funding event".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Refresh who works there now
    summary: >-
      Funding usually brings new executives, more headcount and new plans, so the decision makers, team
      size and recent hires are pulled again. Whatever you had on file is now out of date.
    builds: workflow
    description: >-
      Re-enrich the account post-funding, funding rounds frequently coincide with new exec hires, expanded
      headcount, new initiatives. Pull latest decision-makers, team size, recent hires. Funding announcements
      often trigger immediate org changes; the account data on file is now stale. Use the result of "Watch
      for funding news", "Match it to an account".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Draft the congratulations
    summary: >-
      An email naming the round and what the investors suggest about their direction, a hypothesis about
      the problem companies at that stage hit, and a soft ask for a meeting. Saved on the AE task, never
      sent automatically.
    builds: workflow
    description: >-
      Configure AI write step that drafts a personalized outreach email/message referencing the specific
      funding event ('Congrats on the Series B, your investors include [name], which suggests focus on
      [inference about strategy]'), then connecting to a relevant value hypothesis ('Teams raising at
      this stage typically face X challenge (we help with that'), then a soft meeting CTA. Draft saved
      to the AE task; never auto-sent) funding events deserve human review before reaching out. Use the
      result of "Watch for funding news", "Refresh who works there now".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Put it on an AE within a day
    summary: >-
      Assigned by territory, account ownership, or round robin if nobody owns it, at high priority because
      funding signals fade within a fortnight. The task carries the funding details, the refreshed account,
      the drafted email and suggested times, on a 24 hour outreach target.
    builds: workflow
    description: >-
      Configure task creation: assign to the right AE (territory rules, account ownership, or round-robin
      if unassigned). Task priority: HIGH (funding signals decay fast: within 14 days is golden). Task
      body: structured brief with funding context, refreshed account data, AI-drafted outreach, suggested
      meeting times. SLA: AE outreach within 24 hours of funding announcement. Use the result of "Watch
      for funding news", "Refresh who works there now", "Draft the congratulations".
    dependsOn:
      - s1
      - s4
      - s5
  - id: s7
    title: Announce it to the team
    summary: >-
      A line in the sales signals channel naming the account, the amount, the round, the AE it went to
      and the 24 hour target, with links to the task and the account record.
    builds: workflow
    description: >-
      Configure Slack step posting to the #sales-signals channel: '🚀 [Account] raised [amount] [round].
      Assigned to [AE name]. Outreach SLA: 24hr.' Includes link to the task and account record. Surfaces
      the signal velocity for the team: funding events visible to everyone create healthy competitive
      urgency. Use the result of "Watch for funding news", "Put it on an AE within a day".
    dependsOn:
      - s1
      - s6
  - id: s8
    title: Publish and measure the lift
    summary: >-
      Validated and published, tracking how fast AEs respond, how many funding events become meetings,
      and how many become closed deals, set against cold outreach with no signal behind it.
    builds: workflow
    description: >-
      Validate and publish. Monitor: AE response SLA, funding-event-to-meeting-booked rate, funding-event-to-deal-closed
      rate. The benchmark to beat: 4-7x higher conversion vs. unsignaled cold outreach (per Landbase research).
      Use the result of "Watch for funding news", "Announce it to the team".
    dependsOn:
      - s1
      - s7
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s7
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Outreach on a funding round

Catches an account raising money, refreshes who works there now, drafts a congratulations with a budget angle, and asks the AE to act within a day.

## Steps

1. **Watch for funding news** (builds workflow)

   Triggered by a webhook from a signal provider, or by a scheduled scrape of funding news for your target domains. The aim is to be among the first to reach out while the budget is fresh.

2. **Accept the funding event** (builds workflow)

   The webhook takes the company domain, the round, the amount raised, the investors and the announcement date, and rejects anything malformed.

3. **Match it to an account** (builds workflow)

   The domain is matched against your accounts. A match carries on with that record. No match creates a new account with the funding context attached, so the rep knows where it came from.

4. **Refresh who works there now** (builds workflow)

   Funding usually brings new executives, more headcount and new plans, so the decision makers, team size and recent hires are pulled again. Whatever you had on file is now out of date.

5. **Draft the congratulations** (builds workflow)

   An email naming the round and what the investors suggest about their direction, a hypothesis about the problem companies at that stage hit, and a soft ask for a meeting. Saved on the AE task, never sent automatically.

6. **Put it on an AE within a day** (builds workflow)

   Assigned by territory, account ownership, or round robin if nobody owns it, at high priority because funding signals fade within a fortnight. The task carries the funding details, the refreshed account, the drafted email and suggested times, on a 24 hour outreach target.

7. **Announce it to the team** (builds workflow)

   A line in the sales signals channel naming the account, the amount, the round, the AE it went to and the 24 hour target, with links to the task and the account record.

8. **Publish and measure the lift** (builds workflow)

   Validated and published, tracking how fast AEs respond, how many funding events become meetings, and how many become closed deals, set against cold outreach with no signal behind it.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
