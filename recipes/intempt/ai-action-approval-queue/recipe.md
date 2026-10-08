---
description: Holds riskier actions an AI workflow wants to take, such as a mass update or a send to a big account, in an approval gate and queue for human review before execution.
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
  - finance
---

# Human approval for AI actions

Slash command: /ai-action-approval-queue

## Step 1: Gate the risky AI actions

Create a workflow 'AI action approval queue' that intercepts high-stakes AI-generated actions and requires human approval before execution. Goal: capture AI's speed while keeping human judgment on the consequential decisions. Configurable threshold for what triggers approval (ARR cutoff, segment size, action type, AI confidence).

## Step 2: Let other workflows queue one

Configure webhook trigger that other workflows call when they want to queue an action for approval. Payload schema: action_type (send_email / update_records / route_lead / make_decision), action_summary (one-line description), full_payload (the actual action data), requesting_workflow (originator), threshold_reason (why this needs approval: high-ARR / large-segment / low-confidence). Use the result of "Gate the risky AI actions".

## Step 3: Send it to the right approver

Multi-split by action_type: send_email to marketing lead approval; update_records to RevOps approval; route_lead to sales manager approval; make_decision to varies by decision type. Each routes to the right approver Slack channel. The approver matters: wrong approver leads to bottlenecks. Use the result of "Gate the risky AI actions", "Let other workflows queue one".

## Step 4: Ask in Slack

Configure Slack step that posts an interactive approval message to the right channel/user. Message includes: action summary, originator workflow, threshold reason, action preview (e.g. for email: subject + first 200 chars), and Approve/Reject buttons (or Slack thread-reply 'approve'/'reject'). Tag the specific approver. Use the result of "Gate the risky AI actions", "Send it to the right approver".

## Step 5: Wait for an answer

Configure wait-until step that pauses workflow execution until approval response received. Timeout: 4 hours (configurable: high-ARR sends might warrant 1hr, routine updates might allow 24hrs). On timeout: default-reject (safer than default-approve) + post 'auto-rejected after timeout' notification. Use the result of "Gate the risky AI actions", "Ask in Slack".

## Step 6: Act on the decision

Branch step on the approval decision: APPROVED to execute action (webhook back to originator workflow with 'go ahead'); REJECTED to archive with rejection reason + notify originator workflow to abort + post reasoning to #ai-governance for learning; TIMEOUT to same as rejected, with timeout reason logged. Use the result of "Gate the risky AI actions", "Wait for an answer".

## Step 7: Tell the workflow to proceed

Configure webhook call back to the originator workflow to proceed with the queued action. Include approval metadata (approver name, timestamp, any approver comments). Log to audit trail, every AI action that went through approval is fully traceable for compliance + later review. Use the result of "Gate the risky AI actions", "Act on the decision".

## Step 8: Log what humans reject

On rejected branch: write the rejection to a structured learning log: which AI suggestions are humans rejecting, what's the rejection reason. Over time this reveals which AI behaviors need prompt tuning or guardrails. The reject log is the feedback loop that improves the underlying AI workflows. Use the result of "Gate the risky AI actions", "Act on the decision".

## Step 9: Publish and watch the queue

Validate and publish. Monitor: approval volume per week, approval-rate (target: 80%+; below 60% suggests upstream AI workflows need tuning), median time-to-decision (target: under 30min during business hours), timeout rate (high = wrong approvers or low-engagement channel). The dashboard for responsible AI governance. Use the result of "Gate the risky AI actions", "Tell the workflow to proceed", "Log what humans reject".
