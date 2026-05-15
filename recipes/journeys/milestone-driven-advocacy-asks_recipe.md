---
name: milestone-driven-advocacy-asks
description: Use when a user mentions "milestone advocacy asks", "lifecycle advocacy", "natural advocacy moments", or asks for related help. Detect natural advocacy moments via AI attribute — first value achieved, expansion completed, renewal closed, high-engagement-streak, customer-milestone-hit — fire contextual advocacy ask matched to moment (review / referral / case-study / speaker opportunity). The Captivate Collective Lifecycle Advocacy framework.
arguments: []
intempt:
  id: milestone-driven-advocacy-asks
  version: 1.0.0
  slashCommand: /milestone-driven-advocacy-asks
  group: Journeys
  shortDescription: "Detect natural advocacy moments via AI attribute — first value achieved, expansion completed, renewal closed, high-engagement-streak, customer-milestone-hit — fire contextual advocacy ask matched to moment (review / referral / case-study / speaker opportunity). The Captivate Collective Lifecycle Advocacy framework."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: journey-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [advocacy, lifecycle-marketing, referrals]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  invokesCommands:
    - create_ai_attribute
    - create_segment
    - create_email_content
    - create_recommendation
    - create_journey
    - create_dashboard
  procedure:
    - step: 1
      title: Build Advocacy-Moment AI Attribute
      command: create_ai_attribute
      produces: attribute
      bindsAs: advocacy_moment
      description: 'Create an AI-derived attribute ''active_advocacy_moment'' on the User/Account object. Detects natural advocacy windows (when goodwill is highest). Inputs: (a) first-value-achieved events (key activation milestone), (b) expansion-completed events (account just upgraded), (c) renewal-closed events (just renewed for another term), (d) high-engagement-streak (consecutive weeks of strong activity), (e) customer-success-milestone (reached usage benchmark, completed initial use case), (f) explicit positive support sentiment, (g) NOT during friction or churn-risk. Output: object with moment_type, moment_strength (high/medium), recommended_ask (review / referral / case-study / speaker-opportunity / roadmap-feedback), and ask_recipient_role (champion / economic-buyer / power-user).'
      prompt: 'Create an AI-derived attribute ''active_advocacy_moment'' on the User/Account object. Detects natural advocacy windows (when goodwill is highest). Inputs: (a) first-value-achieved events (key activation milestone), (b) expansion-completed events (account just upgraded), (c) renewal-closed events (just renewed for another term), (d) high-engagement-streak (consecutive weeks of strong activity), (e) customer-success-milestone (reached usage benchmark, completed initial use case), (f) explicit positive support sentiment, (g) NOT during friction or churn-risk. Output: object with moment_type, moment_strength (high/medium), recommended_ask (review / referral / case-study / speaker-opportunity / roadmap-feedback), and ask_recipient_role (champion / economic-buyer / power-user).'
    - step: 2
      title: Identify Advocacy-Ready Users
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - advocacy_moment
      description: Build a segment 'Advocacy-ready' capturing users where active_advocacy_moment is high-strength in the last 7 days AND the user hasn't been asked for an advocacy action in the last 90 days (avoid donor fatigue) AND there's no active friction/churn signal (the timing is genuinely good, not just numerically positive). Partitioned by recommended_ask so the journey routes accordingly.
      prompt: Build a segment 'Advocacy-ready' capturing users where active_advocacy_moment is high-strength in the last 7 days AND the user hasn't been asked for an advocacy action in the last 90 days (avoid donor fatigue) AND there's no active friction/churn signal (the timing is genuinely good, not just numerically positive). Partitioned by recommended_ask so the journey routes accordingly.
    - step: 3
      title: Build Per-Ask Content Variants
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - advocacy_moment
      - segment
      description: 'Generate advocacy-ask email variants per recommended_ask. Review ask: ''You just [hit milestone] — would you share your experience publicly? Takes 3 minutes.'' Includes one-click links to G2, Capterra, or the relevant review site, pre-filled where the platform allows. Referral ask: ''You''re [in top X% of users / just expanded / just renewed] — know anyone who''d benefit from [Product]? Here''s your referral code for [reward].'' Case-study ask: ''Your team''s [specific achievement] is a great story — would you be willing to share it as a customer case study? Our marketing team will do all the writing.'' Speaker-opportunity ask: ''We have a [conference / webinar] coming up — would you be interested in speaking?'' Roadmap-feedback ask: ''You''re using [Product] in such interesting ways — can we get 20 minutes for product roadmap feedback?'' Tone: peer-respectful, never transactional. Send-from: named CSM or success lead, never marketing@.'
      prompt: 'Generate advocacy-ask email variants per recommended_ask. Review ask: ''You just [hit milestone] — would you share your experience publicly? Takes 3 minutes.'' Includes one-click links to G2, Capterra, or the relevant review site, pre-filled where the platform allows. Referral ask: ''You''re [in top X% of users / just expanded / just renewed] — know anyone who''d benefit from [Product]? Here''s your referral code for [reward].'' Case-study ask: ''Your team''s [specific achievement] is a great story — would you be willing to share it as a customer case study? Our marketing team will do all the writing.'' Speaker-opportunity ask: ''We have a [conference / webinar] coming up — would you be interested in speaking?'' Roadmap-feedback ask: ''You''re using [Product] in such interesting ways — can we get 20 minutes for product roadmap feedback?'' Tone: peer-respectful, never transactional. Send-from: named CSM or success lead, never marketing@.'
    - step: 4
      title: Build Advocacy Recommendation Surface
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - advocacy_moment
      - segment
      description: Configure a recommendation surface 'Advocacy opportunities' that activates for advocacy-ready users in the in-app dashboard. Shows the user 2-3 advocacy actions they could take, each with a clear effort estimate ('3 min', '15 min', '1 hour') and what the user gets in return (recognition, referral reward, speaking visibility). Soft-surface — discoverable not interruptive. Lets the user volunteer rather than only being asked.
      prompt: Configure a recommendation surface 'Advocacy opportunities' that activates for advocacy-ready users in the in-app dashboard. Shows the user 2-3 advocacy actions they could take, each with a clear effort estimate ('3 min', '15 min', '1 hour') and what the user gets in return (recognition, referral reward, speaking visibility). Soft-surface — discoverable not interruptive. Lets the user volunteer rather than only being asked.
    - step: 5
      title: Build Advocacy Journey
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - advocacy_moment
      - segment
      - email_asset
      - rec_surface
      description: 'Build a journey wired to advocacy-ready segment. Touch 1 (Day 1 after moment detected): advocacy-ask email matched to recommended_ask. Touch 2 (Day 0 of touch 1): activate recommendation surface in-app. Touch 3 (Day 7, ONLY if user engaged with touch 1 OR rec-surface): light follow-up with concrete next step (''You said you''d love to refer someone — here''s the link to send them''). Branch: if user submits an advocacy action (review left / referral submitted / case-study agreed / etc), tag the user as ''active advocate'' for cross-team awareness AND ensure they''re prioritized for future advocacy opportunities. Exit on: action completed (success — log advocacy_event), explicit decline (respect), or 14-day timeout. No badgering.'
      prompt: 'Build a journey wired to advocacy-ready segment. Touch 1 (Day 1 after moment detected): advocacy-ask email matched to recommended_ask. Touch 2 (Day 0 of touch 1): activate recommendation surface in-app. Touch 3 (Day 7, ONLY if user engaged with touch 1 OR rec-surface): light follow-up with concrete next step (''You said you''d love to refer someone — here''s the link to send them''). Branch: if user submits an advocacy action (review left / referral submitted / case-study agreed / etc), tag the user as ''active advocate'' for cross-team awareness AND ensure they''re prioritized for future advocacy opportunities. Exit on: action completed (success — log advocacy_event), explicit decline (respect), or 14-day timeout. No badgering.'
    - step: 6
      title: Build Advocacy Program Dashboard
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - advocacy_moment
      - segment
      - email_asset
      - rec_surface
      - journey
      description: 'Compose an advocacy program dashboard: advocacy-moment detection volume per week, ask-to-action conversion rate by ask type (which advocacy asks actually convert — referrals usually beat reviews in volume but reviews beat referrals in long-term value), top advocates (users who have completed 3+ advocacy actions — this is the inner-circle list to nurture specially), and downstream attribution (reviews influencing G2 score, referrals creating new pipeline, case studies appearing in sales decks). Reframes CS work from ''retention cost-center'' to ''pipeline contributor''.'
      prompt: 'Compose an advocacy program dashboard: advocacy-moment detection volume per week, ask-to-action conversion rate by ask type (which advocacy asks actually convert — referrals usually beat reviews in volume but reviews beat referrals in long-term value), top advocates (users who have completed 3+ advocacy actions — this is the inner-circle list to nurture specially), and downstream attribution (reviews influencing G2 score, referrals creating new pipeline, case studies appearing in sales decks). Reframes CS work from ''retention cost-center'' to ''pipeline contributor''.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---

# Milestone Driven Advocacy Asks

## Procedure

1. **Build Advocacy-Moment AI Attribute** [`create_ai_attribute`] — Create an AI-derived attribute 'active_advocacy_moment' on the User/Account object. Detects natural advocacy windows (when goodwill is highest). Inputs: (a) first-value-achieved events (key activation milestone), (b) expansion-completed events (account just upgraded), (c) renewal-closed events (just renewed for another term), (d) high-engagement-streak (consecutive weeks of strong activity), (e) customer-success-milestone (reached usage benchmark, completed initial use case), (f) explicit positive support sentiment, (g) NOT during friction or churn-risk. Output: object with moment_type, moment_strength (high/medium), recommended_ask (review / referral / case-study / speaker-opportunity / roadmap-feedback), and ask_recipient_role (champion / economic-buyer / power-user). → produces: attribute
2. **Identify Advocacy-Ready Users** [`create_segment`] — Build a segment 'Advocacy-ready' capturing users where active_advocacy_moment is high-strength in the last 7 days AND the user hasn't been asked for an advocacy action in the last 90 days (avoid donor fatigue) AND there's no active friction/churn signal (the timing is genuinely good, not just numerically positive). Partitioned by recommended_ask so the journey routes accordingly. → produces: segment
3. **Build Per-Ask Content Variants** [`create_email_content`] — Generate advocacy-ask email variants per recommended_ask. Review ask: 'You just [hit milestone] — would you share your experience publicly? Takes 3 minutes.' Includes one-click links to G2, Capterra, or the relevant review site, pre-filled where the platform allows. Referral ask: 'You're [in top X% of users / just expanded / just renewed] — know anyone who'd benefit from [Product]? Here's your referral code for [reward].' Case-study ask: 'Your team's [specific achievement] is a great story — would you be willing to share it as a customer case study? Our marketing team will do all the writing.' Speaker-opportunity ask: 'We have a [conference / webinar] coming up — would you be interested in speaking?' Roadmap-feedback ask: 'You're using [Product] in such interesting ways — can we get 20 minutes for product roadmap feedback?' Tone: peer-respectful, never transactional. Send-from: named CSM or success lead, never marketing@. → produces: asset
4. **Build Advocacy Recommendation Surface** [`create_recommendation`] — Configure a recommendation surface 'Advocacy opportunities' that activates for advocacy-ready users in the in-app dashboard. Shows the user 2-3 advocacy actions they could take, each with a clear effort estimate ('3 min', '15 min', '1 hour') and what the user gets in return (recognition, referral reward, speaking visibility). Soft-surface — discoverable not interruptive. Lets the user volunteer rather than only being asked. → produces: recommendation
5. **Build Advocacy Journey** [`create_journey`] — Build a journey wired to advocacy-ready segment. Touch 1 (Day 1 after moment detected): advocacy-ask email matched to recommended_ask. Touch 2 (Day 0 of touch 1): activate recommendation surface in-app. Touch 3 (Day 7, ONLY if user engaged with touch 1 OR rec-surface): light follow-up with concrete next step ('You said you'd love to refer someone — here's the link to send them'). Branch: if user submits an advocacy action (review left / referral submitted / case-study agreed / etc), tag the user as 'active advocate' for cross-team awareness AND ensure they're prioritized for future advocacy opportunities. Exit on: action completed (success — log advocacy_event), explicit decline (respect), or 14-day timeout. No badgering. → produces: journey
6. **Build Advocacy Program Dashboard** [`create_dashboard`] — Compose an advocacy program dashboard: advocacy-moment detection volume per week, ask-to-action conversion rate by ask type (which advocacy asks actually convert — referrals usually beat reviews in volume but reviews beat referrals in long-term value), top advocates (users who have completed 3+ advocacy actions — this is the inner-circle list to nurture specially), and downstream attribution (reviews influencing G2 score, referrals creating new pipeline, case studies appearing in sales decks). Reframes CS work from 'retention cost-center' to 'pipeline contributor'. → produces: dashboard
