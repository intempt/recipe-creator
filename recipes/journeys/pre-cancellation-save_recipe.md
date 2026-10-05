---
name: pre-cancellation-save
description: Use when a user mentions "pre-cancellation save", "cancel intent save flow", "save flow before cancel", or asks for related help. When a user starts the cancellation flow (visits cancel page, clicks cancel button) but hasn't completed it, fire a contextual save sequence — pause offer, downgrade offer, retention discount, or human handoff — calibrated by user value and stated cancel reason.
arguments: []
intempt:
  id: pre-cancellation-save
  version: 1.0.0
  slashCommand: /pre-cancellation-save
  group: Journeys
  shortDescription: "Produce a cancel_intent_signal attribute from cancel-flow interactions, then trigger a segment-based save journey offering pause, downgrade, discount, or human handoff."
  availability: coming-soon
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
      title: Build Cancel-Intent Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: cancel_intent
      description: 'Create an AI-derived attribute ''cancel_intent_signal'' on the User object. Computed in real-time. Inputs: (a) visited /cancel or /downgrade page in last 14 days; (b) clicked ''cancel subscription'' button (which triggers cancel-modal not cancellation); (c) submitted cancel reason in cancel-flow form without confirming. Output: object with intent_level (browsing / interacting / committing), stated_reason if captured (price / unused / competitor / feature-gap / pause-needed / other), and timestamp. The signal expires after 7 days of no further activity.'
      prompt: 'Create an AI-derived attribute ''cancel_intent_signal'' on the User object. Computed in real-time. Inputs: (a) visited /cancel or /downgrade page in last 14 days; (b) clicked ''cancel subscription'' button (which triggers cancel-modal not cancellation); (c) submitted cancel reason in cancel-flow form without confirming. Output: object with intent_level (browsing / interacting / committing), stated_reason if captured (price / unused / competitor / feature-gap / pause-needed / other), and timestamp. The signal expires after 7 days of no further activity.'
    - step: 2
      title: Identify Cancel-Intent Users
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - cancel_intent
      description: Build a segment 'Cancel-intent active' capturing paying users where cancel_intent_signal.intent_level is 'interacting' or 'committing' AND subscription is still active (not yet cancelled — once cancelled, post-cancel-winback takes over). Excludes users on trial (different motion) and users who have already received a cancel-save offer in last 90 days (no spam).
      prompt: Build a segment 'Cancel-intent active' capturing paying users where cancel_intent_signal.intent_level is 'interacting' or 'committing' AND subscription is still active (not yet cancelled — once cancelled, post-cancel-winback takes over). Excludes users on trial (different motion) and users who have already received a cancel-save offer in last 90 days (no spam).
    - step: 3
      title: Build Save-Offer Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - cancel_intent
      - segment
      description: 'Generate branched save-offer content per cancel reason. (a) Price reason: offer 20% retention discount for 3 months OR downgrade-to-lighter-plan option; (b) Unused reason: offer 60-day pause OR a 1:1 onboarding call to drive activation; (c) Competitor reason: offer a 1:1 call with PM to address feature gaps + competitive comparison sheet; (d) Feature-gap reason: roadmap visibility for the specific missing feature + interim workaround; (e) Pause-needed reason: 1-click pause for up to 90 days (preserves data); (f) Other/no-reason: ask ''what would have made you stay?'' + offer 1:1 call. Send-from: the customer''s CSM if assigned, else success@ address.'
      prompt: 'Generate branched save-offer content per cancel reason. (a) Price reason: offer 20% retention discount for 3 months OR downgrade-to-lighter-plan option; (b) Unused reason: offer 60-day pause OR a 1:1 onboarding call to drive activation; (c) Competitor reason: offer a 1:1 call with PM to address feature gaps + competitive comparison sheet; (d) Feature-gap reason: roadmap visibility for the specific missing feature + interim workaround; (e) Pause-needed reason: 1-click pause for up to 90 days (preserves data); (f) Other/no-reason: ask ''what would have made you stay?'' + offer 1:1 call. Send-from: the customer''s CSM if assigned, else success@ address.'
    - step: 4
      title: Build Save Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - cancel_intent
      - segment
      - asset
      description: 'Build a branched journey triggered when cancel_intent_signal becomes ''interacting'' or ''committing''. Branch on stated_reason — each user gets ONE save offer matched to their stated reason. Touch 1 (within 1 hour of intent signal): the matched save offer email. Touch 2 (Day 2, if no engagement): softer follow-up reinforcing the offer. For high-LTV customers (top 10% by ARR), additionally create urgent CSM task at intent detection — human save attempt parallel to email. Exit on: save_offer_accepted (recorded as retention_win event), subscription_canceled (proceed to post-cancel-winback), or 14-day timeout.'
      prompt: 'Build a branched journey triggered when cancel_intent_signal becomes ''interacting'' or ''committing''. Branch on stated_reason — each user gets ONE save offer matched to their stated reason. Touch 1 (within 1 hour of intent signal): the matched save offer email. Touch 2 (Day 2, if no engagement): softer follow-up reinforcing the offer. For high-LTV customers (top 10% by ARR), additionally create urgent CSM task at intent detection — human save attempt parallel to email. Exit on: save_offer_accepted (recorded as retention_win event), subscription_canceled (proceed to post-cancel-winback), or 14-day timeout.'
    - step: 5
      title: Build Save-Flow Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - cancel_intent
      - segment
      - asset
      - journey
      description: 'Compose a save-flow dashboard: cancel-intent volume by week, save rate (intent users who DON''T cancel within 30 days), save rate by stated reason (which save offers actually work), save rate by offer type (discount vs. pause vs. downgrade vs. 1:1 call — informs offer strategy), and ARR saved this quarter. Also surface: stated cancel reasons distribution (voice-of-customer for product/pricing teams) and cohorts where save attempts fail consistently (deep churn signal — those segments need product fixes, not save offers).'
      prompt: 'Compose a save-flow dashboard: cancel-intent volume by week, save rate (intent users who DON''T cancel within 30 days), save rate by stated reason (which save offers actually work), save rate by offer type (discount vs. pause vs. downgrade vs. 1:1 call — informs offer strategy), and ARR saved this quarter. Also surface: stated cancel reasons distribution (voice-of-customer for product/pricing teams) and cohorts where save attempts fail consistently (deep churn signal — those segments need product fixes, not save offers).'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Pre Cancellation Save

## Procedure

1. **Build Cancel-Intent Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'cancel_intent_signal' on the User object. Computed in real-time. Inputs: (a) visited /cancel or /downgrade page in last 14 days; (b) clicked 'cancel subscription' button (which triggers cancel-modal not cancellation); (c) submitted cancel reason in cancel-flow form without confirming. Output: object with intent_level (browsing / interacting / committing), stated_reason if captured (price / unused / competitor / feature-gap / pause-needed / other), and timestamp. The signal expires after 7 days of no further activity. → produces: attribute
2. **Identify Cancel-Intent Users** [`create_segment`] — Build a segment 'Cancel-intent active' capturing paying users where cancel_intent_signal.intent_level is 'interacting' or 'committing' AND subscription is still active (not yet cancelled — once cancelled, post-cancel-winback takes over). Excludes users on trial (different motion) and users who have already received a cancel-save offer in last 90 days (no spam). → produces: segment
3. **Build Save-Offer Content** [`create_email_content`] — Generate branched save-offer content per cancel reason. (a) Price reason: offer 20% retention discount for 3 months OR downgrade-to-lighter-plan option; (b) Unused reason: offer 60-day pause OR a 1:1 onboarding call to drive activation; (c) Competitor reason: offer a 1:1 call with PM to address feature gaps + competitive comparison sheet; (d) Feature-gap reason: roadmap visibility for the specific missing feature + interim workaround; (e) Pause-needed reason: 1-click pause for up to 90 days (preserves data); (f) Other/no-reason: ask 'what would have made you stay?' + offer 1:1 call. Send-from: the customer's CSM if assigned, else success@ address. → produces: asset
4. **Build Save Journey** [`create_journey`] — Build a branched journey triggered when cancel_intent_signal becomes 'interacting' or 'committing'. Branch on stated_reason — each user gets ONE save offer matched to their stated reason. Touch 1 (within 1 hour of intent signal): the matched save offer email. Touch 2 (Day 2, if no engagement): softer follow-up reinforcing the offer. For high-LTV customers (top 10% by ARR), additionally create urgent CSM task at intent detection — human save attempt parallel to email. Exit on: save_offer_accepted (recorded as retention_win event), subscription_canceled (proceed to post-cancel-winback), or 14-day timeout. → produces: journey
5. **Build Save-Flow Dashboard** [`create_dashboard`] — Compose a save-flow dashboard: cancel-intent volume by week, save rate (intent users who DON'T cancel within 30 days), save rate by stated reason (which save offers actually work), save rate by offer type (discount vs. pause vs. downgrade vs. 1:1 call — informs offer strategy), and ARR saved this quarter. Also surface: stated cancel reasons distribution (voice-of-customer for product/pricing teams) and cohorts where save attempts fail consistently (deep churn signal — those segments need product fixes, not save offers). → produces: dashboard
