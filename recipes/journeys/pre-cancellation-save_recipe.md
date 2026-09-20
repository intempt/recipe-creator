---
name: pre-cancellation-save
description: Use when a user mentions "pre-cancellation save", "cancel intent save flow", "save flow before cancel", or asks for related help. When a user starts the cancellation flow (visits cancel page, clicks cancel button) but hasn't completed it, fire a contextual save sequence (pause offer, downgrade offer, retention discount, or human handoff) calibrated by user value and stated cancel reason.
arguments: []
intempt:
  id: pre-cancellation-save
  title: "Save them before they cancel"
  version: 1.0.0
  slashCommand: /pre-cancellation-save
  group: Journeys
  shortDescription: "Catches people who open the cancel flow but have not finished it, and answers the reason they gave with a pause, a downgrade, a discount or a call."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [cancel-save, retention, voluntary-churn]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: page_viewed, severity: blocking }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: "Catch cancel intent live"
      command: create_ai_attribute
      produces: attribute
      bindsAs: cancel_intent
      description: "Tracked in real time: a visit to the cancel or downgrade page in the last 14 days, a click on cancel subscription, or a cancel reason submitted without confirming. It records how far they got, the reason if they gave one, and when. It expires after 7 quiet days."
      prompt: 'Create an AI-derived attribute ''cancel_intent_signal'' on the User object. Computed in real-time. Inputs: (a) visited /cancel or /downgrade page in last 14 days; (b) clicked ''cancel subscription'' button (which triggers cancel-modal not cancellation); (c) submitted cancel reason in cancel-flow form without confirming. Output: object with intent_level (browsing / interacting / committing), stated_reason if captured (price / unused / competitor / feature-gap / pause-needed / other), and timestamp. The signal expires after 7 days of no further activity.'
    - step: 2
      title: "Find who is halfway out"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - cancel_intent
      description: "Paying users who are interacting with or committing to the cancel flow but are still subscribed. Trials are left out, and so is anyone who already got a save offer in the last 90 days."
      prompt: Build a segment 'Cancel-intent active' capturing paying users where cancel_intent_signal.intent_level is 'interacting' or 'committing' AND subscription is still active (not yet cancelled, once cancelled, post-cancel-winback takes over). Excludes users on trial (different motion) and users who have already received a cancel-save offer in last 90 days (no spam).
    - step: 3
      title: "Write one offer per reason"
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - cancel_intent
      - segment
      description: "Price gets 20% off for three months or a lighter plan. Not using it gets a 60 day pause or a one to one onboarding call. A competitor gets a call with a product manager and a comparison sheet. A missing feature gets the roadmap for it and a workaround in the meantime. Needing a break gets a one click pause of up to 90 days with their data kept. No reason given gets a question about what would have kept them, plus a call."
      prompt: 'Generate branched save-offer content per cancel reason. (a) Price reason: offer 20% retention discount for 3 months OR downgrade-to-lighter-plan option; (b) Unused reason: offer 60-day pause OR a 1:1 onboarding call to drive activation; (c) Competitor reason: offer a 1:1 call with PM to address feature gaps + competitive comparison sheet; (d) Feature-gap reason: roadmap visibility for the specific missing feature + interim workaround; (e) Pause-needed reason: 1-click pause for up to 90 days (preserves data); (f) Other/no-reason: ask ''what would have made you stay?'' + offer 1:1 call. Send-from: the customer''s CSM if assigned, else success@ address.'
    - step: 4
      title: "Make one matched offer"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - cancel_intent
      - segment
      - asset
      description: "Each person gets a single offer, chosen by the reason they gave, within an hour of the signal, and a softer follow up on day 2 if nothing happens. The top 10% by ARR also raise an urgent CSM task straight away, so a human tries in parallel. It closes when the offer is accepted, when they cancel anyway, or after 14 days."
      prompt: 'Build a branched journey triggered when cancel_intent_signal becomes ''interacting'' or ''committing''. Branch on stated_reason: each user gets ONE save offer matched to their stated reason. Touch 1 (within 1 hour of intent signal): the matched save offer email. Touch 2 (Day 2, if no engagement): softer follow-up reinforcing the offer. For high-LTV customers (top 10% by ARR), additionally create urgent CSM task at intent detection: human save attempt parallel to email. Exit on: save_offer_accepted (recorded as retention_win event), subscription_canceled (proceed to post-cancel-winback), or 14-day timeout.'
    - step: 5
      title: "See which saves actually work"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - cancel_intent
      - segment
      - asset
      - journey
      description: "Cancel intent per week, how many of those people are still here 30 days later, the save rate by reason and by offer type, the ARR saved this quarter, the spread of reasons given, and the segments where saving never works."
      prompt: 'Compose a save-flow dashboard: cancel-intent volume by week, save rate (intent users who DON''T cancel within 30 days), save rate by stated reason (which save offers actually work), save rate by offer type (discount vs. pause vs. downgrade vs. 1:1 call: informs offer strategy), and ARR saved this quarter. Also surface: stated cancel reasons distribution (voice-of-customer for product/pricing teams) and cohorts where save attempts fail consistently (deep churn signal: those segments need product fixes, not save offers).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Save them before they cancel

Catches people who open the cancel flow but have not finished it, and answers the reason they gave with a pause, a downgrade, a discount or a call.

## Before you run it

- Send the `page_viewed` event

## What it does

1. **Catch cancel intent live** (`create_ai_attribute`)

   Tracked in real time: a visit to the cancel or downgrade page in the last 14 days, a click on cancel subscription, or a cancel reason submitted without confirming. It records how far they got, the reason if they gave one, and when. It expires after 7 quiet days.

2. **Find who is halfway out** (`create_segment`)

   Paying users who are interacting with or committing to the cancel flow but are still subscribed. Trials are left out, and so is anyone who already got a save offer in the last 90 days.

3. **Write one offer per reason** (`create_email_content`)

   Price gets 20% off for three months or a lighter plan. Not using it gets a 60 day pause or a one to one onboarding call. A competitor gets a call with a product manager and a comparison sheet. A missing feature gets the roadmap for it and a workaround in the meantime. Needing a break gets a one click pause of up to 90 days with their data kept. No reason given gets a question about what would have kept them, plus a call.

4. **Make one matched offer** (`create_journey`)

   Each person gets a single offer, chosen by the reason they gave, within an hour of the signal, and a softer follow up on day 2 if nothing happens. The top 10% by ARR also raise an urgent CSM task straight away, so a human tries in parallel. It closes when the offer is accepted, when they cancel anyway, or after 14 days.

5. **See which saves actually work** (`create_dashboard`)

   Cancel intent per week, how many of those people are still here 30 days later, the save rate by reason and by offer type, the ARR saved this quarter, the spread of reasons given, and the segments where saving never works.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
