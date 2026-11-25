---
frontmatter_id: ai-draft-sales-reply
slash_command: /ai-draft-sales-reply
description: Drafts a reply to each incoming sales email using the deal stage, recent meeting notes and recent product activity,
  and emails the draft to the rep to review and send.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Drafts a reply to every incoming sales email from the deal and product context and emails it to the rep for review.
  parameters:
  - name: lookback_window
    type: duration
    label: Window of product activity used as context
    default: 14 d
    required: false
  - name: rep_recipients
    type: string
    label: Email addresses of the reps who get reply drafts
    required: true
  requirements:
  - slot: sales_email_received
    kind: event
    meaning: A contact sent an email to the sales inbox or into an active-deal email thread
    properties:
    - name: thread_subject
      type: string
      meaning: Subject of the email thread
      optional: false
    - name: message_body
      type: string
      meaning: Text of the incoming email
      optional: false
  - slot: product_activity
    kind: event
    meaning: A contact used or viewed the product
    properties:
    - name: activity_type
      type: string
      meaning: What the contact did
      optional: true
  - slot: deal_stage
    kind: attribute
    meaning: User attribute with the current pipeline stage of the contact's deal
  - slot: meeting_summary
    kind: attribute
    meaning: User attribute with the summary of the latest sales meeting with the contact
    optional: true
  steps:
  - id: s1
    builds: automation
    uses:
    - sales_email_received
    - product_activity
    - deal_stage
    - meeting_summary
    - lookback_window
    - rep_recipients
    instruction: Build an automation that starts when a user does {sales_email_received}. It analyzes {sales_email_received.message_body},
      classifies it as one of question, objection, scheduling request, agreement, acknowledgment or out of office, and writes
      a short reply draft that answers it using the user's {deal_stage}, their {meeting_summary}, and their {product_activity}
      events with {product_activity.activity_type} in the last {lookback_window}. Out-of-office emails get no draft. Then
      it emails {rep_recipients} a plain-text note with the contact's name and email, {sales_email_received.thread_subject},
      the classification and the reply draft, for the rep to review and send. Nothing is sent to the contact.
---

# AI drafted sales replies

Slash command: /ai-draft-sales-reply

## Step 1: Draft it into the rep's outbox

Build an automation that starts when a user does sales email received. It analyzes message body, classifies it as one of question, objection, scheduling request, agreement, acknowledgment or out of office, and writes a short reply draft that answers it using the user's deal stage, their meeting summary, and their product activity events with activity type in the last 14 d. Out-of-office emails get no draft. Then it emails the email addresses of the reps who get reply drafts a plain-text note with the contact's name and email, thread subject, the classification and the reply draft, for the rep to review and send. Nothing is sent to the contact.
