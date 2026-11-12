---
frontmatter_id: funding-event-triggered-outreach
slash_command: /funding-event-triggered-outreach
description: Catches an account raising money, refreshes who works there now, drafts a congratulations with a budget angle, and asks the AE to act within a day.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Catches an account's funding round, refreshes its contacts, drafts a human-reviewed congratulations email, assigns
    it to an AE within a day, and posts it to the sales team.
  parameters:
  - name: sla_hours
    type: number
    label: AE outreach SLA (hours after funding announcement)
    default: 24
    required: false
  - name: task_priority
    type: enum
    label: Task priority
    default: high
    required: false
    options:
    - high
    - medium
    - low
  - name: signal_window
    type: duration
    label: Window in which funding signal is most valuable
    default: 14 d
    required: false
  - name: announce_channel
    type: string
    label: Team Slack channel for announcements
    default: '#sales-signals'
    required: false
  requirements:
  - slot: funding_signal_source
    kind: integration
    meaning: A funding-news signal provider (such as Crunchbase, PitchBook, or RSS news feed) that can send funding events
      by webhook or scheduled scrape
    channel: hubspot
  - slot: funding_event
    kind: event
    meaning: A target account announced a funding round
    properties:
    - name: company_domain
      type: string
      meaning: Web domain of the company that raised funds
      optional: false
    - name: round_type
      type: string
      meaning: Funding round stage such as seed, A, B, or C
      optional: false
    - name: amount_raised
      type: string
      meaning: Amount of money raised in the round
      optional: false
    - name: investors
      type: text
      meaning: Names of investors in the round
      optional: true
    - name: announcement_date
      type: date
      meaning: Date the round was announced
      optional: false
  - slot: account
    kind: attribute
    meaning: A company account record in the CRM matched by web domain
  - slot: account_owner
    kind: attribute
    meaning: The AE who owns the account or territory assignment rules for unassigned accounts
  - slot: sales_team_channel
    kind: destination
    meaning: A Slack channel where the sales team receives funding announcements
    channel: slack
  - slot: enrichment_source
    kind: integration
    meaning: A data provider that returns current decision-makers, headcount, and recent hires for an account
    channel: email
  steps:
  - id: s1
    builds: automation
    uses:
    - funding_signal_source
    - funding_event
    instruction: 'Create a workflow ''Funding-event-triggered outreach'' triggered either by a webhook from {funding_signal_source}
      or by a scheduled scrape of funding news for target-account domains. Goal: reach out soon after funding while budget
      is fresh.'
  - id: s2
    builds: automation
    uses:
    - s1
    - funding_event
    instruction: Configure a webhook trigger to receive funding-event payloads with {funding_event.company_domain}, {funding_event.round_type},
      {funding_event.amount_raised}, {funding_event.investors}, and {funding_event.announcement_date}. Validate the payload
      schema and reject malformed events. Use the result of "Funding-event-triggered outreach".
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - account
    - funding_event
    instruction: Find the {account} whose domain matches {funding_event.company_domain}. If a match exists, proceed with that
      account. If no match exists, create a new {account} record with the funding context attached so the account owner knows
      the source. Use the results of "Funding-event-triggered outreach" and "Accept the funding event".
  - id: s4
    builds: automation
    uses:
    - enrichment_source
    - s1
    - s3
    instruction: Re-enrich the account via {enrichment_source} after funding. Pull current decision-makers, team size, and
      recent hires, since the stored account data is likely stale. Use the results of "Funding-event-triggered outreach" and
      "Match it to an account".
  - id: s5
    builds: email
    uses:
    - funding_event
    - s1
    - s4
    instruction: Draft a personalized outreach email that references {funding_event.round_type} and {funding_event.amount_raised}
      from {funding_event.announcement_date}, names {funding_event.investors} where present, and infers likely strategic focus
      from them. Connect it to a relevant value hypothesis for teams raising at this stage, then close with a soft meeting
      request. Save the draft to the AE task only; never send automatically. Use the results of "Funding-event-triggered outreach"
      and "Refresh who works there now".
  - id: s6
    builds: task
    uses:
    - account_owner
    - task_priority
    - signal_window
    - sla_hours
    - s1
    - s4
    - s5
    instruction: 'Assign a task to the correct {account_owner} using territory rules, account ownership, or round-robin if
      unassigned. Set priority to {task_priority} because funding signals decay within {signal_window}. Task body: funding
      context, refreshed account data, the AI-drafted outreach from "Draft the congratulations", and suggested meeting times.
      Require AE outreach within {sla_hours} hours of the funding announcement. Use the results of "Funding-event-triggered
      outreach", "Refresh who works there now", and "Draft the congratulations".'
  - id: s7
    builds: automation
    uses:
    - sales_team_channel
    - funding_event
    - sla_hours
    - s1
    - s6
    instruction: 'Post to {sales_team_channel} ({announce_channel}): ''Account raised {funding_event.amount_raised} {funding_event.round_type}.
      Assigned to [assigned AE]. Outreach SLA: {sla_hours}hr.'' Include links to the task and the account record. Use the
      results of "Funding-event-triggered outreach" and "Put it on an AE within a day".'
  - id: s8
    builds: report
    uses:
    - sla_hours
    - s1
    - s7
    instruction: 'Validate and publish the workflow. Monitor AE response time against {sla_hours} hours, funding-event-to-meeting-booked
      rate, and funding-event-to-deal-closed rate. Benchmark: the target is a 4-7x higher conversion versus unsignaled cold
      outreach. Use the results of "Funding-event-triggered outreach" and "Announce it to the team".'
---

# Outreach on a funding round

Slash command: /funding-event-triggered-outreach

## Step 1: Watch for funding news

Create a workflow 'Funding-event-triggered outreach' triggered by webhook from a signal provider (Crunchbase, PitchBook, or scraped TechCrunch RSS) OR by a scheduled scrape of funding news for target-account domains. Goal: be among the first to reach out post-funding when budget is fresh and growth-investment mood is high.

## Step 2: Accept the funding event

This step builds a workflow.
Configure the webhook trigger to receive funding-event payloads from external sources. Expected payload: company_domain, round_type (seed/A/B/C/etc), amount_raised, investors, announcement_date. Validate payload schema; reject malformed events. Use the result of "Watch for funding news".

## Step 3: Match it to an account

This step builds a workflow.
Configure find-records step that matches the funding-event company_domain to an existing Account in the CRM. If match exists, proceed with that account (existing pipeline / customer / prospect). If no match, create a new Account record with the funding context attached so SDR/AE knows where this came from. Use the result of "Watch for funding news", "Accept the funding event".

## Step 4: Refresh who works there now

This step builds a workflow.
Re-enrich the account post-funding, funding rounds frequently coincide with new exec hires, expanded headcount, new initiatives. Pull latest decision-makers, team size, recent hires. Funding announcements often trigger immediate org changes; the account data on file is now stale. Use the result of "Watch for funding news", "Match it to an account".

## Step 5: Draft the congratulations

This step builds a workflow.
Configure AI write step that drafts a personalized outreach email/message referencing the specific funding event ('Congrats on the Series B, your investors include [name], which suggests focus on [inference about strategy]'), then connecting to a relevant value hypothesis ('Teams raising at this stage typically face X challenge (we help with that'), then a soft meeting CTA. Draft saved to the AE task; never auto-sent) funding events deserve human review before reaching out. Use the result of "Watch for funding news", "Refresh who works there now".

## Step 6: Put it on an AE within a day

This step builds a workflow.
Configure task creation: assign to the right AE (territory rules, account ownership, or round-robin if unassigned). Task priority: HIGH (funding signals decay fast: within 14 days is golden). Task body: structured brief with funding context, refreshed account data, AI-drafted outreach, suggested meeting times. SLA: AE outreach within 24 hours of funding announcement. Use the result of "Watch for funding news", "Refresh who works there now", "Draft the congratulations".

## Step 7: Announce it to the team

This step builds a workflow.
Configure Slack step posting to the #sales-signals channel: '🚀 [Account] raised [amount] [round]. Assigned to [AE name]. Outreach SLA: 24hr.' Includes link to the task and account record. Surfaces the signal velocity for the team: funding events visible to everyone create healthy competitive urgency. Use the result of "Watch for funding news", "Put it on an AE within a day".

## Step 8: Publish and measure the lift

This step builds a workflow.
Validate and publish. Monitor: AE response SLA, funding-event-to-meeting-booked rate, funding-event-to-deal-closed rate. The benchmark to beat: 4-7x higher conversion vs. unsignaled cold outreach (per Landbase research). Use the result of "Watch for funding news", "Announce it to the team".
