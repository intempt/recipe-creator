---
frontmatter_id: high-intent-visitors
slash_command: /high-intent-visitors
description: Free-plan users reading your site heavily, nudged toward a relevant paid feature by push notification and shared with growth as a shortlist worth a closer look.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Nudges free-plan users who research heavily on your site with a push about a relevant paid feature, and shares
    the shortlist with growth for timely outreach.
  parameters:
  - name: visitThreshold
    type: number
    label: Minimum page views in window
    default: 3
  - name: windowLength
    type: duration
    label: Lookback window
    default: 14 d
  - name: pushTitleMaxChars
    type: number
    label: Maximum push title length (characters)
    default: 40
  - name: pricingPageLink
    type: string
    label: Deep link to pricing page
    default: /pricing
  - name: pushTone
    type: enum
    label: Push tone
    default: helpful
    options:
    - helpful
    - neutral
    - enthusiastic
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A user viewed a page on the website
  - slot: plan_attribute
    kind: attribute
    meaning: The subscription plan a user is on (for example free or paid)
  - slot: high_intent_visitors
    kind: segment
    meaning: Users on the free plan who viewed pages heavily in a recent window
    creatable: true
    definition: users whose {plan_attribute} is free and who did {page_view_event} at least {visitThreshold} times in the
      last {windowLength}
  - slot: paid_only_feature
    kind: knowledge
    meaning: A feature that is available only on a paid plan, to highlight in the push
  - slot: growth_team_list
    kind: destination
    meaning: Distribution list for the growth team that receives shortlists by email
    channel: email
  steps:
  - id: s1
    builds: segment
    uses:
    - plan_attribute
    - page_view_event
    - visitThreshold
    - windowLength
    instruction: Build a segment named "High-Intent Visitors" of users where {plan_attribute} is free and who did {page_view_event}
      at least {visitThreshold} times in the last {windowLength}.
  - id: s2
    builds: push
    uses:
    - s1
    - high_intent_visitors
    - paid_only_feature
    - pushTitleMaxChars
    - pushTone
    - pricingPageLink
    instruction: Write a push notification for the users in {high_intent_visitors} highlighting one feature from {paid_only_feature}
      that is available only on a paid plan. Keep the title under {pushTitleMaxChars} characters, add one short body line,
      use a {pushTone} tone, and deep link to {pricingPageLink}.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - high_intent_visitors
    - growth_team_list
    instruction: Write a plain-text email to {growth_team_list} listing the email address of each user in {high_intent_visitors}
      so outreach can be timed to their actual research activity.
---

# Free users researching heavily

Slash command: /high-intent-visitors

## Step 1: Build the high-intent list

Build a segment of users named "High-Intent Visitors".
A user is in the segment only when all of these are true:
- their Plan attribute is "free"
- they did the View page event 3 or more times in the last 14 days

## Step 2: Nudge toward a paid feature

Generate a push notification for the users in "High-Intent Visitors" highlighting one feature only available on a paid plan. Title under 40 characters, one short body line, helpful and not pushy tone, deep link to the pricing page. Use the result of "Build the high-intent list".

## Step 3: Share the shortlist with growth

Generate a plain-text email to the growth team distribution list For each user in "High-Intent Visitors", name their email address, so outreach can be timed to their actual research activity. Use the result of "Build the high-intent list".
