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
    instruction: Build a new segment named "High-Intent Visitors" of users where {plan_attribute} is free and who did {page_view_event}
      at least {visitThreshold} times in the last {windowLength}.
  - id: s2
    builds: push
    uses:
    - s1
    - paid_only_feature
    - pushTitleMaxChars
    - pushTone
    - pricingPageLink
    dependsOn:
    - s1
    instruction: Write a push notification for the users in the segment from "Build the high-intent list" highlighting one
      feature from {paid_only_feature} that is available only on a paid plan. Keep the title under {pushTitleMaxChars} characters,
      add one short body line, use a {pushTone} tone, and deep link to {pricingPageLink}. Write no template tag or placeholder
      (such as a deeplink tag) in the push title or body; a link, if any, is the URL given for this run.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - growth_team_list
    dependsOn:
    - s1
    instruction: 'Write a plain-text email to {growth_team_list} listing the email address of each user in the segment from
      "Build the high-intent list" so outreach can be timed to their actual research activity. The plain-text email is plain
      text only: no HTML tags, no markup and no unsubscribe line.'
---

# Free users researching heavily

Slash command: /high-intent-visitors

## Step 1: Build the high-intent list

Build a new segment named "High-Intent Visitors" of users where plan attribute is free and who did page view event at least 3 times in the last 14 d.

## Step 2: Nudge toward a paid feature

Write a push notification for the users in the segment from "Build the high-intent list" highlighting one feature from paid only feature that is available only on a paid plan. Keep the title under 40 characters, add one short body line, use a helpful tone, and deep link to /pricing. Write no template tag or placeholder (such as a deeplink tag) in the push title or body; a link, if any, is the URL given for this run.

## Step 3: Share the shortlist with growth

Write a plain-text email to growth team list listing the email address of each user in the segment from "Build the high-intent list" so outreach can be timed to their actual research activity. The plain-text email is plain text only: no HTML tags, no markup and no unsubscribe line.
