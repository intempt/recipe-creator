---
name: content-download-nurture
description: Use when a user mentions "content download nurture", "lead magnet nurture", "ebook download follow-up", or asks for related help. When a prospect downloads a content asset (ebook, guide, whitepaper, calculator), fire a topic-aligned nurture sequence (related content, case study, and warm CTA) to convert content interest into product evaluation.
arguments: []
intempt:
  id: content-download-nurture
  title: "Content download nurture"
  version: 1.0.0
  slashCommand: /content-download-nurture
  group: Journeys
  shortDescription: "Follows a gated download with two more pieces on the same topic and a soft invite, and fast tracks anyone who reads all three."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: standard
    executionMode: live
    tags: [content-nurture, lead-magnet, b2b-marketing]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: form_submitted, severity: blocking }
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Find recent downloaders"
      command: create_segment
      produces: segment
      bindsAs: segment
      description: "Anyone who filled in a content download form in the last 30 days, split by the topic they took so each gets its own cadence. Paying customers and people with an open deal are left out."
      prompt: Build a segment 'Recent content downloaders - last 30 days' capturing users who submitted a content-download form in the last 30 days, partitioned by the content topic (so each topic gets its own nurture cadence). Excludes users who are already paying customers (different motion) and users with an open deal already (don't double-nurture).
    - step: 2
      title: "Write three emails per topic"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: "Day 1 thanks them and offers a related piece. Day 7 sends a case study from a similar company. Day 14 invites them to a 30 minute demo or a free trial. Educational first and sales second, with the first two from marketing and the last from sales."
      prompt: 'Generate 3-touch nurture email content per content topic. Touch 1 (Day 1): ''Thanks for downloading [content title] (here''s a related piece you might like'') second piece of related content. Touch 2 (Day 7): customer case study from a similar company/industry where the topic problem was solved using your product. Touch 3 (Day 14): warm CTA: ''Want to see how this works in your context? Book a 30-min demo'' or ''Try it free for 14 days''. Each email educational-first, sales-second. Send-from: marketing@ for touch 1-2, sales@ or AE for touch 3.'
    - step: 3
      title: "Send on days 1, 7 and 14"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: "Starts on the download. Anyone who opens all three and clicks twice is handed to an SDR and leaves early. A second download restarts the sequence on the new topic. They also leave on a booked meeting, a new deal, or after 21 days."
      prompt: 'Build a 3-touch journey triggered when a content-download form is submitted. Touch 1: Day 1. Touch 2: Day 7. Touch 3: Day 14. Add an engagement branch: if the user engages strongly (opens all 3 emails + clicks 2+ CTAs), fast-track to an SDR task (high-intent signal) and exit journey. If user downloads ANOTHER piece of content during the journey, reset the journey to Day 1 with the new topic (signals deeper exploration, restart the nurture in the new context). Exit conditions: Meeting scheduled, Deal created, or 21-day timeout.'
    - step: 4
      title: "See which topics make pipeline"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: "Downloads by topic, how often each topic leads to a meeting, engagement per email, who has taken three or more pieces, and the closed pipeline traced back to content."
      prompt: 'Compose a content-nurture funnel dashboard: content-download volume by topic (which topics attract the most downloads: informs content strategy), download-to-meeting conversion rate by topic (which topics actually correlate with sales pipeline: informs which content to produce more of), email engagement per touch, multi-download user count (users downloading 3+ pieces are high-intent signals: flag for SDR fast-tracking), and content-to-deal-closed pipeline value (the longer-cycle proof-of-value).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Content download nurture

Follows a gated download with two more pieces on the same topic and a soft invite, and fast tracks anyone who reads all three.

## Before you run it

- Send the `form_submitted` event

## What it does

1. **Find recent downloaders** (`create_segment`)

   Anyone who filled in a content download form in the last 30 days, split by the topic they took so each gets its own cadence. Paying customers and people with an open deal are left out.

2. **Write three emails per topic** (`create_email_content`)

   Day 1 thanks them and offers a related piece. Day 7 sends a case study from a similar company. Day 14 invites them to a 30 minute demo or a free trial. Educational first and sales second, with the first two from marketing and the last from sales.

3. **Send on days 1, 7 and 14** (`create_journey`)

   Starts on the download. Anyone who opens all three and clicks twice is handed to an SDR and leaves early. A second download restarts the sequence on the new topic. They also leave on a booked meeting, a new deal, or after 21 days.

4. **See which topics make pipeline** (`create_dashboard`)

   Downloads by topic, how often each topic leads to a meeting, engagement per email, who has taken three or more pieces, and the closed pipeline traced back to content.

## What you end up with

- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
