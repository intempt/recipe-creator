---
id: ai-draft-sales-reply
title: AI drafted sales replies
slash_command: /ai-draft-sales-reply
group: Workflows
owner: intempt
summary: Drafts a reply to every inbound sales email using the thread, the deal stage and the buyer's
  recent product use, and leaves it in the rep's drafts.
description: >-
  When a new email arrives in the shared sales inbox (or in an active deal conversation), AI-draft a personalized
  reply based on prior conversation context + deal stage + recent product activity, presented to the rep
  for one-click review-and-send.
version: 2.0.0
classification:
  product:
    - sales
  agent: revops-automator
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - ai-draft
    - reply-assistance
    - sales-productivity
prerequisites:
  events:
    - value: email_received
      severity: blocking
  integrations:
    - value: slack
      severity: recommended
    - value: gmail
      severity: recommended
touches:
  reads:
    - The email_received event in your project
    - Your Slack connection
    - Your Gmail connection
  writes:
    - A new attribute, from step 1 "Gather the reply context"
    - A new workflow, from step 2 "Draft it into the rep's outbox"
    - A new dashboard, from step 3 "See how good the drafts are"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Gather the reply context
    summary: >-
      At the moment the email lands: what the message is asking for, the last three exchanges with this
      contact, the deal stage and any meeting summary, what they have done in the product in the last
      14 days, and any open tasks on the deal.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'reply_context' computed at email-received time. Pulls together:
      (a) the incoming email's intent classification (question / objection / scheduling-request / agreement
      / acknowledgment / out-of-office); (b) prior conversation thread (last 3 exchanges with this contact);
      (c) linked deal stage and any recent meeting_summary; (d) product activity by this contact in last
      14 days; (e) any open tasks on the deal. The context blob is what the draft AI uses as its source:
      quality of context = quality of draft.
  - id: s2
    title: Draft it into the rep's outbox
    summary: >-
      Fires on any email into the shared sales inbox or an active deal thread. It writes a reply in that
      rep's own style, learned from their last 50 sent emails, saves it as a draft rather than sending
      it, creates a review task with a preview, and sends the rep a Slack message. Nothing goes out automatically.
    builds: workflow
    description: >-
      Create a workflow firing on email_received in the shared sales inbox OR in any active-deal email
      thread. Step sequence: (1) compute reply_context; (2) generate AI-drafted reply with tone matching
      the rep's prior outbound style (learned from their last 50 sent emails); (3) save draft to the rep's
      outbox folder (NOT sent: gmail/outlook draft); (4) create a task for the rep labeled 'Review AI
      draft: [thread subject]' with a preview of the draft and a link to the email; (5) Slack DM with
      thread context and 'review' button. The rep can send-as-is, edit, or discard. NO auto-send. Use
      the result of "Gather the reply context".
    dependsOn:
      - s1
  - id: s3
    title: See how good the drafts are
    summary: >-
      Drafts per week, how many go out unchanged, how many are edited first, how many are thrown away,
      the median time from email in to reply out before and after, and adoption per rep. Above 30% discarded
      means the model needs retraining on newer behaviour.
    builds: dashboard
    description: >-
      Compose an AI-draft quality dashboard: draft volume per week, send-as-drafted rate (drafts sent
      unchanged = high quality), edit-then-send rate, discard rate (signal of poor draft quality or wrong
      context), time saved per rep (median seconds from email-arrival to reply-sent, before vs. after
      enabling), and rep-by-rep adoption rate. Discard rate above 30% = retrain the draft model on more
      recent rep behavior. Use the result of "Gather the reply context", "Draft it into the rep's outbox".
    dependsOn:
      - s1
      - s2
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: workflow
    producedByStep: s2
    type: workflow
    description: Workflow produced by this recipe.
  - key: dashboard
    producedByStep: s3
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# AI drafted sales replies

Drafts a reply to every inbound sales email using the thread, the deal stage and the buyer's recent product use, and leaves it in the rep's drafts.

## Steps

1. **Gather the reply context** (builds attribute)

   At the moment the email lands: what the message is asking for, the last three exchanges with this contact, the deal stage and any meeting summary, what they have done in the product in the last 14 days, and any open tasks on the deal.

2. **Draft it into the rep's outbox** (builds workflow)

   Fires on any email into the shared sales inbox or an active deal thread. It writes a reply in that rep's own style, learned from their last 50 sent emails, saves it as a draft rather than sending it, creates a review task with a preview, and sends the rep a Slack message. Nothing goes out automatically.

3. **See how good the drafts are** (builds dashboard)

   Drafts per week, how many go out unchanged, how many are edited first, how many are thrown away, the median time from email in to reply out before and after, and adoption per rep. Above 30% discarded means the model needs retraining on newer behaviour.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The email_received event in your project
- Your Slack connection
- Your Gmail connection

Writes:

- A new attribute, from step 1 "Gather the reply context"
- A new workflow, from step 2 "Draft it into the rep's outbox"
- A new dashboard, from step 3 "See how good the drafts are"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, workflow.
