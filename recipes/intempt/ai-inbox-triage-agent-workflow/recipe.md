---
id: ai-inbox-triage-agent-workflow
title: AI inbox triage
slash_command: /ai-inbox-triage-agent-workflow
group: Workflows
owner: intempt
summary: Reads every inbound message, works out whether it is sales, support, billing, partnership or
  spam, and gets it to the right person inside five minutes.
description: >-
  Inbound conversations (email, chat, form) hit an AI triage agent that classifies intent (sales / support
  / billing / partnership / spam) and routes via multi-split to the right team + drafts an appropriate
  first response. Replaces the manual 'who handles this?' loop.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: workflow-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - ai-triage
    - inbox-routing
    - conversation-intelligence
prerequisites:
  integrations:
    - value: slack
      severity: recommended
  events:
    - value: conversation_received
      severity: blocking
steps:
  - id: s1
    title: Catch every inbound message
    summary: >-
      Runs when anything arrives on a tracked channel: email, web chat, a contact form or a social DM
      by webhook. Every message should reach the right human within five minutes with its context attached.
    builds: workflow
    description: >-
      Create a workflow 'AI inbox triage' triggered when a new inbound conversation arrives in any tracked
      channel (email, web chat, contact form, social DM via webhook). Goal: every message reaches the
      right human within 5 minutes with appropriate context attached, replacing the manual ops triage.
  - id: s2
    title: Work out what they want
    summary: >-
      Each message is classified as a sales enquiry, a support question, a billing question, a partnership
      approach, spam, or something needing escalation such as legal, security or abuse. It returns the
      label, a confidence score, and the products, competitors and urgency it picked out.
    builds: workflow
    description: >-
      Configure AI step that classifies the inbound message into one of: sales-inquiry (interested in
      buying), support-question (existing customer issue), billing-question (payment/account), partnership
      (BD/integration), spam/non-actionable, or escalation-required (legal threat, security, abuse). Output:
      intent_label + confidence + extracted entities (mentioned products, mentioned competitors, urgency
      signals). Use the result of "Catch every inbound message".
    dependsOn:
      - s1
  - id: s3
    title: Send it to the right team
    summary: >-
      Sales goes to an AE task and the sales inbox, support to the support queue against the customer,
      billing to finance, partnership to BD, spam is archived quietly, and an escalation pages whoever
      is on call. Each branch carries the full message.
    builds: workflow
    description: >-
      Configure multi-split routing into branches: sales-inquiry to AE task + sales-inbox; support-question
      to support queue (linked customer); billing-question to finance queue; partnership to BD task; spam
      to archive silently; escalation-required to on-call alert. Each branch gets the full message context
      attached. Use the result of "Catch every inbound message", "Work out what they want".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Match them to an account
    summary: >-
      On the sales branch, the sender's email or domain is matched to an existing account or lead so their
      history shows. If nothing matches, a lead is created and enrichment is triggered.
    builds: workflow
    description: >-
      On the sales-inquiry branch: try to match sender's email/domain to an existing Account or Lead.
      If match, surface their history (prior touches, opened deals, account tier). If no match, create
      lead with auto-enrichment trigger. Use the result of "Catch every inbound message", "Send it to
      the right team".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Draft the first reply
    summary: >-
      On the sales branch, a reply that acknowledges the enquiry, references any past dealings and offers
      a concrete next step: a demo, a specialist, or pricing. It waits on the AE task for review. The
      target is a first response inside five minutes.
    builds: workflow
    description: >-
      Configure AI write step on the sales branch: draft a personalized initial reply acknowledging the
      inquiry, referencing any past interactions if matched, offering specific next steps (book a demo
      / talk to specialist / send pricing). Saved as draft on the AE task; AE reviews, edits if needed,
      sends. Reply-SLA target: 5 minutes from inbound. Use the result of "Catch every inbound message",
      "Match them to an account".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Give the AE the whole picture
    summary: >-
      A task carrying the original message, the classification and its confidence, the matched account
      and the drafted reply. Assigned by territory or round robin, high priority for known accounts and
      medium for the rest.
    builds: workflow
    description: >-
      Create AE task with: original message, AI classification + confidence, matched account/lead context,
      AI-drafted reply ready-to-send. Assign by territory or round-robin. Priority: HIGH for known accounts,
      MEDIUM for unknown. SLA: 5-minute first response. Use the result of "Catch every inbound message",
      "Match them to an account", "Draft the first reply".
    dependsOn:
      - s1
      - s4
      - s5
  - id: s7
    title: Queue the support questions
    summary: >-
      Support gets the account tier, recent product usage and recent tickets. Paid plans are flagged as
      priority, free tier gets an FAQ first response.
    builds: workflow
    description: >-
      On the support-question branch: route to support queue with customer context (account tier, recent
      product usage, recent tickets). If customer is on a paid plan, flag as priority; if free-tier, route
      to FAQ-first response template. Use the result of "Catch every inbound message", "Send it to the
      right team".
    dependsOn:
      - s1
      - s3
  - id: s8
    title: Ask a human when unsure
    summary: >-
      If confidence is under 60%, or the message needs escalating, it goes to the ops triage channel with
      the AI's best guess so nothing falls through.
    builds: workflow
    description: >-
      Configure Slack step that fires when AI classification confidence is below 60% OR when the message
      is escalation-required type. Posts to #ops-triage channel with the message and AI's best guess at
      routing, asking for human review. Don't let edge cases fall through. Use the result of "Catch every
      inbound message", "Work out what they want".
    dependsOn:
      - s1
      - s2
  - id: s9
    title: Publish and audit the calls
    summary: >-
      Validated and published. Each week a human grades a 5% sample against a 90% accuracy target, alongside
      the first response time and how often messages go to the wrong team. The prompts get tuned when
      accuracy slips.
    builds: workflow
    description: >-
      Validate and publish. Monitor: classification accuracy (sample 5% of messages weekly, human-rates
      whether the AI got it right: target: 90%+), first-response SLA, mis-routed-message rate. Tune the
      AI prompts when accuracy dips. Use the result of "Catch every inbound message", "Give the AE the
      whole picture", "Queue the support questions", "Ask a human when unsure".
    dependsOn:
      - s1
      - s6
      - s7
      - s8
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s8
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# AI inbox triage

Reads every inbound message, works out whether it is sales, support, billing, partnership or spam, and gets it to the right person inside five minutes.

## Steps

1. **Catch every inbound message** (builds workflow)

   Runs when anything arrives on a tracked channel: email, web chat, a contact form or a social DM by webhook. Every message should reach the right human within five minutes with its context attached.

2. **Work out what they want** (builds workflow)

   Each message is classified as a sales enquiry, a support question, a billing question, a partnership approach, spam, or something needing escalation such as legal, security or abuse. It returns the label, a confidence score, and the products, competitors and urgency it picked out.

3. **Send it to the right team** (builds workflow)

   Sales goes to an AE task and the sales inbox, support to the support queue against the customer, billing to finance, partnership to BD, spam is archived quietly, and an escalation pages whoever is on call. Each branch carries the full message.

4. **Match them to an account** (builds workflow)

   On the sales branch, the sender's email or domain is matched to an existing account or lead so their history shows. If nothing matches, a lead is created and enrichment is triggered.

5. **Draft the first reply** (builds workflow)

   On the sales branch, a reply that acknowledges the enquiry, references any past dealings and offers a concrete next step: a demo, a specialist, or pricing. It waits on the AE task for review. The target is a first response inside five minutes.

6. **Give the AE the whole picture** (builds workflow)

   A task carrying the original message, the classification and its confidence, the matched account and the drafted reply. Assigned by territory or round robin, high priority for known accounts and medium for the rest.

7. **Queue the support questions** (builds workflow)

   Support gets the account tier, recent product usage and recent tickets. Paid plans are flagged as priority, free tier gets an FAQ first response.

8. **Ask a human when unsure** (builds workflow)

   If confidence is under 60%, or the message needs escalating, it goes to the ops triage channel with the AI's best guess so nothing falls through.

9. **Publish and audit the calls** (builds workflow)

   Validated and published. Each week a human grades a 5% sample against a 90% accuracy target, alongside the first response time and how often messages go to the wrong team. The prompts get tuned when accuracy slips.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## Availability

Coming soon: waiting on the engine to build workflow.
