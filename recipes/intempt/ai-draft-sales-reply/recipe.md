---
description: Drafts a Gmail reply for a sales email thread using the thread, deal stage, and recent product activity, leaving it in the rep's drafts for review and send.
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
  - ecommerce
---

# AI drafted sales replies

Slash command: /ai-draft-sales-reply

## Step 1: Gather the reply context

Create an AI-derived attribute 'reply_context' computed at email-received time. Pulls together: (a) the incoming email's intent classification (question / objection / scheduling-request / agreement / acknowledgment / out-of-office); (b) prior conversation thread (last 3 exchanges with this contact); (c) linked deal stage and any recent meeting_summary; (d) product activity by this contact in last 14 days; (e) any open tasks on the deal. The context blob is what the draft AI uses as its source: quality of context = quality of draft.

## Step 2: Draft it into the rep's outbox

Create a workflow firing on email_received in the shared sales inbox OR in any active-deal email thread. Step sequence: (1) compute reply_context; (2) generate AI-drafted reply with tone matching the rep's prior outbound style (learned from their last 50 sent emails); (3) save draft to the rep's outbox folder (NOT sent: gmail/outlook draft); (4) create a task for the rep labeled 'Review AI draft: [thread subject]' with a preview of the draft and a link to the email; (5) Slack DM with thread context and 'review' button. The rep can send-as-is, edit, or discard. NO auto-send. Use the result of "Gather the reply context".

## Step 3: See how good the drafts are

Compose an AI-draft quality dashboard: draft volume per week, send-as-drafted rate (drafts sent unchanged = high quality), edit-then-send rate, discard rate (signal of poor draft quality or wrong context), time saved per rep (median seconds from email-arrival to reply-sent, before vs. after enabling), and rep-by-rep adoption rate. Discard rate above 30% = retrain the draft model on more recent rep behavior. Use the result of "Gather the reply context", "Draft it into the rep's outbox".
