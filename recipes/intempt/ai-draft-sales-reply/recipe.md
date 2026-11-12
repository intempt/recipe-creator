---
frontmatter_id: ai-draft-sales-reply
slash_command: /ai-draft-sales-reply
description: Drafts a Gmail reply for a sales email thread using the thread, deal stage, and recent product activity, leaving it in the rep's drafts for review and send.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Drafts a Gmail reply to each sales email using thread history, deal stage and recent product activity, saving it
    to the rep's drafts for review, with a dashboard tracking draft quality.
  parameters:
  - name: lookback_window
    type: duration
    label: Product activity lookback window
    default: 14 d
    required: false
  - name: prior_exchanges
    type: number
    label: Number of prior thread exchanges to include
    default: 3
    required: false
  - name: sent_sample_size
    type: number
    label: Number of rep's recent sent emails used to learn tone
    default: 50
    required: false
  - name: discard_alert_threshold
    type: number
    label: Discard rate (%) above which the draft model should be retrained
    default: 30
    required: false
  - name: dashboard_report_period
    type: duration
    label: Dashboard reporting period per week bucket
    default: 7 d
    required: false
  requirements:
  - slot: sales_email_received
    kind: event
    meaning: A contact sent an email to the sales inbox or into an active-deal email thread
    properties:
    - name: thread_subject
      type: string
      meaning: Subject of the email thread
      optional: false
    - name: sender_contact
      type: string
      meaning: Contact who sent the email
      optional: false
  - slot: active_deal_thread
    kind: segment
    meaning: Email threads linked to a deal that is in an active stage
  - slot: product_activity
    kind: event
    meaning: A contact used or viewed a product
    properties:
    - name: activity_type
      type: string
      meaning: Kind of product activity performed
      optional: true
  - slot: meeting_summary
    kind: attribute
    meaning: Summary text of a recent sales meeting linked to a deal
    optional: true
  - slot: deal_stage
    kind: attribute
    meaning: Current pipeline stage of the linked deal
  - slot: open_deal_task
    kind: attribute
    meaning: Open tasks on the linked deal
    optional: true
  - slot: rep_sent_emails
    kind: attribute
    meaning: Emails the sales rep has sent, used to learn their writing tone
  - slot: rep_gmail_drafts
    kind: integration
    meaning: Connected Gmail account where drafts are saved for the rep
    channel: email
  - slot: rep_slack
    kind: integration
    meaning: Connected Slack workspace for sending the rep a direct message
    channel: slack
  - slot: rep_review_task
    kind: destination
    meaning: Task list where the rep receives review tasks for AI drafts
    optional: true
    channel: hubspot
  steps:
  - id: s1
    builds: attribute
    uses:
    - sales_email_received
    - deal_stage
    - meeting_summary
    - product_activity
    - open_deal_task
    - prior_exchanges
    - lookback_window
    instruction: 'Create an AI-derived attribute ''reply_context'' computed when {sales_email_received} arrives. Combine:
      (a) the intent of the incoming email, classified as one of question, objection, scheduling-request, agreement, acknowledgment,
      or out-of-office; (b) the last {prior_exchanges} exchanges in the thread with this contact; (c) the stage from {deal_stage}
      and any recent {meeting_summary}; (d) {product_activity} by this contact within the last {lookback_window}; (e) any
      open {open_deal_task} on the deal. The context is the sole source for the draft, so keep every field populated where
      available.'
  - id: s2
    builds: automation
    uses:
    - s1
    - sales_email_received
    - active_deal_thread
    - rep_sent_emails
    - sent_sample_size
    - rep_gmail_drafts
    - rep_review_task
    - rep_slack
    instruction: 'Create a workflow that fires on {sales_email_received} for threads in {active_deal_thread} or the shared
      sales inbox. Step 1: compute the context in "Gather the reply context". Step 2: generate an AI reply draft using that
      context, matching the tone learned from the rep''s last {sent_sample_size} sent emails in {rep_sent_emails}. Step 3:
      save the draft to the rep''s drafts folder in {rep_gmail_drafts}. Do NOT send the message. Step 4: create a review task
      for the rep in {rep_review_task} titled ''Review AI draft: [thread subject]'' that includes a preview of the draft and
      a link to the source email. Step 5: send the rep a Slack direct message in {rep_slack} with the thread context and a
      review button. The rep may send as-is, edit, or discard the draft.'
  - id: s3
    builds: dashboard
    uses:
    - s1
    - s2
    - dashboard_report_period
    - discard_alert_threshold
    instruction: 'Build an AI-draft quality dashboard showing, per {dashboard_report_period} bucket: draft volume; send-as-drafted
      rate (drafts sent unchanged); edit-then-send rate; discard rate; median seconds from email arrival to reply sent, before
      and after enabling the workflow; and rep-by-rep adoption rate. Flag when discard rate exceeds {discard_alert_threshold}
      percent as a signal to retrain the draft model on recent rep behavior. Use the results of "Gather the reply context"
      and "Draft it into the rep''s outbox".'
---

# AI drafted sales replies

Slash command: /ai-draft-sales-reply

## Step 1: Gather the reply context

Create an AI-derived attribute 'reply_context' computed at email-received time. Pulls together: (a) the incoming email's intent classification (question / objection / scheduling-request / agreement / acknowledgment / out-of-office); (b) prior conversation thread (last 3 exchanges with this contact); (c) linked deal stage and any recent meeting_summary; (d) product activity by this contact in last 14 days; (e) any open tasks on the deal. The context blob is what the draft AI uses as its source: quality of context = quality of draft.

## Step 2: Draft it into the rep's outbox

Create a workflow firing on email_received in the shared sales inbox OR in any active-deal email thread. Step sequence: (1) compute reply_context; (2) generate AI-drafted reply with tone matching the rep's prior outbound style (learned from their last 50 sent emails); (3) save draft to the rep's outbox folder (NOT sent: gmail/outlook draft); (4) create a task for the rep labeled 'Review AI draft: [thread subject]' with a preview of the draft and a link to the email; (5) Slack DM with thread context and 'review' button. The rep can send-as-is, edit, or discard. NO auto-send. Use the result of "Gather the reply context".

## Step 3: See how good the drafts are

Compose an AI-draft quality dashboard: draft volume per week, send-as-drafted rate (drafts sent unchanged = high quality), edit-then-send rate, discard rate (signal of poor draft quality or wrong context), time saved per rep (median seconds from email-arrival to reply-sent, before vs. after enabling), and rep-by-rep adoption rate. Discard rate above 30% = retrain the draft model on more recent rep behavior. Use the result of "Gather the reply context", "Draft it into the rep's outbox".
