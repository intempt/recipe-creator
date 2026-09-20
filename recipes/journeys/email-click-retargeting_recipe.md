---
name: email-click-retargeting
description: Use when a user mentions "email click retargeting", "interest-based follow-up", "click-triggered nurture", or asks for related help. When a user clicks a specific link in a marketing email (product feature, pricing page, case study), fire an interest-based follow-up sequence with deeper content on that exact topic — clicks are intent signals, treat them as such.
arguments: []
intempt:
  id: email-click-retargeting
  version: 1.0.0
  slashCommand: /email-click-retargeting
  group: Journeys
  shortDescription: 'When a user clicks a specific link in a marketing email (product feature, pricing page, case study), fire an interest-based follow-up sequence with deeper content on that exact topic: clicks are intent signals, treat them as such.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [click-triggered, interest-based, behavioral-nurture]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: email_clicked, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Click-Intent Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: click_intent
      description: 'Create an AI-derived attribute ''recent_click_topics'' on the User object. Capture: links clicked in marketing emails in the last 14 days, classified by topic (pricing / feature-X / case-study / blog / integration). Output: ranked list of top topics by click count. The clicker is showing you what they care about — log it and act on it.'
      prompt: 'Create an AI-derived attribute ''recent_click_topics'' on the User object. Capture: links clicked in marketing emails in the last 14 days, classified by topic (pricing / feature-X / case-study / blog / integration). Output: ranked list of top topics by click count. The clicker is showing you what they care about — log it and act on it.'
    - step: 2
      title: Identify Recent Clickers
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - click_intent
      description: Build a segment 'Recent email clickers - last 14 days' capturing users with email_clicked event in the last 14 days where the click was on a high-signal link (pricing, feature page, case study — not generic 'view in browser' or footer). Partitioned by click_topic. Excludes users who already engaged downstream (e.g. visited pricing page, started trial — those are getting other journeys).
      prompt: Build a segment 'Recent email clickers - last 14 days' capturing users with email_clicked event in the last 14 days where the click was on a high-signal link (pricing, feature page, case study — not generic 'view in browser' or footer). Partitioned by click_topic. Excludes users who already engaged downstream (e.g. visited pricing page, started trial — those are getting other journeys).
    - step: 3
      title: Build Retargeting Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - click_intent
      - segment
      description: 'Generate retargeting email content per click topic. Pricing-page click: ''You looked at pricing — want to talk it through? Or here''s a pricing FAQ.'' Feature-X click: deeper dive on feature X with a customer story using it. Case-study click: related case study from a similar company/industry. Each: low-pressure, educational, treats the click as continued conversation not aggressive ''we saw you!'' creepiness. Send-from: marketing@ or the original email''s sender.'
      prompt: 'Generate retargeting email content per click topic. Pricing-page click: ''You looked at pricing — want to talk it through? Or here''s a pricing FAQ.'' Feature-X click: deeper dive on feature X with a customer story using it. Case-study click: related case study from a similar company/industry. Each: low-pressure, educational, treats the click as continued conversation not aggressive ''we saw you!'' creepiness. Send-from: marketing@ or the original email''s sender.'
    - step: 4
      title: Build Retargeting Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - click_intent
      - segment
      - asset
      description: 'Build a 2-touch journey triggered when email_clicked fires on a high-signal link. Touch 1 (Day 1): topic-matched follow-up. Touch 2 (Day 5): if no further engagement, offer a soft CTA (book a chat / try free / talk to AE based on company size). If user clicks something during this journey, reset to a fresh topic-matched cadence. Exit on: meeting_scheduled, deal_created, or 10-day timeout. Throttle hard: never trigger this journey more than once per week per user — clicks happen constantly, don''t bombard.'
      prompt: 'Build a 2-touch journey triggered when email_clicked fires on a high-signal link. Touch 1 (Day 1): topic-matched follow-up. Touch 2 (Day 5): if no further engagement, offer a soft CTA (book a chat / try free / talk to AE based on company size). If user clicks something during this journey, reset to a fresh topic-matched cadence. Exit on: meeting_scheduled, deal_created, or 10-day timeout. Throttle hard: never trigger this journey more than once per week per user — clicks happen constantly, don''t bombard.'
    - step: 5
      title: Build Click-Retargeting Performance Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - click_intent
      - segment
      - asset
      - journey
      description: 'Compose a click-retargeting dashboard: retargeting trigger volume by click topic, follow-up engagement rate (do retargeting emails get higher engagement than the original — they should: matched intent), click-to-meeting conversion rate, click-to-deal conversion rate. The killer chart: compare conversion rate of click-retargeted users vs. control (users who clicked but received no retargeting) — typically retargeting drives 2-3x higher conversion. Surfaces evidence of behavioral-nurture value.'
      prompt: 'Compose a click-retargeting dashboard: retargeting trigger volume by click topic, follow-up engagement rate (do retargeting emails get higher engagement than the original — they should: matched intent), click-to-meeting conversion rate, click-to-deal conversion rate. The killer chart: compare conversion rate of click-retargeted users vs. control (users who clicked but received no retargeting) — typically retargeting drives 2-3x higher conversion. Surfaces evidence of behavioral-nurture value.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Email Click Retargeting

## Procedure

1. **Build Click-Intent Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'recent_click_topics' on the User object. Capture: links clicked in marketing emails in the last 14 days, classified by topic (pricing / feature-X / case-study / blog / integration). Output: ranked list of top topics by click count. The clicker is showing you what they care about — log it and act on it. → produces: attribute
2. **Identify Recent Clickers** [`create_segment`] — Build a segment 'Recent email clickers - last 14 days' capturing users with email_clicked event in the last 14 days where the click was on a high-signal link (pricing, feature page, case study — not generic 'view in browser' or footer). Partitioned by click_topic. Excludes users who already engaged downstream (e.g. visited pricing page, started trial — those are getting other journeys). → produces: segment
3. **Build Retargeting Email Content** [`create_email_content`] — Generate retargeting email content per click topic. Pricing-page click: 'You looked at pricing — want to talk it through? Or here's a pricing FAQ.' Feature-X click: deeper dive on feature X with a customer story using it. Case-study click: related case study from a similar company/industry. Each: low-pressure, educational, treats the click as continued conversation not aggressive 'we saw you!' creepiness. Send-from: marketing@ or the original email's sender. → produces: asset
4. **Build Retargeting Journey** [`create_journey`] — Build a 2-touch journey triggered when email_clicked fires on a high-signal link. Touch 1 (Day 1): topic-matched follow-up. Touch 2 (Day 5): if no further engagement, offer a soft CTA (book a chat / try free / talk to AE based on company size). If user clicks something during this journey, reset to a fresh topic-matched cadence. Exit on: meeting_scheduled, deal_created, or 10-day timeout. Throttle hard: never trigger this journey more than once per week per user — clicks happen constantly, don't bombard. → produces: journey
5. **Build Click-Retargeting Performance Dashboard** [`create_dashboard`] — Compose a click-retargeting dashboard: retargeting trigger volume by click topic, follow-up engagement rate (do retargeting emails get higher engagement than the original — they should: matched intent), click-to-meeting conversion rate, click-to-deal conversion rate. The killer chart: compare conversion rate of click-retargeted users vs. control (users who clicked but received no retargeting) — typically retargeting drives 2-3x higher conversion. Surfaces evidence of behavioral-nurture value. → produces: dashboard
