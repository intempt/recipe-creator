---
frontmatter_id: closed-lost-revival
slash_command: /closed-lost-revival
description: Goes back to deals lost 90 days ago, checks what has changed at the account, and reopens the conversation where the reason for losing may have expired.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Revisits deals lost 90 to 180 days ago, checks what changed at the account, and sends a soft two-touch revival
    sequence so the conversation can reopen when the original objection may have expired.
  parameters:
  - name: lookback_start
    type: duration
    label: Earliest days since loss
    default: 90 d
    required: false
  - name: lookback_end
    type: duration
    label: Latest days since loss
    default: 180 d
    required: false
  - name: max_closed_lost_count
    type: number
    label: Maximum closed-lost count before excluding account
    default: 2
    required: false
  - name: followup_delay
    type: duration
    label: Delay before second touch
    default: 14 d
    required: false
  - name: journey_max_duration
    type: duration
    label: Maximum journey duration
    default: 30 d
    required: false
  - name: tone
    type: enum
    label: Email tone
    default: warm
    required: false
    options:
    - warm
    - neutral
    - formal
  requirements:
  - slot: deal_lost_event
    kind: event
    meaning: A deal was marked closed lost
    properties:
    - name: lost_reason
      type: string
      meaning: Reason the deal was lost
      optional: false
    - name: occurred_at
      type: date
      meaning: When the deal was lost
      optional: false
  - slot: account_enrichment
    kind: integration
    meaning: A data enrichment source that refreshes account and contact details such as champion, leadership, funding and
      product launches
    channel: hubspot
  - slot: ae_owner
    kind: attribute
    meaning: The account executive who owned the original deal
  - slot: primary_contact
    kind: attribute
    meaning: The primary contact on the original deal
  - slot: revival_signal_event
    kind: event
    meaning: A record of a revival response such as a reply or booked meeting on the closed-lost deal
  steps:
  - id: s1
    builds: segment
    uses:
    - deal_lost_event
    - lookback_start
    - lookback_end
    - max_closed_lost_count
    instruction: Build the segment 'Closed-lost revival candidates' with deals where {deal_lost_event} fired between {lookback_start}
      and {lookback_end} ago AND {deal_lost_event.lost_reason} is not 'wrong-fit' or 'competitor-won-firm-commitment'. Include
      losses for timing, budget, no-decision, internal-resourcing and postponed. Exclude accounts that have entered closed-lost
      more than {max_closed_lost_count} times.
  - id: s2
    builds: email
    uses:
    - s1
    - tone
    - ae_owner
    instruction: 'Generate a two-touch revival email sequence for the contacts in ''Find losses worth revisiting''. Touch
      1 (day 0) opens: ''It''s been a few months: wanted to check in. Last time we talked, {deal_lost_event.lost_reason}.
      Has anything changed?'' Reference specific prior conversation context. Keep it a soft re-open, not a sales pitch. Touch
      2 (day 14, if no reply) shares a relevant product update or customer story from a similar account that addresses the
      original objection. Send from {ae_owner}. Use a {tone} tone that acknowledges the prior no.'
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - account_enrichment
    - ae_owner
    - revival_signal_event
    instruction: 'Create a daily workflow for newly eligible contacts from ''Find losses worth revisiting''. Step 1: refresh
      {account_enrichment} data to check whether the champion is still in role, whether there is new leadership, a funding
      announcement, or a product launch. Step 2: if a significant change is detected (such as a new champion-role hire or
      a funding round), create an urgent task for {ae_owner} to reach out manually. Otherwise, enroll the contact in the ''Send
      at day 0 and day 14'' journey. Log responses and new meeting bookings as {revival_signal_event} records on the original
      closed-lost deal.'
  - id: s4
    builds: automation
    uses:
    - s1
    - s2
    - s3
    - primary_contact
    - tone
    - followup_delay
    - journey_max_duration
    instruction: 'Build a two-touch journey triggered by the revival workflow in ''Check what changed first''. Audience: {primary_contact}
      on the original deal. Touch 1 sends on day 0 using ''Write two revival emails''. Touch 2 sends after {followup_delay},
      skipped if the contact replied or booked a meeting. Exit on: meeting scheduled (open a new deal), reply received (warm
      handoff to {ae_owner}), unsubscribe, or after {journey_max_duration}.'
  - id: s5
    builds: dashboard
    uses:
    - s1
    - s2
    - s3
    - s4
    - revival_signal_event
    instruction: 'Build a revival performance dashboard showing: closed-lost deals entering revival per month; reply rate
      to revival outreach; meeting-booked rate from revival; revived-deal-to-win rate; and ARR resurrected this quarter from
      revival pipeline. Break every metric down by original {deal_lost_event.lost_reason} to show which lost reasons most
      often turn into revivals.'
---

# Closed lost revival

Slash command: /closed-lost-revival

## Step 1: Find losses worth revisiting

Build a segment 'Closed-lost revival candidates' capturing deals where Deal lost event fired 90-180 days ago AND lost_reason is NOT 'wrong-fit' or 'competitor-won-firm-commitment' (those won't revive). Includes deals lost to: timing, budget, no-decision, internal-resourcing, postponed. Excludes accounts that have entered closed-lost more than twice (3-strikes rule: stop pestering).

## Step 2: Write two revival emails

Generate 2-touch revival email content. Touch 1 (Day 0): 'It's been a few months: wanted to check in. Last time we talked, [original_lost_reason]. Has anything changed?' Reference specific prior conversation context. Soft re-open, not a sales pitch. Touch 2 (Day 14, if no reply): share a relevant product update or customer story from a similar account that addresses their original objection. Send-from: the original AE owner. Tone: warm, low-pressure, acknowledging the prior 'no'. Use the result of "Find losses worth revisiting".

## Step 3: Check what changed first

Create a workflow firing daily for newly-eligible revival candidates. Step sequence: (1) refresh account enrichment (champion still there? new leadership? funding announced? product launched?); (2) IF significant change detected (new champion-role hire, funding round, etc.): create urgent AE task to manually reach out; ELSE trigger the standard 2-touch revival journey. Track responses and any new meeting bookings as revival_signal events on the original closed-lost deal record. Use the result of "Find losses worth revisiting", "Write two revival emails".

## Step 4: Send at day 0 and day 14

Build a 2-touch journey triggered by the revival workflow. Touch 1 at Day 0, Touch 2 at Day 14 (skipped if user replies or books meeting). Audience: the original deal's primary contact. Exit on: Meeting scheduled (revival success: open new deal), email_replied (warm handoff to AE), unsubscribe, or 30-day max duration. Use the result of "Find losses worth revisiting", "Write two revival emails", "Check what changed first".

## Step 5: See what comes back to life

Compose a revival performance dashboard: closed-lost deals entering revival per month, reply rate to revival outreach, meeting-booked rate from revival, revived-deal-to-win rate (final conversion), and ARR resurrected this quarter from revival pipeline. Break down by original lost_reason: which lost-reasons most often turn into revivals (informs sales coaching on when 'no' was actually 'not yet'). Use the result of "Find losses worth revisiting", "Write two revival emails", "Check what changed first", "Send at day 0 and day 14".
