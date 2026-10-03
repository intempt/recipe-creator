---
id: ai-action-approval-queue
title: Human approval for AI actions
slash_command: /ai-action-approval-queue
group: Workflows
owner: intempt
curator: trishik
summary: Holds the riskier things an AI workflow wants to do, such as a mass update or a send to a big
  account, for a yes or no in Slack.
description: >-
  High-value AI-suggested actions (auto-email to high-ARR account, mass account update, large segment
  send, AI-classified routing decisions) pause for human approval before execution. Slack-based approval.
  The Relay-style HITL pattern that combines AI scale with human judgment.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: workflow-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - human-in-the-loop
    - approval-gate
    - ai-governance
prerequisites:
  integrations:
    - value: slack
      severity: blocking
touches:
  reads:
    - Your Slack connection
  writes:
    - A new workflow, from step 1 "Gate the risky AI actions"
    - A new workflow, from step 2 "Let other workflows queue one"
    - A new workflow, from step 3 "Send it to the right approver"
    - A new workflow, from step 4 "Ask in Slack"
    - A new workflow, from step 5 "Wait for an answer"
    - A new workflow, from step 6 "Act on the decision"
    - A new workflow, from step 7 "Tell the workflow to proceed"
    - A new workflow, from step 8 "Log what humans reject"
    - A new workflow, from step 9 "Publish and watch the queue"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Gate the risky AI actions
    summary: >-
      Sits in front of the high stakes actions an AI workflow wants to take. You set what needs approval:
      an ARR cutoff, a segment size, the kind of action, or how confident the AI was.
    builds: workflow
    description: >-
      Create a workflow 'AI action approval queue' that intercepts high-stakes AI-generated actions and
      requires human approval before execution. Goal: capture AI's speed while keeping human judgment
      on the consequential decisions. Configurable threshold for what triggers approval (ARR cutoff, segment
      size, action type, AI confidence).
  - id: s2
    title: Let other workflows queue one
    summary: >-
      A webhook other workflows call to submit an action. It carries the kind of action, a one line summary,
      the full payload, which workflow asked, and why this one needs approval.
    builds: workflow
    description: >-
      Configure webhook trigger that other workflows call when they want to queue an action for approval.
      Payload schema: action_type (send_email / update_records / route_lead / make_decision), action_summary
      (one-line description), full_payload (the actual action data), requesting_workflow (originator),
      threshold_reason (why this needs approval: high-ARR / large-segment / low-confidence). Use the result
      of "Gate the risky AI actions".
    dependsOn:
      - s1
  - id: s3
    title: Send it to the right approver
    summary: >-
      Emails go to marketing, record updates to RevOps, lead routing to a sales manager, and other decisions
      by type. The wrong approver is what turns this into a bottleneck.
    builds: workflow
    description: >-
      Multi-split by action_type: send_email to marketing lead approval; update_records to RevOps approval;
      route_lead to sales manager approval; make_decision to varies by decision type. Each routes to the
      right approver Slack channel. The approver matters: wrong approver leads to bottlenecks. Use the
      result of "Gate the risky AI actions", "Let other workflows queue one".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Ask in Slack
    summary: >-
      An interactive message in the approver's channel with the summary, the workflow that asked, why
      it needs approval, a preview such as the subject line and first 200 characters, and approve or reject
      buttons.
    builds: workflow
    description: >-
      Configure Slack step that posts an interactive approval message to the right channel/user. Message
      includes: action summary, originator workflow, threshold reason, action preview (e.g. for email:
      subject + first 200 chars), and Approve/Reject buttons (or Slack thread-reply 'approve'/'reject').
      Tag the specific approver. Use the result of "Gate the risky AI actions", "Send it to the right
      approver".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Wait for an answer
    summary: >-
      Execution pauses until someone responds, four hours by default. Shorten it for a big send, stretch
      it for routine updates. Silence counts as a rejection and posts a notice.
    builds: workflow
    description: >-
      Configure wait-until step that pauses workflow execution until approval response received. Timeout:
      4 hours (configurable: high-ARR sends might warrant 1hr, routine updates might allow 24hrs). On
      timeout: default-reject (safer than default-approve) + post 'auto-rejected after timeout' notification.
      Use the result of "Gate the risky AI actions", "Ask in Slack".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Act on the decision
    summary: >-
      Approved runs the action. Rejected archives it with the reason, tells the originating workflow to
      stop, and posts the reasoning to the governance channel. A timeout behaves like a rejection and
      is logged as one.
    builds: workflow
    description: >-
      Branch step on the approval decision: APPROVED to execute action (webhook back to originator workflow
      with 'go ahead'); REJECTED to archive with rejection reason + notify originator workflow to abort
      + post reasoning to #ai-governance for learning; TIMEOUT to same as rejected, with timeout reason
      logged. Use the result of "Gate the risky AI actions", "Wait for an answer".
    dependsOn:
      - s1
      - s5
  - id: s7
    title: Tell the workflow to proceed
    summary: >-
      A webhook back to the workflow that asked, carrying the approver, the timestamp and any comment,
      all written to the audit trail so every AI action is traceable.
    builds: workflow
    description: >-
      Configure webhook call back to the originator workflow to proceed with the queued action. Include
      approval metadata (approver name, timestamp, any approver comments). Log to audit trail, every AI
      action that went through approval is fully traceable for compliance + later review. Use the result
      of "Gate the risky AI actions", "Act on the decision".
    dependsOn:
      - s1
      - s6
  - id: s8
    title: Log what humans reject
    summary: >-
      Every rejection and its reason goes into a structured log, which over time shows which AI behaviours
      need tighter prompts or guardrails.
    builds: workflow
    description: >-
      On rejected branch: write the rejection to a structured learning log: which AI suggestions are humans
      rejecting, what's the rejection reason. Over time this reveals which AI behaviors need prompt tuning
      or guardrails. The reject log is the feedback loop that improves the underlying AI workflows. Use
      the result of "Gate the risky AI actions", "Act on the decision".
    dependsOn:
      - s1
      - s6
  - id: s9
    title: Publish and watch the queue
    summary: >-
      Validated and published, with approvals per week, the approval rate against an 80% target, the median
      time to a decision inside business hours against 30 minutes, and the timeout rate, which points
      at the wrong approver or a dead channel.
    builds: workflow
    description: >-
      Validate and publish. Monitor: approval volume per week, approval-rate (target: 80%+; below 60%
      suggests upstream AI workflows need tuning), median time-to-decision (target: under 30min during
      business hours), timeout rate (high = wrong approvers or low-engagement channel). The dashboard
      for responsible AI governance. Use the result of "Gate the risky AI actions", "Tell the workflow
      to proceed", "Log what humans reject".
    dependsOn:
      - s1
      - s7
      - s8
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s8
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Human approval for AI actions

Holds the riskier things an AI workflow wants to do, such as a mass update or a send to a big account, for a yes or no in Slack.

## Steps

1. **Gate the risky AI actions** (builds workflow)

   Sits in front of the high stakes actions an AI workflow wants to take. You set what needs approval: an ARR cutoff, a segment size, the kind of action, or how confident the AI was.

2. **Let other workflows queue one** (builds workflow)

   A webhook other workflows call to submit an action. It carries the kind of action, a one line summary, the full payload, which workflow asked, and why this one needs approval.

3. **Send it to the right approver** (builds workflow)

   Emails go to marketing, record updates to RevOps, lead routing to a sales manager, and other decisions by type. The wrong approver is what turns this into a bottleneck.

4. **Ask in Slack** (builds workflow)

   An interactive message in the approver's channel with the summary, the workflow that asked, why it needs approval, a preview such as the subject line and first 200 characters, and approve or reject buttons.

5. **Wait for an answer** (builds workflow)

   Execution pauses until someone responds, four hours by default. Shorten it for a big send, stretch it for routine updates. Silence counts as a rejection and posts a notice.

6. **Act on the decision** (builds workflow)

   Approved runs the action. Rejected archives it with the reason, tells the originating workflow to stop, and posts the reasoning to the governance channel. A timeout behaves like a rejection and is logged as one.

7. **Tell the workflow to proceed** (builds workflow)

   A webhook back to the workflow that asked, carrying the approver, the timestamp and any comment, all written to the audit trail so every AI action is traceable.

8. **Log what humans reject** (builds workflow)

   Every rejection and its reason goes into a structured log, which over time shows which AI behaviours need tighter prompts or guardrails.

9. **Publish and watch the queue** (builds workflow)

   Validated and published, with approvals per week, the approval rate against an 80% target, the median time to a decision inside business hours against 30 minutes, and the timeout rate, which points at the wrong approver or a dead channel.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new workflow, from step 1 "Gate the risky AI actions"
- A new workflow, from step 2 "Let other workflows queue one"
- A new workflow, from step 3 "Send it to the right approver"
- A new workflow, from step 4 "Ask in Slack"
- A new workflow, from step 5 "Wait for an answer"
- A new workflow, from step 6 "Act on the decision"
- A new workflow, from step 7 "Tell the workflow to proceed"
- A new workflow, from step 8 "Log what humans reject"
- A new workflow, from step 9 "Publish and watch the queue"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
