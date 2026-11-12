---
frontmatter_id: ai-action-approval-queue
slash_command: /ai-action-approval-queue
description: Holds riskier actions an AI workflow wants to take, such as a mass update or a send to a big account, in an approval gate and queue for human review before execution.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Holds risky AI-generated actions, such as mass updates or sends to large accounts, for human approval in Slack
    before they run, with timeouts that default to rejection.
  parameters:
  - name: arr_threshold
    type: number
    label: ARR cutoff that triggers approval
    default: 100000
    required: false
  - name: segment_size_threshold
    type: number
    label: Segment size that triggers approval
    default: 5000
    required: false
  - name: confidence_threshold
    type: number
    label: AI confidence below which approval is required (0-1)
    default: 0.7
    required: false
  - name: approval_timeout
    type: duration
    label: Time to wait for an approval decision before auto-rejecting
    default: 4 h
    required: false
  - name: reject_channel
    type: string
    label: Slack channel for rejection reasoning and learning notes
    default: '#ai-governance'
    required: false
  - name: dashboard_target_approval_rate
    type: number
    label: Target approval rate (%)
    default: 80
    required: false
  - name: dashboard_warning_approval_rate
    type: number
    label: Approval rate below which upstream AI workflows need tuning (%)
    default: 60
    required: false
  - name: target_decision_time
    type: duration
    label: Target median time to decision
    default: 30 min
    required: false
  requirements:
  - slot: ai_action_event
    kind: event
    meaning: An AI workflow requested a high-stakes action that needs human approval
    properties:
    - name: action_type
      type: string
      meaning: 'Type of action: send_email, update_records, route_lead or make_decision'
      optional: false
    - name: action_summary
      type: string
      meaning: One-line description of the action
      optional: false
    - name: full_payload
      type: text
      meaning: The actual action data
      optional: false
    - name: requesting_workflow
      type: string
      meaning: Workflow that requested the action
      optional: false
    - name: threshold_reason
      type: string
      meaning: 'Why approval is needed: high-ARR, large-segment or low-confidence'
      optional: false
  - slot: marketing_lead_approver
    kind: segment
    meaning: Marketing lead users who approve email sends
  - slot: revops_approver
    kind: segment
    meaning: RevOps users who approve record updates
  - slot: sales_manager_approver
    kind: segment
    meaning: Sales managers who approve lead routing
  - slot: decision_approver
    kind: segment
    meaning: Approvers for AI decisions, varying by decision type
  - slot: approval_slack
    kind: integration
    meaning: Slack workspace connection used to post approval requests and notices
    channel: slack
  - slot: audit_log
    kind: destination
    meaning: Destination for the approval audit trail and rejection learning log
    channel: email
  - slot: originator_webhook
    kind: integration
    meaning: Webhook endpoint for calling back the requesting workflow
    channel: email
  - slot: governance_dashboard
    kind: destination
    meaning: Dashboard for tracking approval volume, approval rate, decision time and timeouts
    channel: email
  steps:
  - id: s1
    builds: automation
    uses:
    - ai_action_event
    - arr_threshold
    - segment_size_threshold
    - confidence_threshold
    instruction: Create a workflow 'AI action approval queue' that intercepts high-stakes AI-generated actions and requires
      human approval before execution. Trigger it when a requested action has an ARR at or above {arr_threshold}, a segment
      size at or above {segment_size_threshold}, an AI confidence below {confidence_threshold}, or an action type of update_records,
      send_email, route_lead or make_decision that is flagged as high-stakes. Keep the threshold values configurable.
  - id: s2
    builds: webhook
    uses:
    - ai_action_event
    - originator_webhook
    - s1
    instruction: Configure a webhook trigger that other workflows call to queue an action for approval, using the result of
      "Gate the risky AI actions". Accept the payload fields {ai_action_event.action_type} (send_email, update_records, route_lead
      or make_decision), {ai_action_event.action_summary} (one-line description), {ai_action_event.full_payload} (the actual
      action data), {ai_action_event.requesting_workflow} (originator) and {ai_action_event.threshold_reason} (high-ARR, large-segment
      or low-confidence).
  - id: s3
    builds: automation
    uses:
    - ai_action_event
    - marketing_lead_approver
    - revops_approver
    - sales_manager_approver
    - decision_approver
    - s1
    - s2
    instruction: 'Multi-split on {ai_action_event.action_type} using the results of "Gate the risky AI actions" and "Let other
      workflows queue one": send_email routes to {marketing_lead_approver}; update_records routes to {revops_approver}; route_lead
      routes to {sales_manager_approver}; make_decision routes to {decision_approver} based on decision type. Each route selects
      the matching approver Slack channel. Wrong approver routing creates bottlenecks, so verify each route is mapped.'
  - id: s4
    builds: slack
    uses:
    - approval_slack
    - ai_action_event
    - s1
    - s3
    instruction: Post an interactive approval message to the approver channel or user chosen in "Send it to the right approver",
      using {approval_slack}. Include {ai_action_event.action_summary}, {ai_action_event.requesting_workflow}, {ai_action_event.threshold_reason}
      and an action preview (for send_email, the subject plus the first 200 characters of the body). Provide Approve and Reject
      buttons, or accept thread replies of 'approve' or 'reject'. Tag the specific approver.
  - id: s5
    builds: automation
    uses:
    - approval_timeout
    - approval_slack
    - reject_channel
    - s1
    - s4
    instruction: Wait until an approval response is received for the message posted in "Ask in Slack", pausing execution for
      up to {approval_timeout}. On timeout, record the decision as rejected with reason 'timeout' and post an 'auto-rejected
      after timeout' notice to {reject_channel} using {approval_slack}. For high-ARR sends a shorter window such as 1 hour
      may be set; routine updates may allow 24 hours.
  - id: s6
    builds: automation
    uses:
    - originator_webhook
    - reject_channel
    - s1
    - s5
    instruction: Branch on the decision from "Wait for an answer". If APPROVED, call {originator_webhook} to tell the originator
      to go ahead. If REJECTED, archive the action with its rejection reason, notify the originator to abort, and post the
      reasoning to {reject_channel}. If TIMEOUT, follow the same path as REJECTED and log the timeout reason.
  - id: s7
    builds: webhook
    uses:
    - originator_webhook
    - audit_log
    - s1
    - s6
    instruction: 'Call the originator workflow webhook {originator_webhook} to proceed with the queued action, as set in "Act
      on the decision". Include approval metadata: approver name, timestamp and any approver comments. Write every AI action
      that went through approval to {audit_log} so each one is traceable for compliance and later review.'
  - id: s8
    builds: report
    uses:
    - audit_log
    - s1
    - s6
    instruction: On the rejected branch of "Act on the decision", write the rejection to a structured learning log in {audit_log}
      recording which AI suggestions humans reject and the rejection reason. Use this log to identify AI behaviors that need
      prompt tuning or guardrails.
  - id: s9
    builds: dashboard
    uses:
    - governance_dashboard
    - dashboard_target_approval_rate
    - dashboard_warning_approval_rate
    - target_decision_time
    - s1
    - s7
    - s8
    instruction: Validate and publish the workflow. Build a responsible AI governance dashboard on {governance_dashboard}
      tracking weekly approval volume, approval rate (target {dashboard_target_approval_rate}% or more; below {dashboard_warning_approval_rate}%
      suggests upstream AI workflows need tuning), median time to decision (target under {target_decision_time} during business
      hours), and timeout rate (a high rate suggests wrong approvers or a low-engagement channel). Use the results of "Gate
      the risky AI actions", "Tell the workflow to proceed" and "Log what humans reject".
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
