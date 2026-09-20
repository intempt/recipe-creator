---
name: ai-inbox-triage-agent-workflow
description: Use when a user mentions "AI inbox triage agent", "inbound conversation routing", "AI classify and route messages", or asks for related help. Inbound conversations (email, chat, form) hit an AI triage agent that classifies intent (sales / support / billing / partnership / spam) and routes via multi-split to the right team + drafts an appropriate first response. Replaces the manual 'who handles this?' loop.
arguments: []
intempt:
  id: ai-inbox-triage-agent-workflow
  title: "AI inbox triage"
  version: 1.0.0
  slashCommand: /ai-inbox-triage-agent-workflow
  group: Workflows
  shortDescription: "Reads every inbound message, works out whether it is sales, support, billing, partnership or spam, and gets it to the right person inside five minutes."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: workflow-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [ai-triage, inbox-routing, conversation-intelligence]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
    events:
      - { value: conversation_received, severity: blocking }
  invokesCommands:
    - create_workflow
    - configure_ai_research_step
    - configure_workflow_multi_split_step
    - configure_find_records_step
    - configure_write_with_ai_step
    - configure_create_task_step
    - configure_slack_step
    - publish_workflow
  procedure:
    - step: 1
      title: "Catch every inbound message"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Runs when anything arrives on a tracked channel: email, web chat, a contact form or a social DM by webhook. Every message should reach the right human within five minutes with its context attached."
      prompt: 'Create a workflow ''AI inbox triage'' triggered when a new inbound conversation arrives in any tracked channel (email, web chat, contact form, social DM via webhook). Goal: every message reaches the right human within 5 minutes with appropriate context attached, replacing the manual ops triage.'
    - step: 2
      title: "Work out what they want"
      command: configure_ai_research_step
      produces: step
      bindsAs: classify
      dependsOn:
      - workflow
      description: "Each message is classified as a sales enquiry, a support question, a billing question, a partnership approach, spam, or something needing escalation such as legal, security or abuse. It returns the label, a confidence score, and the products, competitors and urgency it picked out."
      prompt: 'Configure AI step that classifies the inbound message into one of: sales-inquiry (interested in buying), support-question (existing customer issue), billing-question (payment/account), partnership (BD/integration), spam/non-actionable, or escalation-required (legal threat, security, abuse). Output: intent_label + confidence + extracted entities (mentioned products, mentioned competitors, urgency signals).'
    - step: 3
      title: "Send it to the right team"
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: route
      dependsOn:
      - workflow
      - classify
      description: "Sales goes to an AE task and the sales inbox, support to the support queue against the customer, billing to finance, partnership to BD, spam is archived quietly, and an escalation pages whoever is on call. Each branch carries the full message."
      prompt: 'Configure multi-split routing into branches: sales-inquiry to AE task + sales-inbox; support-question to support queue (linked customer); billing-question to finance queue; partnership to BD task; spam to archive silently; escalation-required to on-call alert. Each branch gets the full message context attached.'
    - step: 4
      title: "Match them to an account"
      command: configure_find_records_step
      produces: step
      bindsAs: match_sender
      dependsOn:
      - workflow
      - route
      description: "On the sales branch, the sender's email or domain is matched to an existing account or lead so their history shows. If nothing matches, a lead is created and enrichment is triggered."
      prompt: 'On the sales-inquiry branch: try to match sender''s email/domain to an existing Account or Lead. If match, surface their history (prior touches, opened deals, account tier). If no match, create lead with auto-enrichment trigger.'
    - step: 5
      title: "Draft the first reply"
      command: configure_write_with_ai_step
      produces: step
      bindsAs: draft_reply
      dependsOn:
      - workflow
      - match_sender
      description: "On the sales branch, a reply that acknowledges the enquiry, references any past dealings and offers a concrete next step: a demo, a specialist, or pricing. It waits on the AE task for review. The target is a first response inside five minutes."
      prompt: 'Configure AI write step on the sales branch: draft a personalized initial reply acknowledging the inquiry, referencing any past interactions if matched, offering specific next steps (book a demo / talk to specialist / send pricing). Saved as draft on the AE task; AE reviews, edits if needed, sends. Reply-SLA target: 5 minutes from inbound.'
    - step: 6
      title: "Give the AE the whole picture"
      command: configure_create_task_step
      produces: step
      bindsAs: ae_task
      dependsOn:
      - workflow
      - match_sender
      - draft_reply
      description: "A task carrying the original message, the classification and its confidence, the matched account and the drafted reply. Assigned by territory or round robin, high priority for known accounts and medium for the rest."
      prompt: 'Create AE task with: original message, AI classification + confidence, matched account/lead context, AI-drafted reply ready-to-send. Assign by territory or round-robin. Priority: HIGH for known accounts, MEDIUM for unknown. SLA: 5-minute first response.'
    - step: 7
      title: "Queue the support questions"
      command: configure_create_task_step
      produces: step
      bindsAs: support_task
      dependsOn:
      - workflow
      - route
      description: "Support gets the account tier, recent product usage and recent tickets. Paid plans are flagged as priority, free tier gets an FAQ first response."
      prompt: 'On the support-question branch: route to support queue with customer context (account tier, recent product usage, recent tickets). If customer is on a paid plan, flag as priority; if free-tier, route to FAQ-first response template.'
    - step: 8
      title: "Ask a human when unsure"
      command: configure_slack_step
      produces: step
      bindsAs: slack
      dependsOn:
      - workflow
      - classify
      description: "If confidence is under 60%, or the message needs escalating, it goes to the ops triage channel with the AI's best guess so nothing falls through."
      prompt: 'Configure Slack step that fires when AI classification confidence is below 60% OR when the message is escalation-required type. Posts to #ops-triage channel with the message and AI''s best guess at routing, asking for human review. Don''t let edge cases fall through.'
    - step: 9
      title: "Publish and audit the calls"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - ae_task
      - support_task
      - slack
      description: "Validated and published. Each week a human grades a 5% sample against a 90% accuracy target, alongside the first response time and how often messages go to the wrong team. The prompts get tuned when accuracy slips."
      prompt: 'Validate and publish. Monitor: classification accuracy (sample 5% of messages weekly, human-rates whether the AI got it right: target: 90%+), first-response SLA, mis-routed-message rate. Tune the AI prompts when accuracy dips.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# AI inbox triage

Reads every inbound message, works out whether it is sales, support, billing, partnership or spam, and gets it to the right person inside five minutes.

## Before you run it

- Connect slack
- Send the `conversation_received` event

## What it does

1. **Catch every inbound message** (`create_workflow`)

   Runs when anything arrives on a tracked channel: email, web chat, a contact form or a social DM by webhook. Every message should reach the right human within five minutes with its context attached.

2. **Work out what they want** (`configure_ai_research_step`)

   Each message is classified as a sales enquiry, a support question, a billing question, a partnership approach, spam, or something needing escalation such as legal, security or abuse. It returns the label, a confidence score, and the products, competitors and urgency it picked out.

3. **Send it to the right team** (`configure_workflow_multi_split_step`)

   Sales goes to an AE task and the sales inbox, support to the support queue against the customer, billing to finance, partnership to BD, spam is archived quietly, and an escalation pages whoever is on call. Each branch carries the full message.

4. **Match them to an account** (`configure_find_records_step`)

   On the sales branch, the sender's email or domain is matched to an existing account or lead so their history shows. If nothing matches, a lead is created and enrichment is triggered.

5. **Draft the first reply** (`configure_write_with_ai_step`)

   On the sales branch, a reply that acknowledges the enquiry, references any past dealings and offers a concrete next step: a demo, a specialist, or pricing. It waits on the AE task for review. The target is a first response inside five minutes.

6. **Give the AE the whole picture** (`configure_create_task_step`)

   A task carrying the original message, the classification and its confidence, the matched account and the drafted reply. Assigned by territory or round robin, high priority for known accounts and medium for the rest.

7. **Queue the support questions** (`configure_create_task_step`)

   Support gets the account tier, recent product usage and recent tickets. Paid plans are flagged as priority, free tier gets an FAQ first response.

8. **Ask a human when unsure** (`configure_slack_step`)

   If confidence is under 60%, or the message needs escalating, it goes to the ops triage channel with the AI's best guess so nothing falls through.

9. **Publish and audit the calls** (`publish_workflow`)

   Validated and published. Each week a human grades a 5% sample against a 90% accuracy target, alongside the first response time and how often messages go to the wrong team. The prompts get tuned when accuracy slips.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
