---
frontmatter_id: ai-inbox-triage-agent-workflow
slash_command: /ai-inbox-triage-agent-workflow
description: Classifies inbound messages received through a webhook by intent, such as sales, support, billing, partnership, or spam. Routes each message to the appropriate team and can create a follow-up task.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Automatically classifies each inbound message by intent, routes it to sales, support, billing, partnership, or
    escalation teams, and alerts a human when unsure.
  parameters:
  - name: confidence_threshold
    type: number
    label: Minimum classification confidence (%) before human review
    default: 60
    required: false
  - name: sla_minutes
    type: number
    label: First-response SLA (minutes)
    default: 5
    required: false
  - name: sample_rate_percent
    type: number
    label: Weekly audit sample rate (%)
    default: 5
    required: false
  - name: accuracy_target_percent
    type: number
    label: Classification accuracy target (%)
    default: 90
    required: false
  - name: ops_slack_channel
    type: string
    label: Slack channel for human review
    default: '#ops-triage'
    required: false
  requirements:
  - slot: inbound_message_event
    kind: event
    meaning: A customer or prospect sent an inbound message through email, web chat, contact form, or social DM
    properties:
    - name: message_body
      type: text
      meaning: Text of the inbound message
      optional: false
    - name: sender_email
      type: string
      meaning: Sender email address
      optional: true
    - name: channel_source
      type: string
      meaning: Channel the message arrived through
      optional: false
  - slot: sales_inbox
    kind: integration
    meaning: A shared sales inbox or team destination where sales-inquiry messages are posted
    channel: email
  - slot: ae_task_queue
    kind: integration
    meaning: A CRM task system where AE follow-up tasks can be created and assigned by territory or round-robin
    channel: salesforce
  - slot: support_queue
    kind: destination
    meaning: Support ticket queue that accepts customer context
    channel: email
  - slot: finance_queue
    kind: destination
    meaning: Finance or billing queue for payment and account questions
    channel: email
  - slot: bd_task_queue
    kind: integration
    meaning: A task system where business development follow-ups are created
    channel: salesforce
  - slot: ops_slack
    kind: integration
    meaning: A Slack workspace with the ops triage channel for human review
    channel: slack
  - slot: account_records
    kind: attribute
    meaning: Customer account and lead records matched by sender email or domain, with tier and deal history
  - slot: customer_plan_tier
    kind: attribute
    meaning: The paid or free plan tier of a matched customer
  steps:
  - id: s1
    builds: workflow
    uses:
    - inbound_message_event
    - sla_minutes
    instruction: 'Create a workflow named ''AI inbox triage'' triggered when a new inbound message event arrives from any
      tracked channel (email, web chat, contact form, social DM via webhook). Goal: every message reaches the right human
      within {sla_minutes} minutes with context attached.'
  - id: s2
    builds: workflow
    uses:
    - s1
    instruction: 'Configure an AI classification step on the inbound message from ''Catch every inbound message''. Classify
      into one of: sales-inquiry (interested in buying), support-question (existing customer issue), billing-question (payment
      or account), partnership (business development or integration), spam or non-actionable, or escalation-required (legal
      threat, security, abuse). Output intent label, confidence, and extracted entities: mentioned products, mentioned competitors,
      urgency signals.'
  - id: s3
    builds: workflow
    uses:
    - s1
    - s2
    - sales_inbox
    - support_queue
    - finance_queue
    - bd_task_queue
    instruction: 'Configure a multi-split router on the result of ''Work out what they want''. Branches: sales-inquiry to
      AE task and {sales_inbox}; support-question to {support_queue} linked to the customer; billing-question to {finance_queue};
      partnership to {bd_task_queue} task; spam to archive silently; escalation-required to on-call alert. Attach the full
      message context to each branch.'
  - id: s4
    builds: workflow
    uses:
    - s1
    - s3
    - account_records
    instruction: On the sales-inquiry branch of 'Send it to the right team', match the sender's email or domain to an existing
      {account_records}. If matched, surface prior touches, opened deals, and account tier. If not matched, create a lead
      with an auto-enrichment trigger.
  - id: s5
    builds: email
    uses:
    - s1
    - s4
    instruction: 'On the sales branch, draft a personalized initial reply that acknowledges the inquiry, references past interactions
      if matched in ''Match them to an account'', and offers specific next steps: book a demo, talk to a specialist, or send
      pricing. Save as a draft on the AE task for review. Target first reply within {sla_minutes} minutes of the inbound message.
      Tone: professional.'
  - id: s6
    builds: task
    uses:
    - s1
    - s2
    - s4
    - s5
    - ae_task_queue
    - sla_minutes
    instruction: Create an AE task containing the original message, the AI classification and confidence from 'Work out what
      they want', the matched account or lead context from 'Match them to an account', and the AI-drafted reply from 'Draft
      the first reply'. Assign by territory or round-robin on {ae_task_queue}. Set priority HIGH for known accounts and MEDIUM
      for unknown senders. Set a {sla_minutes}-minute first-response SLA.
  - id: s7
    builds: task
    uses:
    - s1
    - s3
    - support_queue
    - customer_plan_tier
    instruction: 'On the support-question branch of ''Send it to the right team'', route to {support_queue} with customer
      context: account tier, recent product usage, and recent tickets. If the customer is on a paid plan ({customer_plan_tier}),
      flag as priority. If on the free tier, route to an FAQ-first response template.'
  - id: s8
    builds: workflow
    uses:
    - s1
    - s2
    - ops_slack
    - confidence_threshold
    - ops_slack_channel
    instruction: Configure a Slack alert that fires when the AI classification confidence is below {confidence_threshold}
      percent OR the intent is escalation-required. Post the message and the AI's best routing guess to {ops_slack_channel}
      and ask for human review. Do not let edge cases fall through.
  - id: s9
    builds: workflow
    uses:
    - s1
    - s6
    - s7
    - s8
    - sample_rate_percent
    - accuracy_target_percent
    - sla_minutes
    instruction: Validate and publish the workflow. Monitor classification accuracy by sampling {sample_rate_percent} percent
      of messages weekly for human rating against the {accuracy_target_percent} percent target, first-response SLA against
      {sla_minutes} minutes, and mis-routed-message rate. Tune the AI classification prompts when accuracy dips.
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
