---
description: Catches an account raising money, refreshes who works there now, drafts a congratulations with a budget angle, and asks the AE to act within a day.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - b2b-saas
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
