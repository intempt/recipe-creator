---
name: breakup-sequence
description: Use when a user mentions "break-up sequence", "closing the loop", "final outreach attempt", or asks for related help. For cold prospects who have gone completely silent after 5+ outreach attempts, send a final 'closing the loop' break-up email — honest, low-pressure, often surprisingly effective at unsticking conversations that otherwise die in silence.
arguments: []
intempt:
  id: breakup-sequence
  version: 1.0.0
  slashCommand: /breakup-sequence
  group: Journeys
  shortDescription: 'For cold prospects who have gone completely silent after 5+ outreach attempts, send a final ''closing the loop'' break-up email: honest, low-pressure, often surprisingly effective at unsticking conversations that otherwise die in silence.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: journey-builder
    mode: [b2b]
    complexity: quick
    executionMode: live
    tags: [break-up, cold-outreach, loop-closing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Identify Cold Silent Prospects
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Cold silent prospects' capturing leads who received 5+ outreach attempts (across email and call tasks) in the last 60 days AND have not engaged at all (no opens, no replies, no meetings). Excludes leads with open deals (different motion) and leads whose accounts are on the target-account list (those merit continued outreach with new angles, not breakup).
      prompt: Build a segment 'Cold silent prospects' capturing leads who received 5+ outreach attempts (across email and call tasks) in the last 60 days AND have not engaged at all (no opens, no replies, no meetings). Excludes leads with open deals (different motion) and leads whose accounts are on the target-account list (those merit continued outreach with new angles, not breakup).
    - step: 2
      title: Build Break-up Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: 'Generate break-up email content. Subject: ''Closing the loop'' or ''Should I stop reaching out?'' — direct, no fake urgency. Body: short (4-5 sentences). ''I''ve reached out a few times about [topic]. I might have my timing wrong, or this might not be a priority for you right now. I''ll stop reaching out unless I hear back. If circumstances change down the road, here''s an easy way to reconnect: [calendar link].'' Tone: honest, no manipulation, no fake ''final chance!'' framing. Counter-intuitively often the highest-replying email in a cold sequence because it removes pressure and invites a quick ''yes/no''.'
      prompt: 'Generate break-up email content. Subject: ''Closing the loop'' or ''Should I stop reaching out?'' — direct, no fake urgency. Body: short (4-5 sentences). ''I''ve reached out a few times about [topic]. I might have my timing wrong, or this might not be a priority for you right now. I''ll stop reaching out unless I hear back. If circumstances change down the road, here''s an easy way to reconnect: [calendar link].'' Tone: honest, no manipulation, no fake ''final chance!'' framing. Counter-intuitively often the highest-replying email in a cold sequence because it removes pressure and invites a quick ''yes/no''.'
    - step: 3
      title: Build Break-up Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: 'Build a 1-touch journey triggered when a lead enters the cold-silent segment. Send the break-up email. Exit on: email_replied (any reply = success, route to AE for human handling), meeting_scheduled (huge success), unsubscribe (honored — and that''s a clean outcome too), or 14-day timeout (no response — mark lead as ''cold-closed'', exit from active outreach). After timeout, the lead can re-enter prospecting only via a new significant signal (target-account refresh, intent signal, etc).'
      prompt: 'Build a 1-touch journey triggered when a lead enters the cold-silent segment. Send the break-up email. Exit on: email_replied (any reply = success, route to AE for human handling), meeting_scheduled (huge success), unsubscribe (honored — and that''s a clean outcome too), or 14-day timeout (no response — mark lead as ''cold-closed'', exit from active outreach). After timeout, the lead can re-enter prospecting only via a new significant signal (target-account refresh, intent signal, etc).'
    - step: 4
      title: Build Break-up Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: 'Compose a break-up sequence performance dashboard: break-up email volume per week, reply rate (typically 8-15% — surprisingly high for an ''I give up'' message), positive-reply rate (replies that lead to meetings vs. polite ''no thanks''), cold-closed conversion (% who say ''not now but try again later'' — those become future revival candidates), and pipeline recovered via break-up sequence this quarter (the unexpected upside). Manager view: rep-by-rep adoption of the break-up tactic.'
      prompt: 'Compose a break-up sequence performance dashboard: break-up email volume per week, reply rate (typically 8-15% — surprisingly high for an ''I give up'' message), positive-reply rate (replies that lead to meetings vs. polite ''no thanks''), cold-closed conversion (% who say ''not now but try again later'' — those become future revival candidates), and pipeline recovered via break-up sequence this quarter (the unexpected upside). Manager view: rep-by-rep adoption of the break-up tactic.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Breakup Sequence

## Procedure

1. **Identify Cold Silent Prospects** [`create_segment`] — Build a segment 'Cold silent prospects' capturing leads who received 5+ outreach attempts (across email and call tasks) in the last 60 days AND have not engaged at all (no opens, no replies, no meetings). Excludes leads with open deals (different motion) and leads whose accounts are on the target-account list (those merit continued outreach with new angles, not breakup). → produces: segment
2. **Build Break-up Email Content** [`create_email_content`] — Generate break-up email content. Subject: 'Closing the loop' or 'Should I stop reaching out?' — direct, no fake urgency. Body: short (4-5 sentences). 'I've reached out a few times about [topic]. I might have my timing wrong, or this might not be a priority for you right now. I'll stop reaching out unless I hear back. If circumstances change down the road, here's an easy way to reconnect: [calendar link].' Tone: honest, no manipulation, no fake 'final chance!' framing. Counter-intuitively often the highest-replying email in a cold sequence because it removes pressure and invites a quick 'yes/no'. → produces: asset
3. **Build Break-up Journey** [`create_journey`] — Build a 1-touch journey triggered when a lead enters the cold-silent segment. Send the break-up email. Exit on: email_replied (any reply = success, route to AE for human handling), meeting_scheduled (huge success), unsubscribe (honored — and that's a clean outcome too), or 14-day timeout (no response — mark lead as 'cold-closed', exit from active outreach). After timeout, the lead can re-enter prospecting only via a new significant signal (target-account refresh, intent signal, etc). → produces: journey
4. **Build Break-up Performance Dashboard** [`create_dashboard`] — Compose a break-up sequence performance dashboard: break-up email volume per week, reply rate (typically 8-15% — surprisingly high for an 'I give up' message), positive-reply rate (replies that lead to meetings vs. polite 'no thanks'), cold-closed conversion (% who say 'not now but try again later' — those become future revival candidates), and pipeline recovered via break-up sequence this quarter (the unexpected upside). Manager view: rep-by-rep adoption of the break-up tactic. → produces: dashboard
