---
name: post-cancel-winback
description: Use when a user mentions "post-cancel winback", "after cancel winback", "30/60/90 day winback sequence", or asks for related help. After a user cancels, fire a 30/60/90-day winback sequence — staggered re-engagement at increasing intervals with product updates, win-back incentives, and a final 'one last try' message — to recover formerly-paying customers.
arguments: []
intempt:
  id: post-cancel-winback
  version: 1.0.0
  slashCommand: /post-cancel-winback
  group: Journeys
  shortDescription: 'After a user cancels, fire a 30/60/90-day winback sequence (staggered re-engagement at increasing intervals with product updates, win-back incentives, and a final ''one last try'' message) to recover formerly-paying customers.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: standard
    executionMode: live
    tags: [winback, post-cancel, lapsed-customer]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: subscription_canceled, severity: blocking }
  invokesCommands:
    - create_segment
    - create_email_content
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Identify Recently Cancelled Users
      command: create_segment
      produces: segment
      bindsAs: segment
      description: Build a segment 'Recently cancelled - last 120 days' capturing users with subscription_canceled in the last 30-120 days AND cancel_reason is NOT 'wrong-fit' or 'company-shutdown' (those won't winback). Excludes users who have already won back (subscribed again) and users who explicitly requested no-marketing in cancel form.
      prompt: Build a segment 'Recently cancelled - last 120 days' capturing users with subscription_canceled in the last 30-120 days AND cancel_reason is NOT 'wrong-fit' or 'company-shutdown' (those won't winback). Excludes users who have already won back (subscribed again) and users who explicitly requested no-marketing in cancel form.
    - step: 2
      title: Build Winback Email Content
      command: create_email_content
      produces: asset
      bindsAs: asset
      dependsOn:
      - segment
      description: 'Generate 3-touch winback email content. Touch 1 (Day 30 after cancel): ''A lot has changed since you left — here''s what''s new.'' Lead with 2-3 specific product improvements shipped post-cancel, relevant to their stated cancel reason. Touch 2 (Day 60): ''Come back for [N] months at 50% off'' — winback discount offer. Personalize the call-out with their prior use case if known. Touch 3 (Day 90, final): ''One last invitation'' — softer, more emotional appeal — acknowledges you understand they left for a reason, mentions a free 30-day reactivation try (no charge until they confirm) as the final lever. Send-from: their original CSM if known, else success@ address.'
      prompt: 'Generate 3-touch winback email content. Touch 1 (Day 30 after cancel): ''A lot has changed since you left — here''s what''s new.'' Lead with 2-3 specific product improvements shipped post-cancel, relevant to their stated cancel reason. Touch 2 (Day 60): ''Come back for [N] months at 50% off'' — winback discount offer. Personalize the call-out with their prior use case if known. Touch 3 (Day 90, final): ''One last invitation'' — softer, more emotional appeal — acknowledges you understand they left for a reason, mentions a free 30-day reactivation try (no charge until they confirm) as the final lever. Send-from: their original CSM if known, else success@ address.'
    - step: 3
      title: Build Winback Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - segment
      - asset
      description: 'Build a 3-touch journey triggered when subscription_canceled fired 30+ days ago. Touch 1: Day 30. Touch 2: Day 60. Touch 3: Day 90. Each touch personalized using the prior account context (cancel reason, plan, last-used features). Exit on: subscription_created (won back — record winback_won event), email_replied (warm handoff to sales), unsubscribe, or 120-day timeout (after which user moves to long-term lapsed nurture, separate motion).'
      prompt: 'Build a 3-touch journey triggered when subscription_canceled fired 30+ days ago. Touch 1: Day 30. Touch 2: Day 60. Touch 3: Day 90. Each touch personalized using the prior account context (cancel reason, plan, last-used features). Exit on: subscription_created (won back — record winback_won event), email_replied (warm handoff to sales), unsubscribe, or 120-day timeout (after which user moves to long-term lapsed nurture, separate motion).'
    - step: 4
      title: Build Winback Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - segment
      - asset
      - journey
      description: 'Compose a winback dashboard: post-cancel winback rate (% of cancellers who re-subscribe within 90 days — baseline benchmark is 5-10%), winback rate by touch (which touch is actually driving recoveries), winback rate by original cancel reason (informs which reasons are recoverable vs. final), ARR recovered via winback this quarter, and time-to-winback distribution (most winbacks happen in the first 60 days; users dormant 90+ days rarely return without a major external trigger).'
      prompt: 'Compose a winback dashboard: post-cancel winback rate (% of cancellers who re-subscribe within 90 days — baseline benchmark is 5-10%), winback rate by touch (which touch is actually driving recoveries), winback rate by original cancel reason (informs which reasons are recoverable vs. final), ARR recovered via winback this quarter, and time-to-winback distribution (most winbacks happen in the first 60 days; users dormant 90+ days rarely return without a major external trigger).'
  outputs:
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Post Cancel Winback

## Procedure

1. **Identify Recently Cancelled Users** [`create_segment`] — Build a segment 'Recently cancelled - last 120 days' capturing users with subscription_canceled in the last 30-120 days AND cancel_reason is NOT 'wrong-fit' or 'company-shutdown' (those won't winback). Excludes users who have already won back (subscribed again) and users who explicitly requested no-marketing in cancel form. → produces: segment
2. **Build Winback Email Content** [`create_email_content`] — Generate 3-touch winback email content. Touch 1 (Day 30 after cancel): 'A lot has changed since you left — here's what's new.' Lead with 2-3 specific product improvements shipped post-cancel, relevant to their stated cancel reason. Touch 2 (Day 60): 'Come back for [N] months at 50% off' — winback discount offer. Personalize the call-out with their prior use case if known. Touch 3 (Day 90, final): 'One last invitation' — softer, more emotional appeal — acknowledges you understand they left for a reason, mentions a free 30-day reactivation try (no charge until they confirm) as the final lever. Send-from: their original CSM if known, else success@ address. → produces: asset
3. **Build Winback Journey** [`create_journey`] — Build a 3-touch journey triggered when subscription_canceled fired 30+ days ago. Touch 1: Day 30. Touch 2: Day 60. Touch 3: Day 90. Each touch personalized using the prior account context (cancel reason, plan, last-used features). Exit on: subscription_created (won back — record winback_won event), email_replied (warm handoff to sales), unsubscribe, or 120-day timeout (after which user moves to long-term lapsed nurture, separate motion). → produces: journey
4. **Build Winback Dashboard** [`create_dashboard`] — Compose a winback dashboard: post-cancel winback rate (% of cancellers who re-subscribe within 90 days — baseline benchmark is 5-10%), winback rate by touch (which touch is actually driving recoveries), winback rate by original cancel reason (informs which reasons are recoverable vs. final), ARR recovered via winback this quarter, and time-to-winback distribution (most winbacks happen in the first 60 days; users dormant 90+ days rarely return without a major external trigger). → produces: dashboard
