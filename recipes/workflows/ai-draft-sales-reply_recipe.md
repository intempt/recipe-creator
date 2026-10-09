---
name: ai-draft-sales-reply
description: Use when a user mentions "AI draft sales reply", "AI reply assistance", "shared inbox AI draft", or asks for related help. When a new email arrives in the shared sales inbox (or in an active deal conversation), AI-draft a personalized reply based on prior conversation context + deal stage + recent product activity, presented to the rep for one-click review-and-send.
arguments: []
intempt:
  id: ai-draft-sales-reply
  title: "AI drafted sales replies"
  version: 1.0.0
  slashCommand: /ai-draft-sales-reply
  group: Workflows
  shortDescription: "Drafts a reply to every inbound sales email using the thread, the deal stage and the buyer's recent product use, and leaves it in the rep's drafts."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: revops-automator
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [ai-draft, reply-assistance, sales-productivity]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: email_received, severity: blocking }
    integrations:
      - { value: slack, severity: recommended }
      - { value: gmail, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: "Gather the reply context"
      command: create_ai_attribute
      produces: attribute
      bindsAs: reply_context
      description: "At the moment the email lands: what the message is asking for, the last three exchanges with this contact, the deal stage and any meeting summary, what they have done in the product in the last 14 days, and any open tasks on the deal."
      prompt: 'Create an AI-derived attribute ''reply context'' computed when the email arrives. Pulls together: (a) the incoming email''s intent classification (question / objection / scheduling-request / agreement / acknowledgment / out-of-office); (b) prior conversation thread (last 3 exchanges with this contact); (c) linked deal stage and any recent meeting summary; (d) product activity by this contact in last 14 days; (e) any open tasks on the deal. The context blob is what the draft AI uses as its source: quality of context = quality of draft.'
    - step: 2
      title: "Draft it into the rep's outbox"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - reply_context
      description: "Fires on any email into the shared sales inbox or an active deal thread. It writes a reply in that rep's own style, learned from their last 50 sent emails, saves it as a draft rather than sending it, creates a review task with a preview, and sends the rep a Slack message. Nothing goes out automatically."
      prompt: 'Create a workflow firing on Email received in the shared sales inbox OR in any active-deal email thread. Step sequence: (1) compute the reply context; (2) generate AI-drafted reply with tone matching the rep''s prior outbound style (learned from their last 50 sent emails); (3) save draft to the rep''s outbox folder (NOT sent: gmail/outlook draft); (4) create a task for the rep labeled ''Review AI draft: [thread subject]'' with a preview of the draft and a link to the email; (5) Slack DM with thread context and ''review'' button. The rep can send-as-is, edit, or discard. NO auto-send.'
    - step: 3
      title: "See how good the drafts are"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - reply_context
      - workflow
      description: "Drafts per week, how many go out unchanged, how many are edited first, how many are thrown away, the median time from email in to reply out before and after, and adoption per rep. Above 30% discarded means the model needs retraining on newer behaviour."
      prompt: 'Compose an AI-draft quality dashboard: draft volume per week, send-as-drafted rate (drafts sent unchanged = high quality), edit-then-send rate, discard rate (signal of poor draft quality or wrong context), time saved per rep (median seconds from email-arrival to reply-sent, before vs. after enabling), and rep-by-rep adoption rate. Discard rate above 30% = retrain the draft model on more recent rep behavior.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# AI drafted sales replies

Drafts a reply to every inbound sales email using the thread, the deal stage and the buyer's recent product use, and leaves it in the rep's drafts.

## Before you run it

- Connect slack
- Connect gmail
- Send the `email_received` event

## What it does

1. **Gather the reply context** (`create_ai_attribute`)

   At the moment the email lands: what the message is asking for, the last three exchanges with this contact, the deal stage and any meeting summary, what they have done in the product in the last 14 days, and any open tasks on the deal.

2. **Draft it into the rep's outbox** (`create_workflow`)

   Fires on any email into the shared sales inbox or an active deal thread. It writes a reply in that rep's own style, learned from their last 50 sent emails, saves it as a draft rather than sending it, creates a review task with a preview, and sends the rep a Slack message. Nothing goes out automatically.

3. **See how good the drafts are** (`create_dashboard`)

   Drafts per week, how many go out unchanged, how many are edited first, how many are thrown away, the median time from email in to reply out before and after, and adoption per rep. Above 30% discarded means the model needs retraining on newer behaviour.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
