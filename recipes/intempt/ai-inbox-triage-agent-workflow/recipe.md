---
description: Classifies inbound messages received through a webhook by intent, such as sales, support, billing, partnership, or spam. Routes each message to the appropriate team and can create a follow-up task.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - finance
---

# AI inbox triage

Slash command: /ai-inbox-triage-agent-workflow

## Step 1: Catch every inbound message

Create a workflow 'AI inbox triage' triggered when a new inbound conversation arrives in any tracked channel (email, web chat, contact form, social DM via webhook). Goal: every message reaches the right human within 5 minutes with appropriate context attached, replacing the manual ops triage.

## Step 2: Work out what they want

This step builds a workflow.
Configure AI step that classifies the inbound message into one of: sales-inquiry (interested in buying), support-question (existing customer issue), billing-question (payment/account), partnership (BD/integration), spam/non-actionable, or escalation-required (legal threat, security, abuse). Output: intent_label + confidence + extracted entities (mentioned products, mentioned competitors, urgency signals). Use the result of "Catch every inbound message".

## Step 3: Send it to the right team

This step builds a workflow.
Configure multi-split routing into branches: sales-inquiry to AE task + sales-inbox; support-question to support queue (linked customer); billing-question to finance queue; partnership to BD task; spam to archive silently; escalation-required to on-call alert. Each branch gets the full message context attached. Use the result of "Catch every inbound message", "Work out what they want".

## Step 4: Match them to an account

This step builds a workflow.
On the sales-inquiry branch: try to match sender's email/domain to an existing Account or Lead. If match, surface their history (prior touches, opened deals, account tier). If no match, create lead with auto-enrichment trigger. Use the result of "Catch every inbound message", "Send it to the right team".

## Step 5: Draft the first reply

This step builds a workflow.
Configure AI write step on the sales branch: draft a personalized initial reply acknowledging the inquiry, referencing any past interactions if matched, offering specific next steps (book a demo / talk to specialist / send pricing). Saved as draft on the AE task; AE reviews, edits if needed, sends. Reply-SLA target: 5 minutes from inbound. Use the result of "Catch every inbound message", "Match them to an account".

## Step 6: Give the AE the whole picture

This step builds a workflow.
Create AE task with: original message, AI classification + confidence, matched account/lead context, AI-drafted reply ready-to-send. Assign by territory or round-robin. Priority: HIGH for known accounts, MEDIUM for unknown. SLA: 5-minute first response. Use the result of "Catch every inbound message", "Match them to an account", "Draft the first reply".

## Step 7: Queue the support questions

This step builds a workflow.
On the support-question branch: route to support queue with customer context (account tier, recent product usage, recent tickets). If customer is on a paid plan, flag as priority; if free-tier, route to FAQ-first response template. Use the result of "Catch every inbound message", "Send it to the right team".

## Step 8: Ask a human when unsure

This step builds a workflow.
Configure Slack step that fires when AI classification confidence is below 60% OR when the message is escalation-required type. Posts to #ops-triage channel with the message and AI's best guess at routing, asking for human review. Don't let edge cases fall through. Use the result of "Catch every inbound message", "Work out what they want".

## Step 9: Publish and audit the calls

This step builds a workflow.
Validate and publish. Monitor: classification accuracy (sample 5% of messages weekly, human-rates whether the AI got it right: target: 90%+), first-response SLA, mis-routed-message rate. Tune the AI prompts when accuracy dips. Use the result of "Catch every inbound message", "Give the AE the whole picture", "Queue the support questions", "Ask a human when unsure".
