---
name: content-download-nurture
description: Use when a user mentions "content download nurture", "lead magnet nurture", "ebook download follow-up", or asks for related help. When a prospect downloads a content asset (ebook, guide, whitepaper, calculator), fire a topic-aligned nurture sequence — related content, case study, and warm CTA — to convert content interest into product evaluation.
arguments: []
intempt:
  id: content-download-nurture
  version: 1.0.0
  slashCommand: /content-download-nurture
  group: Journeys
  shortDescription: "Builds a per-content-topic segment of 30-day content downloaders and a 3-touch nurture journey with topic-aligned emails."
  availability: coming-soon
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
      title: Identify Recent Content Downloaders
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Recent content downloaders - last 30 days' capturing users with form_submitted where form_type = content_download in the last 30 days, partitioned by the content_topic (so each topic gets its own nurture cadence). Excludes users who are already paying customers (different motion) and users with an open deal already (don't double-nurture).
      prompt: Build a segment 'Recent content downloaders - last 30 days' capturing users with form_submitted where form_type = content_download in the last 30 days, partitioned by the content_topic (so each topic gets its own nurture cadence). Excludes users who are already paying customers (different motion) and users with an open deal already (don't double-nurture).
    - step: 2
      title: Build Topic-Aligned Nurture Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: 'Generate 3-touch nurture email content per content topic. Touch 1 (Day 1): ''Thanks for downloading [content title] — here''s a related piece you might like'' — second piece of related content. Touch 2 (Day 7): customer case study from a similar company/industry where the topic problem was solved using your product. Touch 3 (Day 14): warm CTA — ''Want to see how this works in your context? Book a 30-min demo'' or ''Try it free for 14 days''. Each email educational-first, sales-second. Send-from: marketing@ for touch 1-2, sales@ or AE for touch 3.'
      prompt: 'Generate 3-touch nurture email content per content topic. Touch 1 (Day 1): ''Thanks for downloading [content title] — here''s a related piece you might like'' — second piece of related content. Touch 2 (Day 7): customer case study from a similar company/industry where the topic problem was solved using your product. Touch 3 (Day 14): warm CTA — ''Want to see how this works in your context? Book a 30-min demo'' or ''Try it free for 14 days''. Each email educational-first, sales-second. Send-from: marketing@ for touch 1-2, sales@ or AE for touch 3.'
    - step: 3
      title: Build Nurture Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: 'Build a 3-touch journey triggered when content_download event fires. Touch 1: Day 1. Touch 2: Day 7. Touch 3: Day 14. Add an engagement branch: if the user engages strongly (opens all 3 emails + clicks 2+ CTAs), fast-track to an SDR task (high-intent signal) and exit journey. If user downloads ANOTHER piece of content during the journey, reset the journey to Day 1 with the new topic (signals deeper exploration, restart the nurture in the new context). Exit conditions: meeting_scheduled, deal_created, or 21-day timeout.'
      prompt: 'Build a 3-touch journey triggered when content_download event fires. Touch 1: Day 1. Touch 2: Day 7. Touch 3: Day 14. Add an engagement branch: if the user engages strongly (opens all 3 emails + clicks 2+ CTAs), fast-track to an SDR task (high-intent signal) and exit journey. If user downloads ANOTHER piece of content during the journey, reset the journey to Day 1 with the new topic (signals deeper exploration, restart the nurture in the new context). Exit conditions: meeting_scheduled, deal_created, or 21-day timeout.'
    - step: 4
      title: Build Content Funnel Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: 'Compose a content-nurture funnel dashboard: content-download volume by topic (which topics attract the most downloads — informs content strategy), download-to-meeting conversion rate by topic (which topics actually correlate with sales pipeline — informs which content to produce more of), email engagement per touch, multi-download user count (users downloading 3+ pieces are high-intent signals — flag for SDR fast-tracking), and content-to-deal-closed pipeline value (the longer-cycle proof-of-value).'
      prompt: 'Compose a content-nurture funnel dashboard: content-download volume by topic (which topics attract the most downloads — informs content strategy), download-to-meeting conversion rate by topic (which topics actually correlate with sales pipeline — informs which content to produce more of), email engagement per touch, multi-download user count (users downloading 3+ pieces are high-intent signals — flag for SDR fast-tracking), and content-to-deal-closed pipeline value (the longer-cycle proof-of-value).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Content Download Nurture

## Procedure

1. **Identify Recent Content Downloaders** [`create_segment`] — Build a segment 'Recent content downloaders - last 30 days' capturing users with form_submitted where form_type = content_download in the last 30 days, partitioned by the content_topic (so each topic gets its own nurture cadence). Excludes users who are already paying customers (different motion) and users with an open deal already (don't double-nurture). → produces: segment
2. **Build Topic-Aligned Nurture Content** [`create_email_content`] — Generate 3-touch nurture email content per content topic. Touch 1 (Day 1): 'Thanks for downloading [content title] — here's a related piece you might like' — second piece of related content. Touch 2 (Day 7): customer case study from a similar company/industry where the topic problem was solved using your product. Touch 3 (Day 14): warm CTA — 'Want to see how this works in your context? Book a 30-min demo' or 'Try it free for 14 days'. Each email educational-first, sales-second. Send-from: marketing@ for touch 1-2, sales@ or AE for touch 3. → produces: asset
3. **Build Nurture Journey** [`create_journey`] — Build a 3-touch journey triggered when content_download event fires. Touch 1: Day 1. Touch 2: Day 7. Touch 3: Day 14. Add an engagement branch: if the user engages strongly (opens all 3 emails + clicks 2+ CTAs), fast-track to an SDR task (high-intent signal) and exit journey. If user downloads ANOTHER piece of content during the journey, reset the journey to Day 1 with the new topic (signals deeper exploration, restart the nurture in the new context). Exit conditions: meeting_scheduled, deal_created, or 21-day timeout. → produces: journey
4. **Build Content Funnel Dashboard** [`create_dashboard`] — Compose a content-nurture funnel dashboard: content-download volume by topic (which topics attract the most downloads — informs content strategy), download-to-meeting conversion rate by topic (which topics actually correlate with sales pipeline — informs which content to produce more of), email engagement per touch, multi-download user count (users downloading 3+ pieces are high-intent signals — flag for SDR fast-tracking), and content-to-deal-closed pipeline value (the longer-cycle proof-of-value). → produces: dashboard
