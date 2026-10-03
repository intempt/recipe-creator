---
id: milestone-driven-advocacy-asks
title: Advocacy asks at the right moment
slash_command: /milestone-driven-advocacy-asks
group: Journeys
owner: intempt
curator: somya
summary: Asks for a review, a referral or a case study just after a customer wins something, and never
  asks the same person twice inside 90 days.
description: >-
  Detect natural advocacy moments via AI attribute (first value achieved, expansion completed, renewal
  closed, high-engagement-streak, customer-milestone-hit) fire contextual advocacy ask matched to moment
  (review / referral / case-study / speaker opportunity). The Captivate Collective Lifecycle Advocacy
  framework.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - advocacy
    - lifecycle-marketing
    - referrals
touches:
  reads:
    - Only the events, attributes and items each step names, in your own project
  writes:
    - A new attribute, from step 1 "Spot the goodwill moments"
    - A new segment, from step 2 "Find who is ready to be asked"
    - A new designed email, from step 3 "Write one ask per moment"
    - A new product recommendation, from step 4 "Let them volunteer in the app"
    - A new journey, from step 5 "Ask once, follow up once"
    - A new dashboard, from step 6 "See which asks get a yes"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Spot the goodwill moments
    summary: >-
      Flags the points where goodwill is highest: first value reached, an upgrade completed, a renewal
      closed, a run of strong weekly activity, a usage benchmark passed, or clearly positive support sentiment.
      Never during friction or churn risk. It records the moment, how strong it is, which ask suits it,
      and who to ask.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'active_advocacy_moment' on the User/Account object. Detects natural
      advocacy windows (when goodwill is highest). Inputs: (a) first-value-achieved events (key activation
      milestone), (b) expansion-completed events (account just upgraded), (c) renewal-closed events (just
      renewed for another term), (d) high-engagement-streak (consecutive weeks of strong activity), (e)
      customer-success-milestone (reached usage benchmark, completed initial use case), (f) explicit positive
      support sentiment, (g) NOT during friction or churn-risk. Output: object with moment_type, moment_strength
      (high/medium), recommended_ask (review / referral / case-study / speaker-opportunity / roadmap-feedback),
      and ask_recipient_role (champion / economic-buyer / power-user).
  - id: s2
    title: Find who is ready to be asked
    summary: >-
      Users with a strong moment in the last 7 days who have not been asked for anything in the last 90
      days and show no friction or churn signal, split by the kind of ask.
    builds: segment
    description: >-
      Build a segment 'Advocacy-ready' capturing users where active_advocacy_moment is high-strength in
      the last 7 days AND the user hasn't been asked for an advocacy action in the last 90 days (avoid
      donor fatigue) AND there's no active friction/churn signal (the timing is genuinely good, not just
      numerically positive). Partitioned by recommended_ask so the journey routes accordingly. Use the
      result of "Spot the goodwill moments".
    dependsOn:
      - s1
  - id: s3
    title: Write one ask per moment
    summary: >-
      A review ask with one click links to G2 or Capterra, prefilled where the site allows. A referral
      ask with their code and the reward. A case study ask that promises your marketing team does the
      writing. A speaker invitation. A request for 20 minutes of roadmap feedback. Peer to peer in tone,
      sent by a named CSM, never from a marketing address.
    builds: email_html
    description: >-
      Generate advocacy-ask email variants per recommended_ask. Review ask: 'You just [hit milestone]:
      would you share your experience publicly? Takes 3 minutes.' Includes one-click links to G2, Capterra,
      or the relevant review site, pre-filled where the platform allows. Referral ask: 'You're [in top
      X% of users / just expanded / just renewed]: know anyone who'd benefit from [Product]? Here's your
      referral code for [reward].' Case-study ask: 'Your team's [specific achievement] is a great story:
      would you be willing to share it as a customer case study? Our marketing team will do all the writing.'
      Speaker-opportunity ask: 'We have a [conference / webinar] coming up (would you be interested in
      speaking?' Roadmap-feedback ask: 'You're using [Product] in such interesting ways) can we get 20
      minutes for product roadmap feedback?' Tone: peer-respectful, never transactional. Send-from: named
      CSM or success lead, never marketing@. Use the result of "Spot the goodwill moments", "Find who
      is ready to be asked".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Let them volunteer in the app
    summary: >-
      A quiet in app panel showing two or three things they could do, each with how long it takes and
      what they get back, so they can offer rather than only be asked.
    builds: recommendation
    description: >-
      Configure a recommendation surface 'Advocacy opportunities' that activates for advocacy-ready users
      in the in-app dashboard. Shows the user 2-3 advocacy actions they could take, each with a clear
      effort estimate ('3 min', '15 min', '1 hour') and what the user gets in return (recognition, referral
      reward, speaking visibility). Soft-surface, discoverable not interruptive. Lets the user volunteer
      rather than only being asked. Use the result of "Spot the goodwill moments", "Find who is ready
      to be asked".
    dependsOn:
      - s1
      - s2
  - id: s5
    title: Ask once, follow up once
    summary: >-
      The matched ask on day 1 after the moment, the in app panel the same day, and a single follow up
      on day 7, only if they engaged, carrying the concrete next step. Anyone who completes an action
      is tagged as an advocate and gets priority next time. They leave on completion, on a decline, or
      after 14 days.
    builds: journey
    description: >-
      Build a journey wired to advocacy-ready segment. Touch 1 (Day 1 after moment detected): advocacy-ask
      email matched to recommended_ask. Touch 2 (Day 0 of touch 1): activate recommendation surface in-app.
      Touch 3 (Day 7, ONLY if user engaged with touch 1 OR rec-surface): light follow-up with concrete
      next step ('You said you'd love to refer someone: here's the link to send them'). Branch: if user
      submits an advocacy action (review left / referral submitted / case-study agreed / etc), tag the
      user as 'active advocate' for cross-team awareness AND ensure they're prioritized for future advocacy
      opportunities. Exit on: action completed (success: log advocacy_event), explicit decline (respect),
      or 14-day timeout. No badgering. Use the result of "Spot the goodwill moments", "Find who is ready
      to be asked", "Write one ask per moment", "Let them volunteer in the app".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
  - id: s6
    title: See which asks get a yes
    summary: >-
      Moments detected per week, how each kind of ask converts, who has completed three or more, and what
      came of them: review scores, referral pipeline, and case studies in sales decks.
    builds: dashboard
    description: >-
      Compose an advocacy program dashboard: advocacy-moment detection volume per week, ask-to-action
      conversion rate by ask type (which advocacy asks actually convert: referrals usually beat reviews
      in volume but reviews beat referrals in long-term value), top advocates (users who have completed
      3+ advocacy actions: this is the inner-circle list to nurture specially), and downstream attribution
      (reviews influencing G2 score, referrals creating new pipeline, case studies appearing in sales
      decks). Reframes CS work from 'retention cost-center' to 'pipeline contributor'. Use the result
      of "Spot the goodwill moments", "Find who is ready to be asked", "Write one ask per moment", "Let
      them volunteer in the app", "Ask once, follow up once".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
outputs:
  - key: attribute
    producedByStep: s1
    type: attribute
    description: AI-Derived Attribute produced by this recipe.
  - key: segment
    producedByStep: s2
    type: segment
    description: Segment produced by this recipe.
  - key: asset
    producedByStep: s3
    type: asset
    description: Asset produced by this recipe.
  - key: recommendation
    producedByStep: s4
    type: recommendation
    description: Recommendation Surface produced by this recipe.
  - key: journey
    producedByStep: s5
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s6
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Advocacy asks at the right moment

Asks for a review, a referral or a case study just after a customer wins something, and never asks the same person twice inside 90 days.

## Steps

1. **Spot the goodwill moments** (builds attribute)

   Flags the points where goodwill is highest: first value reached, an upgrade completed, a renewal closed, a run of strong weekly activity, a usage benchmark passed, or clearly positive support sentiment. Never during friction or churn risk. It records the moment, how strong it is, which ask suits it, and who to ask.

2. **Find who is ready to be asked** (builds segment)

   Users with a strong moment in the last 7 days who have not been asked for anything in the last 90 days and show no friction or churn signal, split by the kind of ask.

3. **Write one ask per moment** (builds email_html)

   A review ask with one click links to G2 or Capterra, prefilled where the site allows. A referral ask with their code and the reward. A case study ask that promises your marketing team does the writing. A speaker invitation. A request for 20 minutes of roadmap feedback. Peer to peer in tone, sent by a named CSM, never from a marketing address.

4. **Let them volunteer in the app** (builds recommendation)

   A quiet in app panel showing two or three things they could do, each with how long it takes and what they get back, so they can offer rather than only be asked.

5. **Ask once, follow up once** (builds journey)

   The matched ask on day 1 after the moment, the in app panel the same day, and a single follow up on day 7, only if they engaged, carrying the concrete next step. Anyone who completes an action is tagged as an advocate and gets priority next time. They leave on completion, on a decline, or after 14 days.

6. **See which asks get a yes** (builds dashboard)

   Moments detected per week, how each kind of ask converts, who has completed three or more, and what came of them: review scores, referral pipeline, and case studies in sales decks.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- Only the events, attributes and items each step names, in your own project

Writes:

- A new attribute, from step 1 "Spot the goodwill moments"
- A new segment, from step 2 "Find who is ready to be asked"
- A new designed email, from step 3 "Write one ask per moment"
- A new product recommendation, from step 4 "Let them volunteer in the app"
- A new journey, from step 5 "Ask once, follow up once"
- A new dashboard, from step 6 "See which asks get a yes"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, recommendation.
