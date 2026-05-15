---
name: ai-draft-sales-reply
description: Use when a user mentions "AI draft sales reply", "AI reply assistance", "shared inbox AI draft", or asks for related help. When a new email arrives in the shared sales inbox (or in an active deal conversation), AI-draft a personalized reply based on prior conversation context + deal stage + recent product activity, presented to the rep for one-click review-and-send.
arguments: []
intempt:
  id: ai-draft-sales-reply
  version: 1.0.0
  slashCommand: /ai-draft-sales-reply
  group: Workflows
  shortDescription: "When a new email arrives in the shared sales inbox (or in an active deal conversation), AI-draft a personalized reply based on prior conversation context + deal stage + recent product activity, presented to the rep for one-click review-and-send."
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
      - { value: gmail, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_workflow
    - create_dashboard
  procedure:
    - step: 1
      title: Build Reply Context Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: reply_context
      description: 'Create an AI-derived attribute ''reply_context'' computed at email-received time. Pulls together: (a) the incoming email''s intent classification (question / objection / scheduling-request / agreement / acknowledgment / out-of-office); (b) prior conversation thread (last 3 exchanges with this contact); (c) linked deal stage and any recent meeting_summary; (d) product activity by this contact in last 14 days; (e) any open tasks on the deal. The context blob is what the draft AI uses as its source — quality of context = quality of draft.'
      prompt: 'Create an AI-derived attribute ''reply_context'' computed at email-received time. Pulls together: (a) the incoming email''s intent classification (question / objection / scheduling-request / agreement / acknowledgment / out-of-office); (b) prior conversation thread (last 3 exchanges with this contact); (c) linked deal stage and any recent meeting_summary; (d) product activity by this contact in last 14 days; (e) any open tasks on the deal. The context blob is what the draft AI uses as its source — quality of context = quality of draft.'
    - step: 2
      title: Build AI Draft Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - reply_context
      description: 'Create a workflow firing on email_received in the shared sales inbox OR in any active-deal email thread. Step sequence: (1) compute reply_context; (2) generate AI-drafted reply with tone matching the rep''s prior outbound style (learned from their last 50 sent emails); (3) save draft to the rep''s outbox folder (NOT sent — gmail/outlook draft); (4) create a task for the rep labeled ''Review AI draft: [thread subject]'' with a preview of the draft and a link to the email; (5) Slack DM with thread context and ''review'' button. The rep can send-as-is, edit, or discard. NO auto-send.'
      prompt: 'Create a workflow firing on email_received in the shared sales inbox OR in any active-deal email thread. Step sequence: (1) compute reply_context; (2) generate AI-drafted reply with tone matching the rep''s prior outbound style (learned from their last 50 sent emails); (3) save draft to the rep''s outbox folder (NOT sent — gmail/outlook draft); (4) create a task for the rep labeled ''Review AI draft: [thread subject]'' with a preview of the draft and a link to the email; (5) Slack DM with thread context and ''review'' button. The rep can send-as-is, edit, or discard. NO auto-send.'
    - step: 3
      title: Build AI Draft Quality Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - reply_context
      - workflow
      description: 'Compose an AI-draft quality dashboard: draft volume per week, send-as-drafted rate (drafts sent unchanged = high quality), edit-then-send rate, discard rate (signal of poor draft quality or wrong context), time saved per rep (median seconds from email-arrival to reply-sent, before vs. after enabling), and rep-by-rep adoption rate. Discard rate above 30% = retrain the draft model on more recent rep behavior.'
      prompt: 'Compose an AI-draft quality dashboard: draft volume per week, send-as-drafted rate (drafts sent unchanged = high quality), edit-then-send rate, discard rate (signal of poor draft quality or wrong context), time saved per rep (median seconds from email-arrival to reply-sent, before vs. after enabling), and rep-by-rep adoption rate. Discard rate above 30% = retrain the draft model on more recent rep behavior.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Ai Draft Sales Reply

## Procedure

1. **Build Reply Context Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'reply_context' computed at email-received time. Pulls together: (a) the incoming email's intent classification (question / objection / scheduling-request / agreement / acknowledgment / out-of-office); (b) prior conversation thread (last 3 exchanges with this contact); (c) linked deal stage and any recent meeting_summary; (d) product activity by this contact in last 14 days; (e) any open tasks on the deal. The context blob is what the draft AI uses as its source — quality of context = quality of draft. → produces: attribute
2. **Build AI Draft Workflow** [`create_workflow`] — Create a workflow firing on email_received in the shared sales inbox OR in any active-deal email thread. Step sequence: (1) compute reply_context; (2) generate AI-drafted reply with tone matching the rep's prior outbound style (learned from their last 50 sent emails); (3) save draft to the rep's outbox folder (NOT sent — gmail/outlook draft); (4) create a task for the rep labeled 'Review AI draft: [thread subject]' with a preview of the draft and a link to the email; (5) Slack DM with thread context and 'review' button. The rep can send-as-is, edit, or discard. NO auto-send. → produces: workflow
3. **Build AI Draft Quality Dashboard** [`create_dashboard`] — Compose an AI-draft quality dashboard: draft volume per week, send-as-drafted rate (drafts sent unchanged = high quality), edit-then-send rate, discard rate (signal of poor draft quality or wrong context), time saved per rep (median seconds from email-arrival to reply-sent, before vs. after enabling), and rep-by-rep adoption rate. Discard rate above 30% = retrain the draft model on more recent rep behavior. → produces: dashboard
