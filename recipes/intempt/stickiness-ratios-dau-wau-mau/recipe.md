---
frontmatter_id: stickiness-ratios-dau-wau-mau
slash_command: /stickiness-ratios-dau-wau-mau
description: Emails a weekly digest of daily, weekly and monthly active users and their stickiness ratios, broken down by
  plan, with benchmark and erosion flags.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of daily, weekly and monthly active users and their stickiness ratios by plan, with benchmark
    and erosion flags.
  parameters:
  - name: trendWindow
    type: duration
    label: Time range to show
    default: 90 d
    required: false
  - name: weeklyWindow
    type: duration
    label: Weekly active rolling window
    default: 7 d
    required: false
  - name: monthlyWindow
    type: duration
    label: Monthly active rolling window
    default: 28 d
    required: false
  - name: dauMauGoodThreshold
    type: number
    label: DAU/MAU 'good' benchmark (%)
    default: 20
    required: false
  - name: dauMauBestThreshold
    type: number
    label: DAU/MAU best-in-class benchmark (%)
    default: 50
    required: false
  - name: dauWauStrongThreshold
    type: number
    label: DAU/WAU strong habit benchmark (%)
    default: 50
    required: false
  - name: erosionThreshold
    type: number
    label: Stickiness drop that triggers an erosion flag (percentage points)
    default: 3
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: session_start_event
    kind: event
    meaning: A user started a session in the product (marks the user as active)
  - slot: subscription_plan_attribute
    kind: attribute
    meaning: The plan name on a user's most recent active subscription, used to break down activity by plan
  steps:
  - id: s1
    builds: automation
    uses:
    - session_start_event
    - subscription_plan_attribute
    - trendWindow
    - weeklyWindow
    - monthlyWindow
    - dauMauGoodThreshold
    - dauMauBestThreshold
    - dauWauStrongThreshold
    - erosionThreshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {session_start_event}
      and writes these figures, in total and split by {subscription_plan_attribute}: DAU, the average daily active users over
      the last 7 days; WAU, users active in the last {weeklyWindow}; MAU, users active in the last {monthlyWindow}; DAU/WAU
      % and DAU/MAU %; the same figures for the 7 days ending 7 days ago and the weekly trend over the last {trendWindow}.
      Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. The email reads DAU/MAU
      as good at {dauMauGoodThreshold}%+ and best in class at {dauMauBestThreshold}%+, DAU/WAU as a strong habit at {dauWauStrongThreshold}%+,
      flags plans whose DAU/MAU fell more than {erosionThreshold} points against the week before, and plans whose MAU rose
      while DAU stayed flat. Nothing else is sent.'
---

# Daily, weekly and monthly stickiness

Slash command: /stickiness-ratios-dau-wau-mau

## Step 1: Email the weekly stickiness digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did session start event and writes these figures, in total and split by subscription plan attribute: DAU, the average daily active users over the last 7 days; WAU, users active in the last 7 d; MAU, users active in the last 28 d; DAU/WAU % and DAU/MAU %; the same figures for the 7 days ending 7 days ago and the weekly trend over the last 90 d. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email reads DAU/MAU as good at 20%+ and best in class at 50%+, DAU/WAU as a strong habit at 50%+, flags plans whose DAU/MAU fell more than 3 points against the week before, and plans whose MAU rose while DAU stayed flat. Nothing else is sent.
