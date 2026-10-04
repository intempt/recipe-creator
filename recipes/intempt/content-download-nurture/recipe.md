---
id: content-download-nurture
title: Content download nurture
slash_command: /content-download-nurture
group: Journeys
owner: intempt
curator: somya
summary: Follows a gated download with two more pieces on the same topic and a soft invite, and fast tracks
  anyone who reads all three.
description: >-
  When a prospect downloads a content asset (ebook, guide, whitepaper, calculator), fire a topic-aligned
  nurture sequence (related content, case study, and warm CTA) to convert content interest into product
  evaluation.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: standard
  executionMode: live
  tags:
    - content-nurture
    - lead-magnet
    - b2b-marketing
prerequisites:
  events:
    - value: form_submitted
      severity: blocking
touches:
  reads:
    - The form_submitted event in your project
  writes:
    - A new segment, from step 1 "Find recent downloaders"
    - A new designed email, from step 2 "Write three emails per topic"
    - A new journey, from step 3 "Send on days 1, 7 and 14"
    - A new dashboard, from step 4 "See which topics make pipeline"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Find recent downloaders
    summary: >-
      Anyone who filled in a content download form in the last 30 days, split by the topic they took so
      each gets its own cadence. Paying customers and people with an open deal are left out.
    builds: segment
    description: >-
      Build a segment 'Recent content downloaders - last 30 days' capturing users with form_submitted
      where form_type = content_download in the last 30 days, partitioned by the content_topic (so each
      topic gets its own nurture cadence). Excludes users who are already paying customers (different
      motion) and users with an open deal already (don't double-nurture).
  - id: s2
    title: Write three emails per topic
    summary: >-
      Day 1 thanks them and offers a related piece. Day 7 sends a case study from a similar company. Day
      14 invites them to a 30 minute demo or a free trial. Educational first and sales second, with the
      first two from marketing and the last from sales.
    builds: email_html
    description: >-
      Generate 3-touch nurture email content per content topic. Touch 1 (Day 1): 'Thanks for downloading
      [content title] (here's a related piece you might like') second piece of related content. Touch
      2 (Day 7): customer case study from a similar company/industry where the topic problem was solved
      using your product. Touch 3 (Day 14): warm CTA: 'Want to see how this works in your context? Book
      a 30-min demo' or 'Try it free for 14 days'. Each email educational-first, sales-second. Send-from:
      marketing@ for touch 1-2, sales@ or AE for touch 3. Use the result of "Find recent downloaders".
    dependsOn:
      - s1
  - id: s3
    title: Send on days 1, 7 and 14
    summary: >-
      Starts on the download. Anyone who opens all three and clicks twice is handed to an SDR and leaves
      early. A second download restarts the sequence on the new topic. They also leave on a booked meeting,
      a new deal, or after 21 days.
    builds: journey
    description: >-
      Build a 3-touch journey triggered when content_download event fires. Touch 1: Day 1. Touch 2: Day
      7. Touch 3: Day 14. Add an engagement branch: if the user engages strongly (opens all 3 emails +
      clicks 2+ CTAs), fast-track to an SDR task (high-intent signal) and exit journey. If user downloads
      ANOTHER piece of content during the journey, reset the journey to Day 1 with the new topic (signals
      deeper exploration, restart the nurture in the new context). Exit conditions: meeting_scheduled,
      deal_created, or 21-day timeout. Use the result of "Find recent downloaders", "Write three emails
      per topic".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: See which topics make pipeline
    summary: >-
      Downloads by topic, how often each topic leads to a meeting, engagement per email, who has taken
      three or more pieces, and the closed pipeline traced back to content.
    builds: dashboard
    description: >-
      Compose a content-nurture funnel dashboard: content-download volume by topic (which topics attract
      the most downloads: informs content strategy), download-to-meeting conversion rate by topic (which
      topics actually correlate with sales pipeline: informs which content to produce more of), email
      engagement per touch, multi-download user count (users downloading 3+ pieces are high-intent signals:
      flag for SDR fast-tracking), and content-to-deal-closed pipeline value (the longer-cycle proof-of-value).
      Use the result of "Find recent downloaders", "Write three emails per topic", "Send on days 1, 7
      and 14".
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

# Content download nurture

Follows a gated download with two more pieces on the same topic and a soft invite, and fast tracks anyone who reads all three.

## Steps

1. **Find recent downloaders** (builds segment)

   Anyone who filled in a content download form in the last 30 days, split by the topic they took so each gets its own cadence. Paying customers and people with an open deal are left out.

2. **Write three emails per topic** (builds email_html)

   Day 1 thanks them and offers a related piece. Day 7 sends a case study from a similar company. Day 14 invites them to a 30 minute demo or a free trial. Educational first and sales second, with the first two from marketing and the last from sales.

3. **Send on days 1, 7 and 14** (builds journey)

   Starts on the download. Anyone who opens all three and clicks twice is handed to an SDR and leaves early. A second download restarts the sequence on the new topic. They also leave on a booked meeting, a new deal, or after 21 days.

4. **See which topics make pipeline** (builds dashboard)

   Downloads by topic, how often each topic leads to a meeting, engagement per email, who has taken three or more pieces, and the closed pipeline traced back to content.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The form_submitted event in your project

Writes:

- A new segment, from step 1 "Find recent downloaders"
- A new designed email, from step 2 "Write three emails per topic"
- A new journey, from step 3 "Send on days 1, 7 and 14"
- A new dashboard, from step 4 "See which topics make pipeline"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey.
