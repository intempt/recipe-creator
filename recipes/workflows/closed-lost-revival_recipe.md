---
name: closed-lost-revival
description: 'Use when a user mentions "closed lost revival", "deal revival workflow", "cold deal reactivation", or asks for related help. Revive closed-lost deals 90 days after loss with a fresh re-evaluation outreach — context has likely changed (new initiatives, leadership, budget cycle). Typical revival rates: 5-10%, with low cost of outreach.'
arguments: []
intempt:
  id: closed-lost-revival
  version: 1.0.0
  slashCommand: /closed-lost-revival
  group: Workflows
  shortDescription: "Build a 'Closed-lost revival candidates' segment of deals lost 90-180 days ago and send a 2-touch revival email sequence."
  availability: coming-soon
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [closed-lost-revival, pipeline-resurrection]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: deal_lost, severity: blocking }
  invokesCommands:
    - create_segment
    - create_email_content
    - create_workflow
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Identify Revival Candidates
      command: create_segment
      produces: segment
      bindsAs: segment
      description: 'Build a segment ''Closed-lost revival candidates'' capturing deals where deal_lost event fired 90-180 days ago AND lost_reason is NOT ''wrong-fit'' or ''competitor-won-firm-commitment'' (those won''t revive). Includes deals lost to: timing, budget, no-decision, internal-resourcing, postponed. Excludes accounts that have entered closed-lost more than twice (3-strikes rule: stop pestering).'
      prompt: 'Build a segment ''Closed-lost revival candidates'' capturing deals where deal_lost event fired 90-180 days ago AND lost_reason is NOT ''wrong-fit'' or ''competitor-won-firm-commitment'' (those won''t revive). Includes deals lost to: timing, budget, no-decision, internal-resourcing, postponed. Excludes accounts that have entered closed-lost more than twice (3-strikes rule: stop pestering).'
    - step: 2
      title: Build Revival Outreach Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: 'Generate 2-touch revival email content. Touch 1 (Day 0): ''It''s been a few months — wanted to check in. Last time we talked, [original_lost_reason]. Has anything changed?'' Reference specific prior conversation context. Soft re-open, not a sales pitch. Touch 2 (Day 14, if no reply): share a relevant product update or customer story from a similar account that addresses their original objection. Send-from: the original AE owner. Tone: warm, low-pressure, acknowledging the prior ''no''.'
      prompt: 'Generate 2-touch revival email content. Touch 1 (Day 0): ''It''s been a few months — wanted to check in. Last time we talked, [original_lost_reason]. Has anything changed?'' Reference specific prior conversation context. Soft re-open, not a sales pitch. Touch 2 (Day 14, if no reply): share a relevant product update or customer story from a similar account that addresses their original objection. Send-from: the original AE owner. Tone: warm, low-pressure, acknowledging the prior ''no''.'
    - step: 3
      title: Build Revival Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      - asset
      description: 'Create a workflow firing daily for newly-eligible revival candidates. Step sequence: (1) refresh account enrichment (champion still there? new leadership? funding announced? product launched?); (2) IF significant change detected (new champion-role hire, funding round, etc.) — create urgent AE task to manually reach out; ELSE trigger the standard 2-touch revival journey. Track responses and any new meeting bookings as revival_signal events on the original closed-lost deal record.'
      prompt: 'Create a workflow firing daily for newly-eligible revival candidates. Step sequence: (1) refresh account enrichment (champion still there? new leadership? funding announced? product launched?); (2) IF significant change detected (new champion-role hire, funding round, etc.) — create urgent AE task to manually reach out; ELSE trigger the standard 2-touch revival journey. Track responses and any new meeting bookings as revival_signal events on the original closed-lost deal record.'
    - step: 4
      title: Build Revival Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      - workflow
      description: 'Build a 2-touch journey triggered by the revival workflow. Touch 1 at Day 0, Touch 2 at Day 14 (skipped if user replies or books meeting). Audience: the original deal''s primary contact. Exit on: meeting_scheduled (revival success — open new deal), email_replied (warm handoff to AE), unsubscribe, or 30-day max duration.'
      prompt: 'Build a 2-touch journey triggered by the revival workflow. Touch 1 at Day 0, Touch 2 at Day 14 (skipped if user replies or books meeting). Audience: the original deal''s primary contact. Exit on: meeting_scheduled (revival success — open new deal), email_replied (warm handoff to AE), unsubscribe, or 30-day max duration.'
    - step: 5
      title: Build Revival Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - workflow
      - journey
      description: 'Compose a revival performance dashboard: closed-lost deals entering revival per month, reply rate to revival outreach, meeting-booked rate from revival, revived-deal-to-win rate (final conversion), and ARR resurrected this quarter from revival pipeline. Break down by original lost_reason — which lost-reasons most often turn into revivals (informs sales coaching on when ''no'' was actually ''not yet'').'
      prompt: 'Compose a revival performance dashboard: closed-lost deals entering revival per month, reply rate to revival outreach, meeting-booked rate from revival, revived-deal-to-win rate (final conversion), and ARR resurrected this quarter from revival pipeline. Break down by original lost_reason — which lost-reasons most often turn into revivals (informs sales coaching on when ''no'' was actually ''not yet'').'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Closed Lost Revival

## Procedure

1. **Identify Revival Candidates** [`create_segment`] — Build a segment 'Closed-lost revival candidates' capturing deals where deal_lost event fired 90-180 days ago AND lost_reason is NOT 'wrong-fit' or 'competitor-won-firm-commitment' (those won't revive). Includes deals lost to: timing, budget, no-decision, internal-resourcing, postponed. Excludes accounts that have entered closed-lost more than twice (3-strikes rule: stop pestering). → produces: segment
2. **Build Revival Outreach Content** [`create_email_content`] — Generate 2-touch revival email content. Touch 1 (Day 0): 'It's been a few months — wanted to check in. Last time we talked, [original_lost_reason]. Has anything changed?' Reference specific prior conversation context. Soft re-open, not a sales pitch. Touch 2 (Day 14, if no reply): share a relevant product update or customer story from a similar account that addresses their original objection. Send-from: the original AE owner. Tone: warm, low-pressure, acknowledging the prior 'no'. → produces: asset
3. **Build Revival Workflow** [`create_workflow`] — Create a workflow firing daily for newly-eligible revival candidates. Step sequence: (1) refresh account enrichment (champion still there? new leadership? funding announced? product launched?); (2) IF significant change detected (new champion-role hire, funding round, etc.) — create urgent AE task to manually reach out; ELSE trigger the standard 2-touch revival journey. Track responses and any new meeting bookings as revival_signal events on the original closed-lost deal record. → produces: workflow
4. **Build Revival Journey** [`create_journey`] — Build a 2-touch journey triggered by the revival workflow. Touch 1 at Day 0, Touch 2 at Day 14 (skipped if user replies or books meeting). Audience: the original deal's primary contact. Exit on: meeting_scheduled (revival success — open new deal), email_replied (warm handoff to AE), unsubscribe, or 30-day max duration. → produces: journey
5. **Build Revival Performance Dashboard** [`create_dashboard`] — Compose a revival performance dashboard: closed-lost deals entering revival per month, reply rate to revival outreach, meeting-booked rate from revival, revived-deal-to-win rate (final conversion), and ARR resurrected this quarter from revival pipeline. Break down by original lost_reason — which lost-reasons most often turn into revivals (informs sales coaching on when 'no' was actually 'not yet'). → produces: dashboard
