---
name: milestone-driven-advocacy-asks
description: Use when a user mentions "milestone advocacy asks", "lifecycle advocacy", "natural advocacy moments", or asks for related help. Detect natural advocacy moments via AI attribute (first value achieved, expansion completed, renewal closed, high-engagement-streak, customer-milestone-hit) fire contextual advocacy ask matched to moment (review / referral / case-study / speaker opportunity). The Captivate Collective Lifecycle Advocacy framework.
arguments: []
intempt:
  id: milestone-driven-advocacy-asks
  title: "Advocacy asks at the right moment"
  version: 1.0.0
  slashCommand: /milestone-driven-advocacy-asks
  group: Journeys
  shortDescription: "Asks for a review, a referral or a case study just after a customer wins something, and never asks the same person twice inside 90 days."
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
      title: "Spot the goodwill moments"
      command: create_ai_attribute
      produces: attribute
      bindsAs: advocacy_moment
      description: "Flags the points where goodwill is highest: first value reached, an upgrade completed, a renewal closed, a run of strong weekly activity, a usage benchmark passed, or clearly positive support sentiment. Never during friction or churn risk. It records the moment, how strong it is, which ask suits it, and who to ask."
      prompt: 'Create an AI-derived attribute ''Active advocacy moment'' on the User/Account object. Detects natural advocacy windows (when goodwill is highest). Inputs: (a) first-value-achieved events (key activation milestone), (b) expansion-completed events (account just upgraded), (c) renewal-closed events (just renewed for another term), (d) high-engagement-streak (consecutive weeks of strong activity), (e) customer-success-milestone (reached usage benchmark, completed initial use case), (f) explicit positive support sentiment, (g) NOT during friction or churn-risk. Output: object with moment type, moment strength (high/medium), recommended ask (review / referral / case-study / speaker-opportunity / roadmap-feedback), and ask recipient role (champion / economic-buyer / power-user).'
    - step: 2
      title: "Find who is ready to be asked"
      command: create_segment
      produces: segment
      bindsAs: segment
      dependsOn:
      - advocacy_moment
      description: "Users with a strong moment in the last 7 days who have not been asked for anything in the last 90 days and show no friction or churn signal, split by the kind of ask."
      prompt: Build a segment 'Advocacy-ready' capturing users with a high-strength advocacy moment in the last 7 days AND the user hasn't been asked for an advocacy action in the last 90 days (avoid donor fatigue) AND there's no active friction/churn signal (the timing is genuinely good, not just numerically positive). Partitioned by recommended ask so the journey routes accordingly.
    - step: 3
      title: "Write one ask per moment"
      command: create_email_content
      produces: asset
      bindsAs: email_asset
      dependsOn:
      - advocacy_moment
      - segment
      description: "A review ask with one click links to G2 or Capterra, prefilled where the site allows. A referral ask with their code and the reward. A case study ask that promises your marketing team does the writing. A speaker invitation. A request for 20 minutes of roadmap feedback. Peer to peer in tone, sent by a named CSM, never from a marketing address."
      prompt: 'Generate advocacy-ask email variants per recommended ask. Review ask: ''You just [hit milestone]: would you share your experience publicly? Takes 3 minutes.'' Includes one-click links to G2, Capterra, or the relevant review site, pre-filled where the platform allows. Referral ask: ''You''re [in top X% of users / just expanded / just renewed]: know anyone who''d benefit from [Product]? Here''s your referral code for [reward].'' Case-study ask: ''Your team''s [specific achievement] is a great story: would you be willing to share it as a customer case study? Our marketing team will do all the writing.'' Speaker-opportunity ask: ''We have a [conference / webinar] coming up (would you be interested in speaking?'' Roadmap-feedback ask: ''You''re using [Product] in such interesting ways) can we get 20 minutes for product roadmap feedback?'' Tone: peer-respectful, never transactional. Send-from: named CSM or success lead, never marketing@.'
    - step: 4
      title: "Let them volunteer in the app"
      command: create_recommendation
      produces: recommendation
      bindsAs: rec_surface
      dependsOn:
      - advocacy_moment
      - segment
      description: "A quiet in app panel showing two or three things they could do, each with how long it takes and what they get back, so they can offer rather than only be asked."
      prompt: Configure a recommendation surface 'Advocacy opportunities' that activates for advocacy-ready users in the in-app dashboard. Shows the user 2-3 advocacy actions they could take, each with a clear effort estimate ('3 min', '15 min', '1 hour') and what the user gets in return (recognition, referral reward, speaking visibility). Soft-surface, discoverable not interruptive. Lets the user volunteer rather than only being asked.
    - step: 5
      title: "Ask once, follow up once"
      command: create_journey
      produces: journey
      bindsAs: journey
      dependsOn:
      - advocacy_moment
      - segment
      - email_asset
      - rec_surface
      description: "The matched ask on day 1 after the moment, the in app panel the same day, and a single follow up on day 7, only if they engaged, carrying the concrete next step. Anyone who completes an action is tagged as an advocate and gets priority next time. They leave on completion, on a decline, or after 14 days."
      prompt: 'Build a journey wired to advocacy-ready segment. Touch 1 (Day 1 after moment detected): advocacy-ask email matched to the recommended ask. Touch 2 (Day 0 of touch 1): activate recommendation surface in-app. Touch 3 (Day 7, ONLY if user engaged with touch 1 OR rec-surface): light follow-up with concrete next step (''You said you''d love to refer someone: here''s the link to send them''). Branch: if user submits an advocacy action (review left / referral submitted / case-study agreed / etc), tag the user as ''active advocate'' for cross-team awareness AND ensure they''re prioritized for future advocacy opportunities. Exit on: action completed (success: log an advocacy event), explicit decline (respect), or 14-day timeout. No badgering.'
    - step: 6
      title: "See which asks get a yes"
      command: create_dashboard
      produces: dashboard
      bindsAs: dashboard
      dependsOn:
      - advocacy_moment
      - segment
      - email_asset
      - rec_surface
      - journey
      description: "Moments detected per week, how each kind of ask converts, who has completed three or more, and what came of them: review scores, referral pipeline, and case studies in sales decks."
      prompt: 'Compose an advocacy program dashboard: advocacy-moment detection volume per week, ask-to-action conversion rate by ask type (which advocacy asks actually convert: referrals usually beat reviews in volume but reviews beat referrals in long-term value), top advocates (users who have completed 3+ advocacy actions: this is the inner-circle list to nurture specially), and downstream attribution (reviews influencing G2 score, referrals creating new pipeline, case studies appearing in sales decks). Reframes CS work from ''retention cost-center'' to ''pipeline contributor''.'
  outputs:
    - { name: attribute, type: attribute, cardinality: single, description: "AI-Derived Attribute produced by this recipe." }
    - { name: segment, type: segment, cardinality: single, description: "Segment produced by this recipe." }
    - { name: asset, type: asset, cardinality: single, description: "Asset produced by this recipe." }
    - { name: recommendation, type: recommendation, cardinality: single, description: "Recommendation Surface produced by this recipe." }
    - { name: journey, type: journey, cardinality: single, description: "Journey produced by this recipe." }
    - { name: dashboard, type: dashboard, cardinality: single, description: "Dashboard produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Advocacy asks at the right moment

Asks for a review, a referral or a case study just after a customer wins something, and never asks the same person twice inside 90 days.

## What it does

1. **Spot the goodwill moments** (`create_ai_attribute`)

   Flags the points where goodwill is highest: first value reached, an upgrade completed, a renewal closed, a run of strong weekly activity, a usage benchmark passed, or clearly positive support sentiment. Never during friction or churn risk. It records the moment, how strong it is, which ask suits it, and who to ask.

2. **Find who is ready to be asked** (`create_segment`)

   Users with a strong moment in the last 7 days who have not been asked for anything in the last 90 days and show no friction or churn signal, split by the kind of ask.

3. **Write one ask per moment** (`create_email_content`)

   A review ask with one click links to G2 or Capterra, prefilled where the site allows. A referral ask with their code and the reward. A case study ask that promises your marketing team does the writing. A speaker invitation. A request for 20 minutes of roadmap feedback. Peer to peer in tone, sent by a named CSM, never from a marketing address.

4. **Let them volunteer in the app** (`create_recommendation`)

   A quiet in app panel showing two or three things they could do, each with how long it takes and what they get back, so they can offer rather than only be asked.

5. **Ask once, follow up once** (`create_journey`)

   The matched ask on day 1 after the moment, the in app panel the same day, and a single follow up on day 7, only if they engaged, carrying the concrete next step. Anyone who completes an action is tagged as an advocate and gets priority next time. They leave on completion, on a decline, or after 14 days.

6. **See which asks get a yes** (`create_dashboard`)

   Moments detected per week, how each kind of ask converts, who has completed three or more, and what came of them: review scores, referral pipeline, and case studies in sales decks.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.
