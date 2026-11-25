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
visibility: draft
rejected: The recipe is an approval gate other workflows call by webhook and approve with interactive Slack buttons; Blu has
  no webhook trigger, callback or interactive approval.
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
portable:
  summary: Holds risky AI-generated actions, such as mass updates or sends to large accounts, for human approval before they
    run.
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
      send_email, route_lead or make_decision that is flagged as high-stakes. Keep the threshold values configurable. Take
      every count from the result of the step that built the list; if it is not there, name the segment or report instead.
      A draft never contains a placeholder in square brackets.
  - id: s2
    builds: webhook
    uses:
    - ai_action_event
    - originator_webhook
    - s1
    dependsOn:
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
    dependsOn:
    - s1
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
    dependsOn:
    - s1
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
    dependsOn:
    - s1
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
    dependsOn:
    - s1
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
    dependsOn:
    - s1
    instruction: 'Call the originator workflow webhook {originator_webhook} to proceed with the queued action, as set in "Act
      on the decision". Include approval metadata: approver name, timestamp and any approver comments. Write every AI action
      that went through approval to {audit_log} so each one is traceable for compliance and later review.'
  - id: s8
    builds: report
    uses:
    - audit_log
    - s1
    - s6
    dependsOn:
    - s1
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
    dependsOn:
    - s1
    instruction: Validate and publish the workflow. Build a responsible AI governance dashboard on {governance_dashboard}
      tracking weekly approval volume, approval rate (target {dashboard_target_approval_rate}% or more; below {dashboard_warning_approval_rate}%
      suggests upstream AI workflows need tuning), median time to decision (target under {target_decision_time} during business
      hours), and timeout rate (a high rate suggests wrong approvers or a low-engagement channel). Use the results of "Gate
      the risky AI actions", "Tell the workflow to proceed" and "Log what humans reject".
---

# Human approval for AI actions

Slash command: /ai-action-approval-queue

## Step 1: Gate the risky AI actions

Create a workflow 'AI action approval queue' that intercepts high-stakes AI-generated actions and requires human approval before execution. Trigger it when a requested action has an ARR at or above 100000, a segment size at or above 5000, an AI confidence below 0.7, or an action type of update_records, send_email, route_lead or make_decision that is flagged as high-stakes. Keep the threshold values configurable. Take every count from the result of the step that built the list; if it is not there, name the segment or report instead. A draft never contains a placeholder in square brackets.

## Step 2: Let other workflows queue one

Configure a webhook trigger that other workflows call to queue an action for approval, using the result of "Gate the risky AI actions". Accept the payload fields action type (send_email, update_records, route_lead or make_decision), action summary (one-line description), full payload (the actual action data), requesting workflow (originator) and threshold reason (high-ARR, large-segment or low-confidence).

## Step 3: Send it to the right approver

Multi-split on action type using the results of "Gate the risky AI actions" and "Let other workflows queue one": send_email routes to marketing lead approver; update_records routes to revops approver; route_lead routes to sales manager approver; make_decision routes to decision approver based on decision type. Each route selects the matching approver Slack channel. Wrong approver routing creates bottlenecks, so verify each route is mapped.

## Step 4: Ask in Slack

Post an interactive approval message to the approver channel or user chosen in "Send it to the right approver", using approval slack. Include action summary, requesting workflow, threshold reason and an action preview (for send_email, the subject plus the first 200 characters of the body). Provide Approve and Reject buttons, or accept thread replies of 'approve' or 'reject'. Tag the specific approver.

## Step 5: Wait for an answer

Wait until an approval response is received for the message posted in "Ask in Slack", pausing execution for up to 4 h. On timeout, record the decision as rejected with reason 'timeout' and post an 'auto-rejected after timeout' notice to #ai-governance using approval slack. For high-ARR sends a shorter window such as 1 hour may be set; routine updates may allow 24 hours.

## Step 6: Act on the decision

Branch on the decision from "Wait for an answer". If APPROVED, call originator webhook to tell the originator to go ahead. If REJECTED, archive the action with its rejection reason, notify the originator to abort, and post the reasoning to #ai-governance. If TIMEOUT, follow the same path as REJECTED and log the timeout reason.

## Step 7: Tell the workflow to proceed

Call the originator workflow webhook originator webhook to proceed with the queued action, as set in "Act on the decision". Include approval metadata: approver name, timestamp and any approver comments. Write every AI action that went through approval to audit log so each one is traceable for compliance and later review.

## Step 8: Log what humans reject

On the rejected branch of "Act on the decision", write the rejection to a structured learning log in audit log recording which AI suggestions humans reject and the rejection reason. Use this log to identify AI behaviors that need prompt tuning or guardrails.

## Step 9: Publish and watch the queue

Validate and publish the workflow. Build a responsible AI governance dashboard on governance dashboard tracking weekly approval volume, approval rate (target 80% or more; below 60% suggests upstream AI workflows need tuning), median time to decision (target under 30 min during business hours), and timeout rate (a high rate suggests wrong approvers or a low-engagement channel). Use the results of "Gate the risky AI actions", "Tell the workflow to proceed" and "Log what humans reject".
