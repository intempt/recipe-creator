---
name: predictive-churn-tiered-intervention
description: Use when a user mentions "predictive churn tiered intervention", "churn risk tiered routing", "AI churn save", or asks for related help. Predictive churn-risk AI attribute with nuanced scores routes users to one of four intervention tiers — low gets nurture content, medium gets personalized in-app + email, high gets CSM task + recommendation surface, critical gets agent handoff + exec-sponsor task — the CleverTap-style differentiated churn rescue.
arguments: []
intempt:
  id: predictive-churn-tiered-intervention
  version: 1.0.0
  slashCommand: /predictive-churn-tiered-intervention
  group: Journeys
  shortDescription: 'Predictive churn-risk AI attribute with nuanced scores routes users to one of four intervention tiers (low gets nurture content, medium gets personalized in-app + email, high gets CSM task + recommendation surface, critical gets agent handoff + exec-sponsor task), the CleverTap-style differentiated churn rescue.'
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [saas]
    complexity: advanced
    executionMode: live
    tags: [churn-prevention, tiered-intervention, predictive]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: session_start, severity: blocking }
      - { value: feature_used, severity: recommended }
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_page_content
    - create_recommendation
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Churn-Risk AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: churn_risk
      description: 'Create an AI-derived attribute ''churn_risk_score'' on the User object, refreshed daily. Inputs: engagement velocity (sessions trend over 30/14/7 days), feature usage decay, support sentiment trajectory, billing-status signals, peer-cohort churn patterns, account-level usage (for B2B). Output: numeric 0-100 with tier label — low (0-29) / medium (30-59) / high (60-79) / critical (80-100). NOT binary at-risk-or-not — the nuance is the point: medium and high get different treatments. Refresh on every significant behavioral event so a sudden engagement drop is caught fast.'
      prompt: 'Create an AI-derived attribute ''churn_risk_score'' on the User object, refreshed daily. Inputs: engagement velocity (sessions trend over 30/14/7 days), feature usage decay, support sentiment trajectory, billing-status signals, peer-cohort churn patterns, account-level usage (for B2B). Output: numeric 0-100 with tier label — low (0-29) / medium (30-59) / high (60-79) / critical (80-100). NOT binary at-risk-or-not — the nuance is the point: medium and high get different treatments. Refresh on every significant behavioral event so a sudden engagement drop is caught fast.'
    - step: 2
      title: Identify Tiered Risk Cohorts
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - churn_risk
      description: Build a parent segment 'Churn risk - paying users' capturing all paying users with churn_risk_score >= 30. Implicitly partitioned by tier through the attribute. Excludes users in the first 14 days (early signals aren't reliable yet) and users already in active save flows (no double-intervention).
      prompt: Build a parent segment 'Churn risk - paying users' capturing all paying users with churn_risk_score >= 30. Implicitly partitioned by tier through the attribute. Excludes users in the first 14 days (early signals aren't reliable yet) and users already in active save flows (no double-intervention).
    - step: 3
      title: Build Tier Content Variants
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - churn_risk
      - segment
      description: 'Generate per-tier email content. Medium tier: educational content matched to underutilized features that drive retention in their cohort + personalized ''pick up where you left off'' deep-link. Tone: helpful, not alarmed. High tier: urgent value reinforcement, CSM availability signal, specific use-case help offer (''Want a 15-min walkthrough on [feature]?''). Critical tier: founder/CEO personal letter (''I noticed your account hasn''t been used much — anything we can do?''), with direct calendar link and concrete asks. Send-from: success@ for medium, named CSM for high, founder/CEO for critical.'
      prompt: 'Generate per-tier email content. Medium tier: educational content matched to underutilized features that drive retention in their cohort + personalized ''pick up where you left off'' deep-link. Tone: helpful, not alarmed. High tier: urgent value reinforcement, CSM availability signal, specific use-case help offer (''Want a 15-min walkthrough on [feature]?''). Critical tier: founder/CEO personal letter (''I noticed your account hasn''t been used much — anything we can do?''), with direct calendar link and concrete asks. Send-from: success@ for medium, named CSM for high, founder/CEO for critical.'
    - step: 4
      title: Build In-App Save Content
      command: create_page_content
      produces: asset
      bindsAs: inapp_asset
      dependsOn:
      - churn_risk
      - segment
      - email_asset
      description: 'Generate in-app messages for high-tier users when they DO log in (rare and precious moments). Format: contextual banner referencing their most-likely-success-path (''Most users in your segment succeed by trying [feature] — want a 60-second walkthrough?''). For critical-tier users on rare logins: a personal-touch interrupt — full-screen modal from the CSM or founder offering a 1:1 call. Never blanket — only when AI signal is strong.'
      prompt: 'Generate in-app messages for high-tier users when they DO log in (rare and precious moments). Format: contextual banner referencing their most-likely-success-path (''Most users in your segment succeed by trying [feature] — want a 60-second walkthrough?''). For critical-tier users on rare logins: a personal-touch interrupt — full-screen modal from the CSM or founder offering a 1:1 call. Never blanket — only when AI signal is strong.'
    - step: 5
      title: Build Retention Recommendation Surface
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - churn_risk
      - segment
      description: 'Configure a recommendation surface specifically for high+critical tier users: surfaces underutilized features that THIS user''s cohort uses successfully but THIS user has not adopted (the ''features-that-stick-users'' pattern). Renders in-app on dashboard, in email content blocks, and on personalization slots when the user does visit. The recommendation logic prioritizes features with high retention-correlation in this user''s segment.'
      prompt: 'Configure a recommendation surface specifically for high+critical tier users: surfaces underutilized features that THIS user''s cohort uses successfully but THIS user has not adopted (the ''features-that-stick-users'' pattern). Renders in-app on dashboard, in email content blocks, and on personalization slots when the user does visit. The recommendation logic prioritizes features with high retention-correlation in this user''s segment.'
    - step: 6
      title: Build Tiered Churn Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - churn_risk
      - segment
      - email_asset
      - inapp_asset
      - rec_surface
      description: 'Build a tiered journey wired to the churn-risk segment. Branch on churn_risk tier at entry AND re-evaluate weekly: LOW tier — light-touch nurture email at Day 7 (no urgency, just value content). MEDIUM tier — Touch 1 email Day 0 (helpful tip), Touch 2 in-app at next login (deep-link to retention feature), Touch 3 email Day 7 with recommendation surface highlighting cohort-success features. HIGH tier — Touch 1 email Day 0 from CSM with offer of help, in-app urgent banner on next session, CSM task created same-day. CRITICAL tier — within 4 hours: founder/CEO personal email + agent handoff offering 1:1 call + urgent CSM task + executive-sponsor task. Tier RECOMPUTED weekly — users de-escalate (engagement returned) exit gracefully; users escalate get tier-appropriate next-touch. Exit on: churn_risk drops below 30 for 14+ days (recovered — log retention_win), subscription_canceled (handoff to post-cancel-winback), or unsubscribe.'
      prompt: 'Build a tiered journey wired to the churn-risk segment. Branch on churn_risk tier at entry AND re-evaluate weekly: LOW tier — light-touch nurture email at Day 7 (no urgency, just value content). MEDIUM tier — Touch 1 email Day 0 (helpful tip), Touch 2 in-app at next login (deep-link to retention feature), Touch 3 email Day 7 with recommendation surface highlighting cohort-success features. HIGH tier — Touch 1 email Day 0 from CSM with offer of help, in-app urgent banner on next session, CSM task created same-day. CRITICAL tier — within 4 hours: founder/CEO personal email + agent handoff offering 1:1 call + urgent CSM task + executive-sponsor task. Tier RECOMPUTED weekly — users de-escalate (engagement returned) exit gracefully; users escalate get tier-appropriate next-touch. Exit on: churn_risk drops below 30 for 14+ days (recovered — log retention_win), subscription_canceled (handoff to post-cancel-winback), or unsubscribe.'
    - step: 7
      title: Build Tiered-Churn Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - churn_risk
      - segment
      - email_asset
      - inapp_asset
      - rec_surface
      - journey
      description: 'Compose a tiered churn intervention dashboard: distribution of users across tiers (low/medium/high/critical) per week — leading indicator of book-of-business health, tier-level save rate (% of users in each tier who exit risk vs. churn — proves tiered strategy works), critical-tier CSM response SLA (target: <4hr for human-touch start), ARR-weighted save value by tier, and tier-migration tracking (high → medium = success, medium → high = early warning). Compare model accuracy: predicted churn vs. actual churn at 30/60/90 days.'
      prompt: 'Compose a tiered churn intervention dashboard: distribution of users across tiers (low/medium/high/critical) per week — leading indicator of book-of-business health, tier-level save rate (% of users in each tier who exit risk vs. churn — proves tiered strategy works), critical-tier CSM response SLA (target: <4hr for human-touch start), ARR-weighted save value by tier, and tier-migration tracking (high → medium = success, medium → high = early warning). Compare model accuracy: predicted churn vs. actual churn at 30/60/90 days.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Predictive Churn Tiered Intervention

## Procedure

1. **Build Churn-Risk AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'churn_risk_score' on the User object, refreshed daily. Inputs: engagement velocity (sessions trend over 30/14/7 days), feature usage decay, support sentiment trajectory, billing-status signals, peer-cohort churn patterns, account-level usage (for B2B). Output: numeric 0-100 with tier label — low (0-29) / medium (30-59) / high (60-79) / critical (80-100). NOT binary at-risk-or-not — the nuance is the point: medium and high get different treatments. Refresh on every significant behavioral event so a sudden engagement drop is caught fast. → produces: attribute
2. **Identify Tiered Risk Cohorts** [`create_segment`] — Build a parent segment 'Churn risk - paying users' capturing all paying users with churn_risk_score >= 30. Implicitly partitioned by tier through the attribute. Excludes users in the first 14 days (early signals aren't reliable yet) and users already in active save flows (no double-intervention). → produces: segment
3. **Build Tier Content Variants** [`create_email_content`] — Generate per-tier email content. Medium tier: educational content matched to underutilized features that drive retention in their cohort + personalized 'pick up where you left off' deep-link. Tone: helpful, not alarmed. High tier: urgent value reinforcement, CSM availability signal, specific use-case help offer ('Want a 15-min walkthrough on [feature]?'). Critical tier: founder/CEO personal letter ('I noticed your account hasn't been used much — anything we can do?'), with direct calendar link and concrete asks. Send-from: success@ for medium, named CSM for high, founder/CEO for critical. → produces: asset
4. **Build In-App Save Content** [`create_page_content`] — Generate in-app messages for high-tier users when they DO log in (rare and precious moments). Format: contextual banner referencing their most-likely-success-path ('Most users in your segment succeed by trying [feature] — want a 60-second walkthrough?'). For critical-tier users on rare logins: a personal-touch interrupt — full-screen modal from the CSM or founder offering a 1:1 call. Never blanket — only when AI signal is strong. → produces: asset
5. **Build Retention Recommendation Surface** [`create_recommendation`] — Configure a recommendation surface specifically for high+critical tier users: surfaces underutilized features that THIS user's cohort uses successfully but THIS user has not adopted (the 'features-that-stick-users' pattern). Renders in-app on dashboard, in email content blocks, and on personalization slots when the user does visit. The recommendation logic prioritizes features with high retention-correlation in this user's segment. → produces: recommendation
6. **Build Tiered Churn Journey** [`create_journey`] — Build a tiered journey wired to the churn-risk segment. Branch on churn_risk tier at entry AND re-evaluate weekly: LOW tier — light-touch nurture email at Day 7 (no urgency, just value content). MEDIUM tier — Touch 1 email Day 0 (helpful tip), Touch 2 in-app at next login (deep-link to retention feature), Touch 3 email Day 7 with recommendation surface highlighting cohort-success features. HIGH tier — Touch 1 email Day 0 from CSM with offer of help, in-app urgent banner on next session, CSM task created same-day. CRITICAL tier — within 4 hours: founder/CEO personal email + agent handoff offering 1:1 call + urgent CSM task + executive-sponsor task. Tier RECOMPUTED weekly — users de-escalate (engagement returned) exit gracefully; users escalate get tier-appropriate next-touch. Exit on: churn_risk drops below 30 for 14+ days (recovered — log retention_win), subscription_canceled (handoff to post-cancel-winback), or unsubscribe. → produces: journey
7. **Build Tiered-Churn Dashboard** [`create_dashboard`] — Compose a tiered churn intervention dashboard: distribution of users across tiers (low/medium/high/critical) per week — leading indicator of book-of-business health, tier-level save rate (% of users in each tier who exit risk vs. churn — proves tiered strategy works), critical-tier CSM response SLA (target: <4hr for human-touch start), ARR-weighted save value by tier, and tier-migration tracking (high → medium = success, medium → high = early warning). Compare model accuracy: predicted churn vs. actual churn at 30/60/90 days. → produces: dashboard
