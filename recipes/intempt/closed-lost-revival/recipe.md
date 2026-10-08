---
description: Goes back to deals lost 90 days ago, checks what has changed at the account, and reopens the conversation where the reason for losing may have expired.
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
---

# Closed lost revival

Slash command: /closed-lost-revival

## Step 1: Find losses worth revisiting

Build a segment 'Closed-lost revival candidates' capturing deals where deal_lost event fired 90-180 days ago AND lost_reason is NOT 'wrong-fit' or 'competitor-won-firm-commitment' (those won't revive). Includes deals lost to: timing, budget, no-decision, internal-resourcing, postponed. Excludes accounts that have entered closed-lost more than twice (3-strikes rule: stop pestering).

## Step 2: Write two revival emails

Generate 2-touch revival email content. Touch 1 (Day 0): 'It's been a few months: wanted to check in. Last time we talked, [original_lost_reason]. Has anything changed?' Reference specific prior conversation context. Soft re-open, not a sales pitch. Touch 2 (Day 14, if no reply): share a relevant product update or customer story from a similar account that addresses their original objection. Send-from: the original AE owner. Tone: warm, low-pressure, acknowledging the prior 'no'. Use the result of "Find losses worth revisiting".

## Step 3: Check what changed first

Create a workflow firing daily for newly-eligible revival candidates. Step sequence: (1) refresh account enrichment (champion still there? new leadership? funding announced? product launched?); (2) IF significant change detected (new champion-role hire, funding round, etc.): create urgent AE task to manually reach out; ELSE trigger the standard 2-touch revival journey. Track responses and any new meeting bookings as revival_signal events on the original closed-lost deal record. Use the result of "Find losses worth revisiting", "Write two revival emails".

## Step 4: Send at day 0 and day 14

Build a 2-touch journey triggered by the revival workflow. Touch 1 at Day 0, Touch 2 at Day 14 (skipped if user replies or books meeting). Audience: the original deal's primary contact. Exit on: meeting_scheduled (revival success: open new deal), email_replied (warm handoff to AE), unsubscribe, or 30-day max duration. Use the result of "Find losses worth revisiting", "Write two revival emails", "Check what changed first".

## Step 5: See what comes back to life

Compose a revival performance dashboard: closed-lost deals entering revival per month, reply rate to revival outreach, meeting-booked rate from revival, revived-deal-to-win rate (final conversion), and ARR resurrected this quarter from revival pipeline. Break down by original lost_reason: which lost-reasons most often turn into revivals (informs sales coaching on when 'no' was actually 'not yet'). Use the result of "Find losses worth revisiting", "Write two revival emails", "Check what changed first", "Send at day 0 and day 14".
