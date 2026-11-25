---
frontmatter_id: ai-inbox-triage-agent-workflow
slash_command: /ai-inbox-triage-agent-workflow
description: Classifies each inbound message by intent (sales, support, billing, partnership, spam or escalation) and emails
  it with context and a suggested reply to the right team, sending unclear ones to a human.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Classifies every inbound message by intent and emails it to the right team with context and a suggested first reply.
  parameters:
  - name: confidence_threshold
    type: number
    label: Classification confidence (%) below which a human reviews
    default: 60
    required: false
  - name: sales_recipients
    type: string
    label: Email addresses of the sales team
    required: true
  - name: support_recipients
    type: string
    label: Email addresses of the support team
    required: true
  - name: billing_recipients
    type: string
    label: Email addresses of the billing team
    required: true
  - name: partnership_recipients
    type: string
    label: Email addresses of the partnerships team
    required: true
  - name: review_recipients
    type: string
    label: Email addresses of the people who review unclear or escalated messages
    required: true
  requirements:
  - slot: inbound_message_event
    kind: event
    meaning: A customer or prospect sent an inbound message through email, web chat or a contact form
    properties:
    - name: message_body
      type: string
      meaning: Text of the message
      optional: false
    - name: sender_email
      type: string
      meaning: Email address of the sender
      optional: false
    - name: channel_source
      type: string
      meaning: Where the message came in, such as email, chat or form
      optional: true
  - slot: customer_plan_tier
    kind: attribute
    meaning: The sender's plan, empty or free when they are not paying
  steps:
  - id: s1
    builds: automation
    uses:
    - inbound_message_event
    - customer_plan_tier
    - confidence_threshold
    - sales_recipients
    - support_recipients
    - billing_recipients
    - partnership_recipients
    - review_recipients
    instruction: 'Build an automation that starts when a user does {inbound_message_event}. It analyzes {inbound_message_event.message_body}
      and classifies it as exactly one of sales, support, billing, partnership, spam or escalation (legal, security or abuse),
      with a confidence from 0 to 100, and writes a short suggested first reply. Then it emails one plain-text note with the
      message, {inbound_message_event.sender_email}, {inbound_message_event.channel_source}, the user''s {customer_plan_tier},
      the class, the confidence and the suggested reply: sales to {sales_recipients}, support to {support_recipients}, billing
      to {billing_recipients}, partnership to {partnership_recipients}. Escalation, or any confidence below {confidence_threshold},
      goes to {review_recipients} instead. Spam is not sent. Nothing is sent to the sender.'
---

# AI inbox triage

Slash command: /ai-inbox-triage-agent-workflow

## Step 1: Triage every inbound message

Build an automation that starts when a user does inbound message event. It analyzes message body and classifies it as exactly one of sales, support, billing, partnership, spam or escalation (legal, security or abuse), with a confidence from 0 to 100, and writes a short suggested first reply. Then it emails one plain-text note with the message, sender email, channel source, the user's customer plan tier, the class, the confidence and the suggested reply: sales to the email addresses of the sales team, support to the email addresses of the support team, billing to the email addresses of the billing team, partnership to the email addresses of the partnerships team. Escalation, or any confidence below 60, goes to the email addresses of the people who review unclear or escalated messages instead. Spam is not sent. Nothing is sent to the sender.
