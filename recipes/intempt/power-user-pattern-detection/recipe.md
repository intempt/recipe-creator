---
id: power-user-pattern-detection
title: Power user pattern detection
slash_command: /power-user-pattern-detection
group: Journeys
owner: intempt
curator: somya
summary: >-
  Detects users with daily or batch patterns of repeated manual work: 5+ same task in 7 days, one-at-a-time
  batch operations, or repeat exports.
description: >-
  Attribute repeated manual-work patterns at daily or batch cadence. Segment users matching 5+ same task in 7
  days, one-at-a-time batch operations, or repeat exports. Send the relevant power-feature recommendation and
  follow-up by email. No mid-session in-app overlay.
version: 2.0.0
classification:
  product:
    - marketing
  agent: journey-builder
  mode:
    - saas
  industry:
    - ai
    - b2b-saas
  vertical:
    - sales-led
  complexity: advanced
  executionMode: live
  tags:
    - power-user-detection
    - feature-discovery
    - advocacy-pipeline
prerequisites:
  events:
    - value: feature_used
      severity: blocking
touches:
  reads:
    - The feature_used event in your project
  writes:
    - A new attribute, from step 1 "Spot work done the hard way"
    - A new segment, from step 2 "Find who could automate it"
    - A new landing page, from step 3 "Nudge them mid task"
    - A new product recommendation, from step 4 "List their power features"
    - A new designed email, from step 5 "Ask adopters for a review"
    - A new journey, from step 6 "Nudge, remind, then let it go"
    - A new dashboard, from step 7 "See which features stay hidden"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Spot work done the hard way
    summary: >-
      Checked daily for repeated manual work the product can automate: the same report run five or more
      times in 7 days when scheduled reports exist, three or more manual exports in 7 days when there
      is an API, the same task assigned again and again when templates exist, or the same dashboard filter
      set 10 times in 14 days when views can be saved. Each pattern is paired with the feature that replaces
      it and how likely that person is to adopt it.
    builds: attribute
    description: >-
      Create an AI-derived attribute 'detected_manual_patterns' on the User object, refreshed daily. Detects
      repeated manual sequences that have automated counterparts in the product. Example patterns: (a)
      user runs same multi-step report 5+ times in 7 days (has unused 'scheduled reports' feature), (b)
      user exports data manually 3+ times in 7 days (has unused API/webhook feature), (c) user assigns
      same task type repeatedly (has unused task templates feature), (d) user filters dashboard same way
      10+ times in 14 days (has unused saved-view feature). Output: list of detected patterns with the
      automate-it feature name and adoption-likelihood score (based on user's plan, skill level, prior
      automation adoption).
  - id: s2
    title: Find who could automate it
    summary: >-
      Paying users with at least one detected pattern who have not used the matching feature, split by
      which feature to introduce. Anyone who has dismissed feature suggestions three times is left out,
      and so is anyone whose plan does not include the feature.
    builds: segment
    description: >-
      Build a segment 'Manual-pattern detected' capturing paying users where detected_manual_patterns
      is non-empty AND the user hasn't yet used the recommended automation feature. Partitioned by feature-to-introduce.
      Excludes users who have dismissed feature-recommendations 3+ times (respect the no) and users with
      plan limits that exclude the suggested feature. Use the result of "Spot work done the hard way".
    dependsOn:
      - s1
  - id: s3
    title: Nudge them mid task
    summary: >-
      A tooltip or card that appears while they are doing it, on the sixth manual export rather than later:
      how many times they have done this, a 60 second clip of the automated way, an enable now button,
      and a dismiss.
    builds: page
    description: >-
      Generate in-app nudge content per detected pattern. Format: tooltip or floating card that appears
      WHEN the user is mid-pattern (e.g. on their 6th manual export). Content: 'You've done this 6 times
      this week: did you know [Product] can automate this?' + 60-second 'how it works' GIF + 'enable now'
      CTA + dismiss option. Renders at the exact moment of friction, not in a generic feature-discovery
      surface. The contextual timing is the magic: this is the 4x feature-adoption uplift pattern from
      the research. Use the result of "Spot work done the hard way", "Find who could automate it".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: List their power features
    summary: >-
      A dashboard panel with the top three patterns and the features that replace them, ranked by how
      likely they are to adopt, each one a line and a link. It rotates as they adopt and stays up for
      30 days after detection.
    builds: recommendation
    description: >-
      Configure a recommendation surface 'Power features for your workflow' on the user's dashboard. Pulls:
      the top 3 detected_manual_patterns with their automate-it counterparts, ranked by adoption-likelihood.
      Each recommendation: 1-line description + 'try it' deep link. Updates when user adopts a feature
      (rotates in the next-best). Renders persistently for 30 days after detection. Use the result of
      "Spot work done the hard way", "Find who could automate it".
    dependsOn:
      - s1
      - s2
  - id: s5
    title: Ask adopters for a review
    summary: >-
      Sent 14 days after someone adopts an automation: what it is saving them per week, then two options,
      leave a review with a direct link or refer a peer through the referral programme.
    builds: email_html
    description: >-
      Generate follow-up email content sent 14 days after a user adopts a recommended automation feature.
      Content: 'Congrats on automating [feature]: you've saved an estimated [time] per week. Mind sharing
      your experience?' Two CTAs: write a review on G2/Capterra (with deep-link to the right product page),
      refer a peer (with referral program info). This is where power-user-detection becomes an advocacy
      pipeline: the user just had a positive experience, the moment is warm. Use the result of "Spot work
      done the hard way", "Find who could automate it".
    dependsOn:
      - s1
      - s2
  - id: s6
    title: Nudge, remind, then let it go
    summary: >-
      The in app nudge fires live on the fifth repeat and the panel switches on. On day 3, if they did
      not dismiss it, an email repeats the case with a customer story. On day 14 adopters get the review
      ask, and everyone else is left alone: the panel stays but the pushing stops. It closes on adoption,
      on a dismissal, or after 30 days.
    builds: journey
    description: >-
      Build a journey wired to manual-pattern-detected segment. Touch 1 (real-time, on the 5th+ pattern
      repetition mid-session): in-app contextual nudge fires. Recommendation surface activates persistently.
      Touch 2 (Day 3, if user didn't dismiss): email reinforcement with the same feature pitch + a customer
      story of someone who automated it. Touch 3 (Day 14, IF user has adopted the feature): advocacy follow-up
      email asking for review/referral. Touch 4 (Day 14, IF user has NOT adopted): exit gracefully: pattern
      stays detected, surface stays active, but stop pushing. Exit on: feature adoption + advocacy ask
      sent, explicit dismiss, or 30-day timeout. Use the result of "Spot work done the hard way", "Find
      who could automate it", "Nudge them mid task", "List their power features", "Ask adopters for a
      review".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
  - id: s7
    title: See which features stay hidden
    summary: >-
      The ten manual patterns that come up most, how often the in app nudge leads to adoption, the 30
      day retention of adopters against everyone else, and how many adopters go on to leave a review or
      refer someone.
    builds: dashboard
    description: >-
      Compose a power-user detection dashboard: top 10 detected manual patterns by frequency (which features
      have the biggest discoverability gap (informs in-app UI redesign priorities), in-app-nudge-to-adoption
      rate (the headline metric) target: 15%+, baseline generic feature emails get 4-6%), 30-day retention
      of adopters vs. non-adopters (proves the journey's value beyond direct adoption), and advocacy-ask
      conversion (% of adopters who write a review or refer: this is the unexpected revenue side-effect
      of feature discovery). Use the result of "Spot work done the hard way", "Find who could automate
      it", "Nudge them mid task", "List their power features", "Ask adopters for a review", "Nudge, remind,
      then let it go".
    dependsOn:
      - s1
      - s2
      - s3
      - s4
      - s5
      - s6
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
    producedByStep: s5
    type: asset
    description: Asset produced by this recipe.
  - key: recommendation
    producedByStep: s4
    type: recommendation
    description: Recommendation Surface produced by this recipe.
  - key: journey
    producedByStep: s6
    type: journey
    description: Journey produced by this recipe.
  - key: dashboard
    producedByStep: s7
    type: dashboard
    description: Dashboard produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Power user pattern detection

Detects users with daily or batch patterns of repeated manual work: 5+ same task in 7 days, one-at-a-time batch operations, or repeat exports.

## Steps

1. **Spot work done the hard way** (builds attribute)

   Checked daily for repeated manual work the product can automate: the same report run five or more times in 7 days when scheduled reports exist, three or more manual exports in 7 days when there is an API, the same task assigned again and again when templates exist, or the same dashboard filter set 10 times in 14 days when views can be saved. Each pattern is paired with the feature that replaces it and how likely that person is to adopt it.

2. **Find who could automate it** (builds segment)

   Paying users with at least one detected pattern who have not used the matching feature, split by which feature to introduce. Anyone who has dismissed feature suggestions three times is left out, and so is anyone whose plan does not include the feature.

3. **Nudge them mid task** (builds page)

   A tooltip or card that appears while they are doing it, on the sixth manual export rather than later: how many times they have done this, a 60 second clip of the automated way, an enable now button, and a dismiss.

4. **List their power features** (builds recommendation)

   A dashboard panel with the top three patterns and the features that replace them, ranked by how likely they are to adopt, each one a line and a link. It rotates as they adopt and stays up for 30 days after detection.

5. **Ask adopters for a review** (builds email_html)

   Sent 14 days after someone adopts an automation: what it is saving them per week, then two options, leave a review with a direct link or refer a peer through the referral programme.

6. **Nudge, remind, then let it go** (builds journey)

   The in app nudge fires live on the fifth repeat and the panel switches on. On day 3, if they did not dismiss it, an email repeats the case with a customer story. On day 14 adopters get the review ask, and everyone else is left alone: the panel stays but the pushing stops. It closes on adoption, on a dismissal, or after 30 days.

7. **See which features stay hidden** (builds dashboard)

   The ten manual patterns that come up most, how often the in app nudge leads to adoption, the 30 day retention of adopters against everyone else, and how many adopters go on to leave a review or refer someone.

## What you end up with

- **attribute** (attribute): AI-Derived Attribute produced by this recipe.
- **segment** (segment): Segment produced by this recipe.
- **asset** (asset): Asset produced by this recipe.
- **recommendation** (recommendation): Recommendation Surface produced by this recipe.
- **journey** (journey): Journey produced by this recipe.
- **dashboard** (dashboard): Dashboard produced by this recipe.

## What this recipe touches

Reads:

- The feature_used event in your project

Writes:

- A new attribute, from step 1 "Spot work done the hard way"
- A new segment, from step 2 "Find who could automate it"
- A new landing page, from step 3 "Nudge them mid task"
- A new product recommendation, from step 4 "List their power features"
- A new designed email, from step 5 "Ask adopters for a review"
- A new journey, from step 6 "Nudge, remind, then let it go"
- A new dashboard, from step 7 "See which features stay hidden"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build dashboard, journey, page, recommendation.
