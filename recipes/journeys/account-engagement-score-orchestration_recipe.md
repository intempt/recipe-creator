---
name: account-engagement-score-orchestration
description: 'Use when a user mentions "account engagement score orchestration", "B2B account scoring journey", "tiered account engagement", or asks for related help. B2B account-level engagement scoring (aggregate user activity rolled up to account) → tiered account journeys: green accounts get expansion-leaning content, yellow get reactivation, red get save-flow + CSM task, dormant get win-back. Adobe CJA B2B-style account-as-unit pattern.'
arguments: []
intempt:
  id: account-engagement-score-orchestration
  version: 1.0.0
  slashCommand: /account-engagement-score-orchestration
  group: Journeys
  shortDescription: "'B2B account-level engagement scoring (aggregate user activity rolled up to account) → tiered account journeys: green accounts get expansion-leaning content, yellow get reactivation, red get save-flow + CSM task, dormant get win-back. Adobe CJA B2B-style account-as-unit pattern.'"
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [account-engagement, b2b-tiering, account-as-unit]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_personalization
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Account Engagement Score Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: account_engagement
      description: 'Create an AI-derived attribute ''account_engagement_score'' on the Account object, refreshed daily. Aggregates ACROSS all users at the account: (a) active-user ratio (active users / total seats); (b) engagement velocity (sessions/events trending up or down at account level); (c) feature breadth (count of features used by anyone at the account); (d) stakeholder distribution (engagement coming from multiple roles vs. single-user dependence); (e) sentiment signals from support tickets. Output: numeric 0-100 with tier — green (75-100 healthy growing) / yellow (40-74 stable but warning signs) / red (15-39 declining quickly) / dormant (<15 effectively inactive). The account-as-unit aggregation is the differentiator — most CDPs score users, this scores the buying entity.'
      prompt: 'Create an AI-derived attribute ''account_engagement_score'' on the Account object, refreshed daily. Aggregates ACROSS all users at the account: (a) active-user ratio (active users / total seats); (b) engagement velocity (sessions/events trending up or down at account level); (c) feature breadth (count of features used by anyone at the account); (d) stakeholder distribution (engagement coming from multiple roles vs. single-user dependence); (e) sentiment signals from support tickets. Output: numeric 0-100 with tier — green (75-100 healthy growing) / yellow (40-74 stable but warning signs) / red (15-39 declining quickly) / dormant (<15 effectively inactive). The account-as-unit aggregation is the differentiator — most CDPs score users, this scores the buying entity.'
    - step: 2
      title: Identify Tiered Accounts
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - account_engagement
      description: Build a segment 'B2B accounts tiered by engagement' capturing all paying B2B accounts, partitioned by account_engagement_score tier. Refreshed daily. Excludes accounts <30 days old (need history) and accounts in active sales-led save-flows (avoid double-orchestration). The journey routes from this segment based on tier.
      prompt: Build a segment 'B2B accounts tiered by engagement' capturing all paying B2B accounts, partitioned by account_engagement_score tier. Refreshed daily. Excludes accounts <30 days old (need history) and accounts in active sales-led save-flows (avoid double-orchestration). The journey routes from this segment based on tier.
    - step: 3
      title: Build Per-Tier Content Variants
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - account_engagement
      - segment
      description: 'Generate per-tier email content. GREEN — expansion-leaning content sent to champion: ''Your team is in the top 25% of [Product] users — here''s what high-growth accounts do next.'' Plus subtle expansion CTA. YELLOW — reactivation content sent to admin: ''Noticing a few of your team members aren''t logging in as often — want help re-engaging the team?'' With a CSM-meeting CTA. RED — urgent personalized content sent to admin + executive sponsor: ''Your team''s engagement has shifted — we''d like to understand what''s going on. 15-minute call?'' Direct CSM offer. DORMANT — last-chance content sent to champion: ''It''s been a while — we miss you. Here''s what''s new since you last logged in.'' With a fresh-start onboarding offer.'
      prompt: 'Generate per-tier email content. GREEN — expansion-leaning content sent to champion: ''Your team is in the top 25% of [Product] users — here''s what high-growth accounts do next.'' Plus subtle expansion CTA. YELLOW — reactivation content sent to admin: ''Noticing a few of your team members aren''t logging in as often — want help re-engaging the team?'' With a CSM-meeting CTA. RED — urgent personalized content sent to admin + executive sponsor: ''Your team''s engagement has shifted — we''d like to understand what''s going on. 15-minute call?'' Direct CSM offer. DORMANT — last-chance content sent to champion: ''It''s been a while — we miss you. Here''s what''s new since you last logged in.'' With a fresh-start onboarding offer.'
    - step: 4
      title: Build Account Personalization Surface
      command: create_personalization
      produces: personalization
      bindsAs: personalization
      dependsOn:
      - account_engagement
      - segment
      description: 'Configure an in-app personalization on the admin dashboard that varies by account tier. Green: shows expansion roadmap + power-features for healthy growth. Yellow: shows team-engagement health stats + ''invite team members'' nudges + use-case templates relevant to slow-adoption rescue. Red: shows direct-CSM-connect button + ''troubleshoot setup'' resources prominently. Dormant: doesn''t render account-engagement personalization (won''t help — the user isn''t logging in anyway; reach them via email instead).'
      prompt: 'Configure an in-app personalization on the admin dashboard that varies by account tier. Green: shows expansion roadmap + power-features for healthy growth. Yellow: shows team-engagement health stats + ''invite team members'' nudges + use-case templates relevant to slow-adoption rescue. Red: shows direct-CSM-connect button + ''troubleshoot setup'' resources prominently. Dormant: doesn''t render account-engagement personalization (won''t help — the user isn''t logging in anyway; reach them via email instead).'
    - step: 5
      title: Build Tiered Account Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - account_engagement
      - segment
      - email_asset
      - personalization
      description: 'Build a tiered journey wired to account-engagement-tiered segment. Branch on account_engagement tier at entry AND re-evaluate weekly. GREEN: Touch 1 monthly — expansion-leaning content to champion. Personalization activates for admin. Touch 2 quarterly — handoff to customer-progress-business-case journey. YELLOW: Touch 1 Day 0 — reactivation content to admin. Touch 2 Day 7 — CSM task to reach out if score hasn''t recovered. RED: Touch 1 Day 0 — urgent content + CSM task SAME-DAY. Touch 2 Day 3 — executive-sponsor task if no CSM contact made. DORMANT: Touch 1 Day 0 — last-chance email. Touch 2 Day 14 — final outreach + warning before suppression. Exit on: tier escalation back to green (recovered — log retention_win), subscription_canceled (handoff to post-cancel-winback), or sustained dormancy 60+ days (suppress).'
      prompt: 'Build a tiered journey wired to account-engagement-tiered segment. Branch on account_engagement tier at entry AND re-evaluate weekly. GREEN: Touch 1 monthly — expansion-leaning content to champion. Personalization activates for admin. Touch 2 quarterly — handoff to customer-progress-business-case journey. YELLOW: Touch 1 Day 0 — reactivation content to admin. Touch 2 Day 7 — CSM task to reach out if score hasn''t recovered. RED: Touch 1 Day 0 — urgent content + CSM task SAME-DAY. Touch 2 Day 3 — executive-sponsor task if no CSM contact made. DORMANT: Touch 1 Day 0 — last-chance email. Touch 2 Day 14 — final outreach + warning before suppression. Exit on: tier escalation back to green (recovered — log retention_win), subscription_canceled (handoff to post-cancel-winback), or sustained dormancy 60+ days (suppress).'
    - step: 6
      title: Build Account Engagement Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - account_engagement
      - segment
      - email_asset
      - personalization
      - journey
      description: 'Compose an account-engagement dashboard: tier distribution across the book of business (green/yellow/red/dormant proportions — the health-of-business snapshot), tier-migration trends week-over-week (which direction are accounts moving), ARR-weighted at-risk pile (red + dormant tier sum), red-tier-to-recovered conversion rate (proof the intervention works), and per-CSM tier distribution (some CSMs handle red-heavy portfolios — informs workload balancing). The strategic NRR view for leadership.'
      prompt: 'Compose an account-engagement dashboard: tier distribution across the book of business (green/yellow/red/dormant proportions — the health-of-business snapshot), tier-migration trends week-over-week (which direction are accounts moving), ARR-weighted at-risk pile (red + dormant tier sum), red-tier-to-recovered conversion rate (proof the intervention works), and per-CSM tier distribution (some CSMs handle red-heavy portfolios — informs workload balancing). The strategic NRR view for leadership.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: personalization, type: personalization, cardinality: single, description: "Personalization produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Account Engagement Score Orchestration

## Procedure

1. **Build Account Engagement Score Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'account_engagement_score' on the Account object, refreshed daily. Aggregates ACROSS all users at the account: (a) active-user ratio (active users / total seats); (b) engagement velocity (sessions/events trending up or down at account level); (c) feature breadth (count of features used by anyone at the account); (d) stakeholder distribution (engagement coming from multiple roles vs. single-user dependence); (e) sentiment signals from support tickets. Output: numeric 0-100 with tier — green (75-100 healthy growing) / yellow (40-74 stable but warning signs) / red (15-39 declining quickly) / dormant (<15 effectively inactive). The account-as-unit aggregation is the differentiator — most CDPs score users, this scores the buying entity. → produces: attribute
2. **Identify Tiered Accounts** [`create_segment`] — Build a segment 'B2B accounts tiered by engagement' capturing all paying B2B accounts, partitioned by account_engagement_score tier. Refreshed daily. Excludes accounts <30 days old (need history) and accounts in active sales-led save-flows (avoid double-orchestration). The journey routes from this segment based on tier. → produces: segment
3. **Build Per-Tier Content Variants** [`create_email_content`] — Generate per-tier email content. GREEN — expansion-leaning content sent to champion: 'Your team is in the top 25% of [Product] users — here's what high-growth accounts do next.' Plus subtle expansion CTA. YELLOW — reactivation content sent to admin: 'Noticing a few of your team members aren't logging in as often — want help re-engaging the team?' With a CSM-meeting CTA. RED — urgent personalized content sent to admin + executive sponsor: 'Your team's engagement has shifted — we'd like to understand what's going on. 15-minute call?' Direct CSM offer. DORMANT — last-chance content sent to champion: 'It's been a while — we miss you. Here's what's new since you last logged in.' With a fresh-start onboarding offer. → produces: asset
4. **Build Account Personalization Surface** [`create_personalization`] — Configure an in-app personalization on the admin dashboard that varies by account tier. Green: shows expansion roadmap + power-features for healthy growth. Yellow: shows team-engagement health stats + 'invite team members' nudges + use-case templates relevant to slow-adoption rescue. Red: shows direct-CSM-connect button + 'troubleshoot setup' resources prominently. Dormant: doesn't render account-engagement personalization (won't help — the user isn't logging in anyway; reach them via email instead). → produces: personalization
5. **Build Tiered Account Journey** [`create_journey`] — Build a tiered journey wired to account-engagement-tiered segment. Branch on account_engagement tier at entry AND re-evaluate weekly. GREEN: Touch 1 monthly — expansion-leaning content to champion. Personalization activates for admin. Touch 2 quarterly — handoff to customer-progress-business-case journey. YELLOW: Touch 1 Day 0 — reactivation content to admin. Touch 2 Day 7 — CSM task to reach out if score hasn't recovered. RED: Touch 1 Day 0 — urgent content + CSM task SAME-DAY. Touch 2 Day 3 — executive-sponsor task if no CSM contact made. DORMANT: Touch 1 Day 0 — last-chance email. Touch 2 Day 14 — final outreach + warning before suppression. Exit on: tier escalation back to green (recovered — log retention_win), subscription_canceled (handoff to post-cancel-winback), or sustained dormancy 60+ days (suppress). → produces: journey
6. **Build Account Engagement Dashboard** [`create_dashboard`] — Compose an account-engagement dashboard: tier distribution across the book of business (green/yellow/red/dormant proportions — the health-of-business snapshot), tier-migration trends week-over-week (which direction are accounts moving), ARR-weighted at-risk pile (red + dormant tier sum), red-tier-to-recovered conversion rate (proof the intervention works), and per-CSM tier distribution (some CSMs handle red-heavy portfolios — informs workload balancing). The strategic NRR view for leadership. → produces: dashboard
