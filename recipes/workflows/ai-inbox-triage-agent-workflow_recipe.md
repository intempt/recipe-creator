---
name: ai-inbox-triage-agent-workflow
description: Use when a user mentions "AI inbox triage agent", "inbound conversation routing", "AI classify and route messages", or asks for related help. Inbound conversations (email, chat, form) hit an AI triage agent that classifies intent (sales / support / billing / partnership / spam) and routes via multi-split to the right team + drafts an appropriate first response. Replaces the manual 'who handles this?' loop.
arguments: []
intempt:
  id: ai-inbox-triage-agent-workflow
  version: 1.0.0
  slashCommand: /ai-inbox-triage-agent-workflow
  group: Workflows
  shortDescription: "Inbound conversations (email, chat, form) hit an AI triage agent that classifies intent (sales / support / billing / partnership / spam) and routes via multi-split to the right team + drafts an appropriate first response. Replaces the manual 'who handles this?' loop."
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
      title: Build the Triage Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''AI inbox triage'' triggered when a new inbound conversation arrives in any tracked channel (email, web chat, contact form, social DM via webhook). Goal: every message reaches the right human within 5 minutes with appropriate context attached, replacing the manual ops triage.'
      prompt: 'Create a workflow ''AI inbox triage'' triggered when a new inbound conversation arrives in any tracked channel (email, web chat, contact form, social DM via webhook). Goal: every message reaches the right human within 5 minutes with appropriate context attached, replacing the manual ops triage.'
    - step: 2
      title: AI Classification Step
      command: configure_ai_research_step
      produces: step
      bindsAs: classify
      dependsOn:
      - workflow
      description: 'Configure AI step that classifies the inbound message into one of: sales-inquiry (interested in buying), support-question (existing customer issue), billing-question (payment/account), partnership (BD/integration), spam/non-actionable, or escalation-required (legal threat, security, abuse). Output: intent_label + confidence + extracted entities (mentioned products, mentioned competitors, urgency signals).'
      prompt: 'Configure AI step that classifies the inbound message into one of: sales-inquiry (interested in buying), support-question (existing customer issue), billing-question (payment/account), partnership (BD/integration), spam/non-actionable, or escalation-required (legal threat, security, abuse). Output: intent_label + confidence + extracted entities (mentioned products, mentioned competitors, urgency signals).'
    - step: 3
      title: Multi-Split by Intent
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: route
      dependsOn:
      - workflow
      - classify
      description: 'Configure multi-split routing into branches: sales-inquiry → AE task + sales-inbox; support-question → support queue (linked customer); billing-question → finance queue; partnership → BD task; spam → archive silently; escalation-required → on-call alert. Each branch gets the full message context attached.'
      prompt: 'Configure multi-split routing into branches: sales-inquiry → AE task + sales-inbox; support-question → support queue (linked customer); billing-question → finance queue; partnership → BD task; spam → archive silently; escalation-required → on-call alert. Each branch gets the full message context attached.'
    - step: 4
      title: 'Sales Branch: Match Sender'
      command: configure_find_records_step
      produces: step
      bindsAs: match_sender
      dependsOn:
      - workflow
      - route
      description: 'On the sales-inquiry branch: try to match sender''s email/domain to an existing Account or Lead. If match, surface their history (prior touches, opened deals, account tier). If no match, create lead with auto-enrichment trigger.'
      prompt: 'On the sales-inquiry branch: try to match sender''s email/domain to an existing Account or Lead. If match, surface their history (prior touches, opened deals, account tier). If no match, create lead with auto-enrichment trigger.'
    - step: 5
      title: 'Sales Branch: AI-Draft Initial Reply'
      command: configure_write_with_ai_step
      produces: step
      bindsAs: draft_reply
      dependsOn:
      - workflow
      - match_sender
      description: 'Configure AI write step on the sales branch: draft a personalized initial reply acknowledging the inquiry, referencing any past interactions if matched, offering specific next steps (book a demo / talk to specialist / send pricing). Saved as draft on the AE task; AE reviews, edits if needed, sends. Reply-SLA target: 5 minutes from inbound.'
      prompt: 'Configure AI write step on the sales branch: draft a personalized initial reply acknowledging the inquiry, referencing any past interactions if matched, offering specific next steps (book a demo / talk to specialist / send pricing). Saved as draft on the AE task; AE reviews, edits if needed, sends. Reply-SLA target: 5 minutes from inbound.'
    - step: 6
      title: 'Sales Branch: Create AE Task'
      command: configure_create_task_step
      produces: step
      bindsAs: ae_task
      dependsOn:
      - workflow
      - match_sender
      - draft_reply
      description: 'Create AE task with: original message, AI classification + confidence, matched account/lead context, AI-drafted reply ready-to-send. Assign by territory or round-robin. Priority: HIGH for known accounts, MEDIUM for unknown. SLA: 5-minute first response.'
      prompt: 'Create AE task with: original message, AI classification + confidence, matched account/lead context, AI-drafted reply ready-to-send. Assign by territory or round-robin. Priority: HIGH for known accounts, MEDIUM for unknown. SLA: 5-minute first response.'
    - step: 7
      title: 'Support Branch: Route to Support Queue'
      command: configure_create_task_step
      produces: step
      bindsAs: support_task
      dependsOn:
      - workflow
      - route
      description: 'On the support-question branch: route to support queue with customer context (account tier, recent product usage, recent tickets). If customer is on a paid plan, flag as priority; if free-tier, route to FAQ-first response template.'
      prompt: 'On the support-question branch: route to support queue with customer context (account tier, recent product usage, recent tickets). If customer is on a paid plan, flag as priority; if free-tier, route to FAQ-first response template.'
    - step: 8
      title: Slack Alert for Edge Cases
      command: configure_slack_step
      produces: step
      bindsAs: slack
      dependsOn:
      - workflow
      - classify
      description: 'Configure Slack step that fires when AI classification confidence is below 60% OR when the message is escalation-required type. Posts to #ops-triage channel with the message and AI''s best guess at routing, asking for human review. Don''t let edge cases fall through.'
      prompt: 'Configure Slack step that fires when AI classification confidence is below 60% OR when the message is escalation-required type. Posts to #ops-triage channel with the message and AI''s best guess at routing, asking for human review. Don''t let edge cases fall through.'
    - step: 9
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - ae_task
      - support_task
      - slack
      description: 'Validate and publish. Monitor: classification accuracy (sample 5% of messages weekly, human-rates whether the AI got it right — target: 90%+), first-response SLA, mis-routed-message rate. Tune the AI prompts when accuracy dips.'
      prompt: 'Validate and publish. Monitor: classification accuracy (sample 5% of messages weekly, human-rates whether the AI got it right — target: 90%+), first-response SLA, mis-routed-message rate. Tune the AI prompts when accuracy dips.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Ai Inbox Triage Agent Workflow

## Procedure

1. **Build the Triage Workflow** [`create_workflow`] — Create a workflow 'AI inbox triage' triggered when a new inbound conversation arrives in any tracked channel (email, web chat, contact form, social DM via webhook). Goal: every message reaches the right human within 5 minutes with appropriate context attached, replacing the manual ops triage. → produces: workflow
2. **AI Classification Step** [`configure_ai_research_step`] — Configure AI step that classifies the inbound message into one of: sales-inquiry (interested in buying), support-question (existing customer issue), billing-question (payment/account), partnership (BD/integration), spam/non-actionable, or escalation-required (legal threat, security, abuse). Output: intent_label + confidence + extracted entities (mentioned products, mentioned competitors, urgency signals). → produces: step
3. **Multi-Split by Intent** [`configure_workflow_multi_split_step`] — Configure multi-split routing into branches: sales-inquiry → AE task + sales-inbox; support-question → support queue (linked customer); billing-question → finance queue; partnership → BD task; spam → archive silently; escalation-required → on-call alert. Each branch gets the full message context attached. → produces: step
4. **Sales Branch: Match Sender** [`configure_find_records_step`] — On the sales-inquiry branch: try to match sender's email/domain to an existing Account or Lead. If match, surface their history (prior touches, opened deals, account tier). If no match, create lead with auto-enrichment trigger. → produces: step
5. **Sales Branch: AI-Draft Initial Reply** [`configure_write_with_ai_step`] — Configure AI write step on the sales branch: draft a personalized initial reply acknowledging the inquiry, referencing any past interactions if matched, offering specific next steps (book a demo / talk to specialist / send pricing). Saved as draft on the AE task; AE reviews, edits if needed, sends. Reply-SLA target: 5 minutes from inbound. → produces: step
6. **Sales Branch: Create AE Task** [`configure_create_task_step`] — Create AE task with: original message, AI classification + confidence, matched account/lead context, AI-drafted reply ready-to-send. Assign by territory or round-robin. Priority: HIGH for known accounts, MEDIUM for unknown. SLA: 5-minute first response. → produces: step
7. **Support Branch: Route to Support Queue** [`configure_create_task_step`] — On the support-question branch: route to support queue with customer context (account tier, recent product usage, recent tickets). If customer is on a paid plan, flag as priority; if free-tier, route to FAQ-first response template. → produces: step
8. **Slack Alert for Edge Cases** [`configure_slack_step`] — Configure Slack step that fires when AI classification confidence is below 60% OR when the message is escalation-required type. Posts to #ops-triage channel with the message and AI's best guess at routing, asking for human review. Don't let edge cases fall through. → produces: step
9. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: classification accuracy (sample 5% of messages weekly, human-rates whether the AI got it right — target: 90%+), first-response SLA, mis-routed-message rate. Tune the AI prompts when accuracy dips. → produces: workflow
