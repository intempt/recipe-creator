---
name: closed-lost-revival
description: 'Use when a user mentions "closed lost revival", "deal revival workflow", "cold deal reactivation", or asks for related help. Revive closed-lost deals 90 days after loss with a fresh re-evaluation outreach: context has likely changed (new initiatives, leadership, budget cycle). Typical revival rates: 5-10%, with low cost of outreach.'
arguments: []
intempt:
  id: closed-lost-revival
  title: "Closed lost revival"
  version: 1.0.0
  slashCommand: /closed-lost-revival
  group: Workflows
  shortDescription: "Goes back to deals lost 90 days ago, checks what has changed at the account, and reopens the conversation where the reason for losing may have expired."
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
      title: "Find losses worth revisiting"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Deals lost between 90 and 180 days ago where the reason was timing, budget, no decision, resourcing or a postponement. Wrong fit and a firm commitment to a competitor are left out, as is any account already lost three times."
      prompt: 'Build a segment ''Closed-lost revival candidates'' capturing deals where deal_lost event fired 90-180 days ago AND lost_reason is NOT ''wrong-fit'' or ''competitor-won-firm-commitment'' (those won''t revive). Includes deals lost to: timing, budget, no-decision, internal-resourcing, postponed. Excludes accounts that have entered closed-lost more than twice (3-strikes rule: stop pestering).'
    - step: 2
      title: "Write two revival emails"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: "Day 0 refers to the actual reason they gave last time and asks whether anything has changed. Day 14 shares a product update or a customer story that answers that original objection. From the AE who owned it, warm and low pressure, acknowledging the earlier no."
      prompt: 'Generate 2-touch revival email content. Touch 1 (Day 0): ''It''s been a few months: wanted to check in. Last time we talked, [original_lost_reason]. Has anything changed?'' Reference specific prior conversation context. Soft re-open, not a sales pitch. Touch 2 (Day 14, if no reply): share a relevant product update or customer story from a similar account that addresses their original objection. Send-from: the original AE owner. Tone: warm, low-pressure, acknowledging the prior ''no''.'
    - step: 3
      title: "Check what changed first"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - segment
      - asset
      description: "Daily, for each newly eligible deal, it refreshes the account: is the champion still there, is there new leadership, was there funding, did they launch something. A significant change raises an urgent AE task to reach out personally. Everything else goes into the two email sequence, and any response is logged on the original deal."
      prompt: 'Create a workflow firing daily for newly-eligible revival candidates. Step sequence: (1) refresh account enrichment (champion still there? new leadership? funding announced? product launched?); (2) IF significant change detected (new champion-role hire, funding round, etc.): create urgent AE task to manually reach out; ELSE trigger the standard 2-touch revival journey. Track responses and any new meeting bookings as revival_signal events on the original closed-lost deal record.'
    - step: 4
      title: "Send at day 0 and day 14"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      - workflow
      description: "Both go to the original contact, with the second skipped if they reply or book. It ends on a booked meeting, which opens a new deal, on a reply, which goes to the AE, on unsubscribe, or after 30 days."
      prompt: 'Build a 2-touch journey triggered by the revival workflow. Touch 1 at Day 0, Touch 2 at Day 14 (skipped if user replies or books meeting). Audience: the original deal''s primary contact. Exit on: meeting_scheduled (revival success: open new deal), email_replied (warm handoff to AE), unsubscribe, or 30-day max duration.'
    - step: 5
      title: "See what comes back to life"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - workflow
      - journey
      description: "Deals entering revival each month, the reply rate, how many meetings come out of it, how many revived deals are won, and the ARR recovered this quarter, split by the original reason for losing."
      prompt: 'Compose a revival performance dashboard: closed-lost deals entering revival per month, reply rate to revival outreach, meeting-booked rate from revival, revived-deal-to-win rate (final conversion), and ARR resurrected this quarter from revival pipeline. Break down by original lost_reason: which lost-reasons most often turn into revivals (informs sales coaching on when ''no'' was actually ''not yet'').'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Closed lost revival

Goes back to deals lost 90 days ago, checks what has changed at the account, and reopens the conversation where the reason for losing may have expired.

## Before you run it

- Send the `deal_lost` event

## What it does

1. **Find losses worth revisiting** (`create_segment`)

   Deals lost between 90 and 180 days ago where the reason was timing, budget, no decision, resourcing or a postponement. Wrong fit and a firm commitment to a competitor are left out, as is any account already lost three times.

2. **Write two revival emails** (`create_email_content`)

   Day 0 refers to the actual reason they gave last time and asks whether anything has changed. Day 14 shares a product update or a customer story that answers that original objection. From the AE who owned it, warm and low pressure, acknowledging the earlier no.

3. **Check what changed first** (`create_workflow`)

   Daily, for each newly eligible deal, it refreshes the account: is the champion still there, is there new leadership, was there funding, did they launch something. A significant change raises an urgent AE task to reach out personally. Everything else goes into the two email sequence, and any response is logged on the original deal.

4. **Send at day 0 and day 14** (`create_journey`)

   Both go to the original contact, with the second skipped if they reply or book. It ends on a booked meeting, which opens a new deal, on a reply, which goes to the AE, on unsubscribe, or after 30 days.

5. **See what comes back to life** (`create_dashboard`)

   Deals entering revival each month, the reply rate, how many meetings come out of it, how many revived deals are won, and the ARR recovered this quarter, split by the original reason for losing.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **workflow** (workflow): Workflow produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
