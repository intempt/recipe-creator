---
name: ai-action-approval-queue
description: Use when a user mentions "AI action approval queue", "human-in-the-loop workflow", "AI approval gate", or asks for related help. High-value AI-suggested actions (auto-email to high-ARR account, mass account update, large segment send, AI-classified routing decisions) pause for human approval before execution. Slack-based approval. The Relay-style HITL pattern that combines AI scale with human judgment.
arguments: []
intempt:
  id: ai-action-approval-queue
  title: "Human approval for AI actions"
  version: 1.0.0
  slashCommand: /ai-action-approval-queue
  group: Workflows
  shortDescription: "Holds the riskier things an AI workflow wants to do, such as a mass update or a send to a big account, for a yes or no in Slack."
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
  prerequisites:
    integrations:
      - { value: slack, severity: blocking }
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
      title: "Gate the risky AI actions"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Sits in front of the high stakes actions an AI workflow wants to take. You set what needs approval: an ARR cutoff, a segment size, the kind of action, or how confident the AI was."
      prompt: 'Create a workflow ''AI action approval queue'' that intercepts high-stakes AI-generated actions and requires human approval before execution. Goal: capture AI''s speed while keeping human judgment on the consequential decisions. Configurable threshold for what triggers approval (ARR cutoff, segment size, action type, AI confidence).'
    - step: 2
      title: "Let other workflows queue one"
      command: configure_webhook_step
      produces: step
      bindsAs: webhook
      dependsOn:
      - workflow
      description: "A webhook other workflows call to submit an action. It carries the kind of action, a one line summary, the full payload, which workflow asked, and why this one needs approval."
      prompt: 'Configure webhook trigger that other workflows call when they want to queue an action for approval. Payload schema: action_type (send_email / update_records / route_lead / make_decision), action_summary (one-line description), full_payload (the actual action data), requesting_workflow (originator), threshold_reason (why this needs approval: high-ARR / large-segment / low-confidence).'
    - step: 3
      title: "Send it to the right approver"
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: type_split
      dependsOn:
      - workflow
      - webhook
      description: "Emails go to marketing, record updates to RevOps, lead routing to a sales manager, and other decisions by type. The wrong approver is what turns this into a bottleneck."
      prompt: 'Multi-split by action_type: send_email to marketing lead approval; update_records to RevOps approval; route_lead to sales manager approval; make_decision to varies by decision type. Each routes to the right approver Slack channel. The approver matters: wrong approver leads to bottlenecks.'
    - step: 4
      title: "Ask in Slack"
      command: configure_slack_step
      produces: step
      bindsAs: slack_prompt
      dependsOn:
      - workflow
      - type_split
      description: "An interactive message in the approver's channel with the summary, the workflow that asked, why it needs approval, a preview such as the subject line and first 200 characters, and approve or reject buttons."
      prompt: 'Configure Slack step that posts an interactive approval message to the right channel/user. Message includes: action summary, originator workflow, threshold reason, action preview (e.g. for email: subject + first 200 chars), and Approve/Reject buttons (or Slack thread-reply ''approve''/''reject''). Tag the specific approver.'
    - step: 5
      title: "Wait for an answer"
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: wait
      dependsOn:
      - workflow
      - slack_prompt
      description: "Execution pauses until someone responds, four hours by default. Shorten it for a big send, stretch it for routine updates. Silence counts as a rejection and posts a notice."
      prompt: 'Configure wait-until step that pauses workflow execution until approval response received. Timeout: 4 hours (configurable: high-ARR sends might warrant 1hr, routine updates might allow 24hrs). On timeout: default-reject (safer than default-approve) + post ''auto-rejected after timeout'' notification.'
    - step: 6
      title: "Act on the decision"
      command: configure_workflow_branch_step
      produces: step
      bindsAs: decision_branch
      dependsOn:
      - workflow
      - wait
      description: "Approved runs the action. Rejected archives it with the reason, tells the originating workflow to stop, and posts the reasoning to the governance channel. A timeout behaves like a rejection and is logged as one."
      prompt: 'Branch step on the approval decision: APPROVED to execute action (webhook back to originator workflow with ''go ahead''); REJECTED to archive with rejection reason + notify originator workflow to abort + post reasoning to #ai-governance for learning; TIMEOUT to same as rejected, with timeout reason logged.'
    - step: 7
      title: "Tell the workflow to proceed"
      command: configure_webhook_step
      produces: step
      bindsAs: execute
      dependsOn:
      - workflow
      - decision_branch
      description: "A webhook back to the workflow that asked, carrying the approver, the timestamp and any comment, all written to the audit trail so every AI action is traceable."
      prompt: Configure webhook call back to the originator workflow to proceed with the queued action. Include approval metadata (approver name, timestamp, any approver comments). Log to audit trail, every AI action that went through approval is fully traceable for compliance + later review.
    - step: 8
      title: "Log what humans reject"
      command: configure_update_attribute_step
      produces: step
      bindsAs: log
      dependsOn:
      - workflow
      - decision_branch
      description: "Every rejection and its reason goes into a structured log, which over time shows which AI behaviours need tighter prompts or guardrails."
      prompt: 'On rejected branch: write the rejection to a structured learning log: which AI suggestions are humans rejecting, what''s the rejection reason. Over time this reveals which AI behaviors need prompt tuning or guardrails. The reject log is the feedback loop that improves the underlying AI workflows.'
    - step: 9
      title: "Publish and watch the queue"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - execute
      - log
      description: "Validated and published, with approvals per week, the approval rate against an 80% target, the median time to a decision inside business hours against 30 minutes, and the timeout rate, which points at the wrong approver or a dead channel."
      prompt: 'Validate and publish. Monitor: approval volume per week, approval-rate (target: 80%+; below 60% suggests upstream AI workflows need tuning), median time-to-decision (target: under 30min during business hours), timeout rate (high = wrong approvers or low-engagement channel). The dashboard for responsible AI governance.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Human approval for AI actions

Holds the riskier things an AI workflow wants to do, such as a mass update or a send to a big account, for a yes or no in Slack.

## Before you run it

- Connect slack

## What it does

1. **Gate the risky AI actions** (`create_workflow`)

   Sits in front of the high stakes actions an AI workflow wants to take. You set what needs approval: an ARR cutoff, a segment size, the kind of action, or how confident the AI was.

2. **Let other workflows queue one** (`configure_webhook_step`)

   A webhook other workflows call to submit an action. It carries the kind of action, a one line summary, the full payload, which workflow asked, and why this one needs approval.

3. **Send it to the right approver** (`configure_workflow_multi_split_step`)

   Emails go to marketing, record updates to RevOps, lead routing to a sales manager, and other decisions by type. The wrong approver is what turns this into a bottleneck.

4. **Ask in Slack** (`configure_slack_step`)

   An interactive message in the approver's channel with the summary, the workflow that asked, why it needs approval, a preview such as the subject line and first 200 characters, and approve or reject buttons.

5. **Wait for an answer** (`configure_workflow_wait_until_step`)

   Execution pauses until someone responds, four hours by default. Shorten it for a big send, stretch it for routine updates. Silence counts as a rejection and posts a notice.

6. **Act on the decision** (`configure_workflow_branch_step`)

   Approved runs the action. Rejected archives it with the reason, tells the originating workflow to stop, and posts the reasoning to the governance channel. A timeout behaves like a rejection and is logged as one.

7. **Tell the workflow to proceed** (`configure_webhook_step`)

   A webhook back to the workflow that asked, carrying the approver, the timestamp and any comment, all written to the audit trail so every AI action is traceable.

8. **Log what humans reject** (`configure_update_attribute_step`)

   Every rejection and its reason goes into a structured log, which over time shows which AI behaviours need tighter prompts or guardrails.

9. **Publish and watch the queue** (`publish_workflow`)

   Validated and published, with approvals per week, the approval rate against an 80% target, the median time to a decision inside business hours against 30 minutes, and the timeout rate, which points at the wrong approver or a dead channel.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
