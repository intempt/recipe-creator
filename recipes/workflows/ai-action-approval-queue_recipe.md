---
name: ai-action-approval-queue
description: Use when a user mentions "AI action approval queue", "human-in-the-loop workflow", "AI approval gate", or asks for related help. High-value AI-suggested actions (auto-email to high-ARR account, mass account update, large segment send, AI-classified routing decisions) pause for human approval before execution. Slack-based approval. The Relay-style HITL pattern that combines AI scale with human judgment.
arguments: []
intempt:
  id: ai-action-approval-queue
  version: 1.0.0
  slashCommand: /ai-action-approval-queue
  group: Workflows
  shortDescription: "Create a workflow that queues high-value AI actions via webhook, routes them to Slack for human approval, then branches to execute or reject."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: workflow-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [human-in-the-loop, approval-gate, ai-governance]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_workflow
    - configure_webhook_step
    - configure_workflow_multi_split_step
    - configure_slack_step
    - configure_workflow_wait_until_step
    - configure_workflow_branch_step
    - configure_update_attribute_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the HITL Approval Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''AI action approval queue'' that intercepts high-stakes AI-generated actions and requires human approval before execution. Goal: capture AI''s speed while keeping human judgment on the consequential decisions. Configurable threshold for what triggers approval (ARR cutoff, segment size, action type, AI confidence).'
      prompt: 'Create a workflow ''AI action approval queue'' that intercepts high-stakes AI-generated actions and requires human approval before execution. Goal: capture AI''s speed while keeping human judgment on the consequential decisions. Configurable threshold for what triggers approval (ARR cutoff, segment size, action type, AI confidence).'
    - step: 2
      title: Webhook Receives Pending AI Action
      command: configure_webhook_step
      produces: step
      bindsAs: webhook
      dependsOn:
      - workflow
      description: 'Configure webhook trigger that other workflows call when they want to queue an action for approval. Payload schema: action_type (send_email / update_records / route_lead / make_decision), action_summary (one-line description), full_payload (the actual action data), requesting_workflow (originator), threshold_reason (why this needs approval — high-ARR / large-segment / low-confidence).'
      prompt: 'Configure webhook trigger that other workflows call when they want to queue an action for approval. Payload schema: action_type (send_email / update_records / route_lead / make_decision), action_summary (one-line description), full_payload (the actual action data), requesting_workflow (originator), threshold_reason (why this needs approval — high-ARR / large-segment / low-confidence).'
    - step: 3
      title: Branch by Action Type
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: type_split
      dependsOn:
      - workflow
      - webhook
      description: 'Multi-split by action_type: send_email → marketing lead approval; update_records → RevOps approval; route_lead → sales manager approval; make_decision → varies by decision type. Each routes to the right approver Slack channel. The approver matters — wrong approver leads to bottlenecks.'
      prompt: 'Multi-split by action_type: send_email → marketing lead approval; update_records → RevOps approval; route_lead → sales manager approval; make_decision → varies by decision type. Each routes to the right approver Slack channel. The approver matters — wrong approver leads to bottlenecks.'
    - step: 4
      title: Slack Approval Prompt
      command: configure_slack_step
      produces: step
      bindsAs: slack_prompt
      dependsOn:
      - workflow
      - type_split
      description: 'Configure Slack step that posts an interactive approval message to the right channel/user. Message includes: action summary, originator workflow, threshold reason, action preview (e.g. for email: subject + first 200 chars), and Approve/Reject buttons (or Slack thread-reply ''approve''/''reject''). Tag the specific approver.'
      prompt: 'Configure Slack step that posts an interactive approval message to the right channel/user. Message includes: action summary, originator workflow, threshold reason, action preview (e.g. for email: subject + first 200 chars), and Approve/Reject buttons (or Slack thread-reply ''approve''/''reject''). Tag the specific approver.'
    - step: 5
      title: Wait Until Approval
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: wait
      dependsOn:
      - workflow
      - slack_prompt
      description: 'Configure wait-until step that pauses workflow execution until approval response received. Timeout: 4 hours (configurable — high-ARR sends might warrant 1hr, routine updates might allow 24hrs). On timeout: default-reject (safer than default-approve) + post ''auto-rejected after timeout'' notification.'
      prompt: 'Configure wait-until step that pauses workflow execution until approval response received. Timeout: 4 hours (configurable — high-ARR sends might warrant 1hr, routine updates might allow 24hrs). On timeout: default-reject (safer than default-approve) + post ''auto-rejected after timeout'' notification.'
    - step: 6
      title: Branch on Decision
      command: configure_workflow_branch_step
      produces: step
      bindsAs: decision_branch
      dependsOn:
      - workflow
      - wait
      description: 'Branch step on the approval decision: APPROVED → execute action (webhook back to originator workflow with ''go ahead''); REJECTED → archive with rejection reason + notify originator workflow to abort + post reasoning to #ai-governance for learning; TIMEOUT → same as rejected, with timeout reason logged.'
      prompt: 'Branch step on the approval decision: APPROVED → execute action (webhook back to originator workflow with ''go ahead''); REJECTED → archive with rejection reason + notify originator workflow to abort + post reasoning to #ai-governance for learning; TIMEOUT → same as rejected, with timeout reason logged.'
    - step: 7
      title: 'Approved Path: Execute and Log'
      command: configure_webhook_step
      produces: step
      bindsAs: execute
      dependsOn:
      - workflow
      - decision_branch
      description: Configure webhook call back to the originator workflow to proceed with the queued action. Include approval metadata (approver name, timestamp, any approver comments). Log to audit trail — every AI action that went through approval is fully traceable for compliance + later review.
      prompt: Configure webhook call back to the originator workflow to proceed with the queued action. Include approval metadata (approver name, timestamp, any approver comments). Log to audit trail — every AI action that went through approval is fully traceable for compliance + later review.
    - step: 8
      title: 'Rejected Path: Log Learning'
      command: configure_update_attribute_step
      produces: step
      bindsAs: log
      dependsOn:
      - workflow
      - decision_branch
      description: 'On rejected branch: write the rejection to a structured learning log — which AI suggestions are humans rejecting, what''s the rejection reason. Over time this reveals which AI behaviors need prompt tuning or guardrails. The reject log is the feedback loop that improves the underlying AI workflows.'
      prompt: 'On rejected branch: write the rejection to a structured learning log — which AI suggestions are humans rejecting, what''s the rejection reason. Over time this reveals which AI behaviors need prompt tuning or guardrails. The reject log is the feedback loop that improves the underlying AI workflows.'
    - step: 9
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - execute
      - log
      description: 'Validate and publish. Monitor: approval volume per week, approval-rate (target: 80%+; below 60% suggests upstream AI workflows need tuning), median time-to-decision (target: under 30min during business hours), timeout rate (high = wrong approvers or low-engagement channel). The dashboard for responsible AI governance.'
      prompt: 'Validate and publish. Monitor: approval volume per week, approval-rate (target: 80%+; below 60% suggests upstream AI workflows need tuning), median time-to-decision (target: under 30min during business hours), timeout rate (high = wrong approvers or low-engagement channel). The dashboard for responsible AI governance.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Ai Action Approval Queue

## Procedure

1. **Build the HITL Approval Workflow** [`create_workflow`] — Create a workflow 'AI action approval queue' that intercepts high-stakes AI-generated actions and requires human approval before execution. Goal: capture AI's speed while keeping human judgment on the consequential decisions. Configurable threshold for what triggers approval (ARR cutoff, segment size, action type, AI confidence). → produces: workflow
2. **Webhook Receives Pending AI Action** [`configure_webhook_step`] — Configure webhook trigger that other workflows call when they want to queue an action for approval. Payload schema: action_type (send_email / update_records / route_lead / make_decision), action_summary (one-line description), full_payload (the actual action data), requesting_workflow (originator), threshold_reason (why this needs approval — high-ARR / large-segment / low-confidence). → produces: step
3. **Branch by Action Type** [`configure_workflow_multi_split_step`] — Multi-split by action_type: send_email → marketing lead approval; update_records → RevOps approval; route_lead → sales manager approval; make_decision → varies by decision type. Each routes to the right approver Slack channel. The approver matters — wrong approver leads to bottlenecks. → produces: step
4. **Slack Approval Prompt** [`configure_slack_step`] — Configure Slack step that posts an interactive approval message to the right channel/user. Message includes: action summary, originator workflow, threshold reason, action preview (e.g. for email: subject + first 200 chars), and Approve/Reject buttons (or Slack thread-reply 'approve'/'reject'). Tag the specific approver. → produces: step
5. **Wait Until Approval** [`configure_workflow_wait_until_step`] — Configure wait-until step that pauses workflow execution until approval response received. Timeout: 4 hours (configurable — high-ARR sends might warrant 1hr, routine updates might allow 24hrs). On timeout: default-reject (safer than default-approve) + post 'auto-rejected after timeout' notification. → produces: step
6. **Branch on Decision** [`configure_workflow_branch_step`] — Branch step on the approval decision: APPROVED → execute action (webhook back to originator workflow with 'go ahead'); REJECTED → archive with rejection reason + notify originator workflow to abort + post reasoning to #ai-governance for learning; TIMEOUT → same as rejected, with timeout reason logged. → produces: step
7. **Approved Path: Execute and Log** [`configure_webhook_step`] — Configure webhook call back to the originator workflow to proceed with the queued action. Include approval metadata (approver name, timestamp, any approver comments). Log to audit trail — every AI action that went through approval is fully traceable for compliance + later review. → produces: step
8. **Rejected Path: Log Learning** [`configure_update_attribute_step`] — On rejected branch: write the rejection to a structured learning log — which AI suggestions are humans rejecting, what's the rejection reason. Over time this reveals which AI behaviors need prompt tuning or guardrails. The reject log is the feedback loop that improves the underlying AI workflows. → produces: step
9. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: approval volume per week, approval-rate (target: 80%+; below 60% suggests upstream AI workflows need tuning), median time-to-decision (target: under 30min during business hours), timeout rate (high = wrong approvers or low-engagement channel). The dashboard for responsible AI governance. → produces: workflow
