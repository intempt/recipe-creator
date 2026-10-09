---
name: breakup-sequence
description: Use when a user mentions "break-up sequence", "closing the loop", "final outreach attempt", or asks for related help. For cold prospects who have gone completely silent after 5+ outreach attempts, send a final 'closing the loop' break-up email, honest, low-pressure, often surprisingly effective at unsticking conversations that otherwise die in silence.
arguments: []
intempt:
  id: breakup-sequence
  title: "Breakup email for silent prospects"
  version: 1.0.0
  slashCommand: /breakup-sequence
  group: Journeys
  shortDescription: "Sends one honest last email to prospects who never replied, which usually gets a faster yes or no than another follow up would."
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
      title: "Find prospects who went quiet"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Leads who got five or more outreach attempts by email or call in the last 60 days and never opened, replied or booked. Leads with an open deal are left out, and so are target accounts, which deserve a new angle instead."
      prompt: Build a segment 'Cold silent prospects' capturing leads who received 5+ outreach attempts (across email and call tasks) in the last 60 days AND have not engaged at all (no opens, no replies, no meetings). Excludes leads with open deals (different motion) and leads whose accounts are on the target-account list (those merit continued outreach with new angles, not breakup).
    - step: 2
      title: "Write the closing the loop note"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: "Four or five sentences under a subject line like 'Closing the loop'. It says you have reached out a few times, the timing may be wrong, you will stop unless you hear back, and here is a calendar link if that changes. No fake final chance framing."
      prompt: 'Generate break-up email content. Subject: ''Closing the loop'' or ''Should I stop reaching out?'': direct, no fake urgency. Body: short (4-5 sentences). ''I''ve reached out a few times about [topic]. I might have my timing wrong, or this might not be a priority for you right now. I''ll stop reaching out unless I hear back. If circumstances change down the road, here''s an easy way to reconnect: [calendar link].'' Tone: honest, no manipulation, no fake ''final chance!'' framing. Counter-intuitively often the highest-replying email in a cold sequence because it removes pressure and invites a quick ''yes/no''.'
    - step: 3
      title: "Send it once, then stop"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: "One email when a lead enters the segment. Any reply routes them to an AE, a booked meeting counts as a win, unsubscribes are honoured, and after 14 days of silence the lead is marked cold closed and drops out of outreach until a new signal brings them back."
      prompt: 'Build a 1-touch journey triggered when a lead enters the cold-silent segment. Send the break-up email. Exit on: Email replied (any reply = success, route to AE for human handling), Meeting scheduled (huge success), unsubscribe (honored (and that''s a clean outcome too), or 14-day timeout (no response) mark lead as ''cold-closed'', exit from active outreach). After timeout, the lead can re-enter prospecting only via a new significant signal (target-account refresh, intent signal, etc).'
    - step: 4
      title: "See what the last email pulls"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: "Volume per week, reply rate, how many replies turn into meetings, how many say try again later, and the pipeline this email recovered this quarter, broken out by rep."
      prompt: 'Compose a break-up sequence performance dashboard: break-up email volume per week, reply rate (typically 8-15%: surprisingly high for an ''I give up'' message), positive-reply rate (replies that lead to meetings vs. polite ''no thanks''), cold-closed conversion (% who say ''not now but try again later'': those become future revival candidates), and pipeline recovered via break-up sequence this quarter (the unexpected upside). Manager view: rep-by-rep adoption of the break-up tactic.'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Breakup email for silent prospects

Sends one honest last email to prospects who never replied, which usually gets a faster yes or no than another follow up would.

## What it does

1. **Find prospects who went quiet** (`create_segment`)

   Leads who got five or more outreach attempts by email or call in the last 60 days and never opened, replied or booked. Leads with an open deal are left out, and so are target accounts, which deserve a new angle instead.

2. **Write the closing the loop note** (`create_email_content`)

   Four or five sentences under a subject line like 'Closing the loop'. It says you have reached out a few times, the timing may be wrong, you will stop unless you hear back, and here is a calendar link if that changes. No fake final chance framing.

3. **Send it once, then stop** (`create_journey`)

   One email when a lead enters the segment. Any reply routes them to an AE, a booked meeting counts as a win, unsubscribes are honoured, and after 14 days of silence the lead is marked cold closed and drops out of outreach until a new signal brings them back.

4. **See what the last email pulls** (`create_dashboard`)

   Volume per week, reply rate, how many replies turn into meetings, how many say try again later, and the pipeline this email recovered this quarter, broken out by rep.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
