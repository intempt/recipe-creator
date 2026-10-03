---
id: breakup-sequence
title: Breakup email for silent prospects
slash_command: /breakup-sequence
group: Journeys
owner: intempt
summary: Sends one honest last email to prospects who never replied, which usually gets a faster yes or
  no than another follow up would.
description: >-
  For cold prospects who have gone completely silent after 5+ outreach attempts, send a final 'closing
  the loop' break-up email, honest, low-pressure, often surprisingly effective at unsticking conversations
  that otherwise die in silence.
version: 2.0.0
classification:
  product:
    - sales
  agent: journey-builder
  mode:
    - b2b
  complexity: quick
  executionMode: live
  tags:
    - break-up
    - cold-outreach
    - loop-closing
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new segment, from step 1 "Find prospects who went quiet"
    - A new designed email, from step 2 "Write the closing the loop note"
    - A new journey, from step 3 "Send it once, then stop"
    - A new dashboard, from step 4 "See what the last email pulls"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find prospects who went quiet
    summary: >-
      Leads who got five or more outreach attempts by email or call in the last 60 days and never opened,
      replied or booked. Leads with an open deal are left out, and so are target accounts, which deserve
      a new angle instead.
    builds: segment
    description: >-
      Build a segment 'Cold silent prospects' capturing leads who received 5+ outreach attempts (across
      email and call tasks) in the last 60 days AND have not engaged at all (no opens, no replies, no
      meetings). Excludes leads with open deals (different motion) and leads whose accounts are on the
      target-account list (those merit continued outreach with new angles, not breakup).
  - id: s2
    title: Write the closing the loop note
    summary: >-
      Four or five sentences under a subject line like 'Closing the loop'. It says you have reached out
      a few times, the timing may be wrong, you will stop unless you hear back, and here is a calendar
      link if that changes. No fake final chance framing.
    builds: email_html
    description: >-
      Generate break-up email content. Subject: 'Closing the loop' or 'Should I stop reaching out?': direct,
      no fake urgency. Body: short (4-5 sentences). 'I've reached out a few times about [topic]. I might
      have my timing wrong, or this might not be a priority for you right now. I'll stop reaching out
      unless I hear back. If circumstances change down the road, here's an easy way to reconnect: [calendar
      link].' Tone: honest, no manipulation, no fake 'final chance!' framing. Counter-intuitively often
      the highest-replying email in a cold sequence because it removes pressure and invites a quick 'yes/no'.
      Use the result of "Find prospects who went quiet".
    dependsOn:
      - s1
  - id: s3
    title: Send it once, then stop
    summary: >-
      One email when a lead enters the segment. Any reply routes them to an AE, a booked meeting counts
      as a win, unsubscribes are honoured, and after 14 days of silence the lead is marked cold closed
      and drops out of outreach until a new signal brings them back.
    builds: journey
    description: >-
      Build a 1-touch journey triggered when a lead enters the cold-silent segment. Send the break-up
      email. Exit on: email_replied (any reply = success, route to AE for human handling), meeting_scheduled
      (huge success), unsubscribe (honored (and that's a clean outcome too), or 14-day timeout (no response)
      mark lead as 'cold-closed', exit from active outreach). After timeout, the lead can re-enter prospecting
      only via a new significant signal (target-account refresh, intent signal, etc). Use the result of
      "Find prospects who went quiet", "Write the closing the loop note".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: See what the last email pulls
    summary: >-
      Volume per week, reply rate, how many replies turn into meetings, how many say try again later,
      and the pipeline this email recovered this quarter, broken out by rep.
    builds: dashboard
    description: >-
      Compose a break-up sequence performance dashboard: break-up email volume per week, reply rate (typically
      8-15%: surprisingly high for an 'I give up' message), positive-reply rate (replies that lead to
      meetings vs. polite 'no thanks'), cold-closed conversion (% who say 'not now but try again later':
      those become future revival candidates), and pipeline recovered via break-up sequence this quarter
      (the unexpected upside). Manager view: rep-by-rep adoption of the break-up tactic. Use the result
      of "Find prospects who went quiet", "Write the closing the loop note", "Send it once, then stop".
    dependsOn:
      - s1
      - s2
      - s3
outputs:
  - key: segment
    producedByStep: s1
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s2
    type: asset
    description: Asset produced by this recipe.
  - key: journey
    producedByStep: s3
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s4
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Breakup email for silent prospects

Sends one honest last email to prospects who never replied, which usually gets a faster yes or no than another follow up would.

## Steps

1. **Find prospects who went quiet** (builds segment)

   Leads who got five or more outreach attempts by email or call in the last 60 days and never opened, replied or booked. Leads with an open deal are left out, and so are target accounts, which deserve a new angle instead.

2. **Write the closing the loop note** (builds email_html)

   Four or five sentences under a subject line like 'Closing the loop'. It says you have reached out a few times, the timing may be wrong, you will stop unless you hear back, and here is a calendar link if that changes. No fake final chance framing.

3. **Send it once, then stop** (builds journey)

   One email when a lead enters the segment. Any reply routes them to an AE, a booked meeting counts as a win, unsubscribes are honoured, and after 14 days of silence the lead is marked cold closed and drops out of outreach until a new signal brings them back.

4. **See what the last email pulls** (builds dashboard)

   Volume per week, reply rate, how many replies turn into meetings, how many say try again later, and the pipeline this email recovered this quarter, broken out by rep.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new segment, from step 1 "Find prospects who went quiet"
- A new designed email, from step 2 "Write the closing the loop note"
- A new journey, from step 3 "Send it once, then stop"
- A new dashboard, from step 4 "See what the last email pulls"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
