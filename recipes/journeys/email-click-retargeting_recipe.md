---
name: email-click-retargeting
description: Use when a user mentions "email click retargeting", "interest-based follow-up", "click-triggered nurture", or asks for related help. When a user clicks a specific link in a marketing email (product feature, pricing page, case study), fire an interest-based follow-up sequence with deeper content on that exact topic, clicks are intent signals, treat them as such.
arguments: []
intempt:
  id: email-click-retargeting
  title: "Email click follow up"
  version: 1.0.0
  slashCommand: /email-click-retargeting
  group: Journeys
  shortDescription: "Treats a click on pricing, a feature page or a case study as interest and sends more on that exact topic, at most once a week."
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
      title: "Log what they clicked"
      command: create_ai_attribute
      produces: attribute
      bindsAs: click_intent
      description: "The links each person clicked in marketing emails over the last 14 days, sorted into topics such as pricing, a feature, a case study, the blog or an integration, then ranked by how often."
      prompt: 'Create an AI-derived attribute ''recent_click_topics'' on the User object. Capture: links clicked in marketing emails in the last 14 days, classified by topic (pricing / feature-X / case-study / blog / integration). Output: ranked list of top topics by click count. The clicker is showing you what they care about: log it and act on it.'
    - step: 2
      title: "Find the meaningful clicks"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - click_intent
      description: "People who clicked a high signal link in the last 14 days, split by topic. Footer and view in browser links do not count, and anyone already further along, on a trial or on the pricing page, is left out."
      prompt: Build a segment 'Recent email clickers - last 14 days' capturing users with email_clicked event in the last 14 days where the click was on a high-signal link (pricing, feature page, case study, not generic 'view in browser' or footer). Partitioned by click_topic. Excludes users who already engaged downstream (e.g. visited pricing page, started trial, those are getting other journeys).
    - step: 3
      title: "Write a reply per topic"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - click_intent
      - segment
      description: "A pricing click gets a pricing FAQ or an offer to talk it through. A feature click gets a deeper look plus a customer using it. A case study click gets a related one. Low pressure and educational, sent by marketing or by whoever sent the original."
      prompt: 'Generate retargeting email content per click topic. Pricing-page click: ''You looked at pricing: want to talk it through? Or here''s a pricing FAQ.'' Feature-X click: deeper dive on feature X with a customer story using it. Case-study click: related case study from a similar company/industry. Each: low-pressure, educational, treats the click as continued conversation not aggressive ''we saw you!'' creepiness. Send-from: marketing@ or the original email''s sender.'
    - step: 4
      title: "Follow up once, nudge once"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - click_intent
      - segment
      - asset
      description: "The matched email goes out a day after the click, and on day 5 a soft call to action if nothing else has happened. A new click restarts the sequence on the new topic. They leave on a booked meeting, a new deal, or after 10 days. Capped at one run per person per week."
      prompt: 'Build a 2-touch journey triggered when email_clicked fires on a high-signal link. Touch 1 (Day 1): topic-matched follow-up. Touch 2 (Day 5): if no further engagement, offer a soft CTA (book a chat / try free / talk to AE based on company size). If user clicks something during this journey, reset to a fresh topic-matched cadence. Exit on: meeting_scheduled, deal_created, or 10-day timeout. Throttle hard: never trigger this journey more than once per week per user: clicks happen constantly, don''t bombard.'
    - step: 5
      title: "Compare against no follow up"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - click_intent
      - segment
      - asset
      - journey
      description: "Triggers by topic, engagement against the original email, click to meeting and click to deal rates, and how people who got the follow up convert against people who clicked and got nothing."
      prompt: 'Compose a click-retargeting dashboard: retargeting trigger volume by click topic, follow-up engagement rate (do retargeting emails get higher engagement than the original: they should: matched intent), click-to-meeting conversion rate, click-to-deal conversion rate. The killer chart: compare conversion rate of click-retargeted users vs. control (users who clicked but received no retargeting): typically retargeting drives 2-3x higher conversion. Surfaces evidence of behavioral-nurture value.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Email click follow up

Treats a click on pricing, a feature page or a case study as interest and sends more on that exact topic, at most once a week.

## Before you run it

- Send the `email_clicked` event

## What it does

1. **Log what they clicked** (`create_ai_attribute`)

   The links each person clicked in marketing emails over the last 14 days, sorted into topics such as pricing, a feature, a case study, the blog or an integration, then ranked by how often.

2. **Find the meaningful clicks** (`create_segment`)

   People who clicked a high signal link in the last 14 days, split by topic. Footer and view in browser links do not count, and anyone already further along, on a trial or on the pricing page, is left out.

3. **Write a reply per topic** (`create_email_content`)

   A pricing click gets a pricing FAQ or an offer to talk it through. A feature click gets a deeper look plus a customer using it. A case study click gets a related one. Low pressure and educational, sent by marketing or by whoever sent the original.

4. **Follow up once, nudge once** (`create_journey`)

   The matched email goes out a day after the click, and on day 5 a soft call to action if nothing else has happened. A new click restarts the sequence on the new topic. They leave on a booked meeting, a new deal, or after 10 days. Capped at one run per person per week.

5. **Compare against no follow up** (`create_dashboard`)

   Triggers by topic, engagement against the original email, click to meeting and click to deal rates, and how people who got the follow up convert against people who clicked and got nothing.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
