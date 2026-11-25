---
frontmatter_id: feature-discovery-adoption
slash_command: /feature-discovery-adoption
description: Emails a weekly digest of how many users discover each feature, try it, use it repeatedly and become habitual
  users, with flags for weak discovery and low stickiness.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly per-feature digest of discovery, first use and habitual use, flagging low-stickiness features and
    promotion candidates.
  parameters:
  - name: conversionWindow
    type: duration
    label: Conversion window
    default: 21 d
    required: false
  - name: habitualUseThreshold
    type: number
    label: Minimum uses to count as repeat use
    default: 3
    required: false
  - name: habitualWindow
    type: duration
    label: Window for repeat use
    default: 21 d
    required: false
  - name: habitualActiveDays
    type: number
    label: Distinct active days required in recent window
    default: 3
    required: false
  - name: recentDayWindow
    type: duration
    label: Recent day window for habitual check
    default: 5 d
    required: false
  - name: highDiscoveryThreshold
    type: number
    label: High-discovery user threshold
    default: 1000
    required: false
  - name: lowStickinessRate
    type: number
    label: Low habitual conversion threshold (%)
    default: 5
    required: false
  - name: lowTrialRate
    type: number
    label: Low discovery-to-trial threshold (%)
    default: 20
    required: false
  - name: promotionRate
    type: number
    label: Promotion candidate habitual conversion threshold (%)
    default: 25
    required: false
  - name: topN
    type: number
    label: Number of top features to surface
    default: 3
    required: false
  - name: comparisonPeriod
    type: duration
    label: Comparison period
    default: 21 d
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: feature_discovery_event
    kind: event
    meaning: A customer viewed a page where a feature was introduced or a feature tour or tooltip was shown
    properties:
    - name: page_url
      type: text
      meaning: URL of the page viewed, containing the feature path
      optional: false
  - slot: feature_click_event
    kind: event
    meaning: A customer clicked a feature interaction element in the product
    properties:
    - name: target_id
      type: text
      meaning: Stable identifier of the clicked feature element, one per feature
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - feature_discovery_event
    - feature_click_event
    - conversionWindow
    - habitualUseThreshold
    - habitualWindow
    - habitualActiveDays
    - recentDayWindow
    - highDiscoveryThreshold
    - lowStickinessRate
    - lowTrialRate
    - promotionRate
    - topN
    - comparisonPeriod
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users per feature,
      a feature being one {feature_click_event.target_id}, over the last {comparisonPeriod} against the {comparisonPeriod}
      before, and writes per feature: users who discovered it ({feature_discovery_event} with {feature_discovery_event.page_url}
      containing the feature path); of those, users who tried it ({feature_click_event} with that target_id within {conversionWindow});
      users using it {habitualUseThreshold}+ times within {habitualWindow}; habitual users, active with it on {habitualActiveDays}
      or more days in the last {recentDayWindow}; discovery-to-habitual rate %; the top {topN} features by habitual users
      and by habitual rate. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}.
      The email lists features with more than {highDiscoveryThreshold} discoverers and a habitual rate under {lowStickinessRate}%
      as low stickiness, features with discovery-to-trial under {lowTrialRate}% as weak discovery, and features with a habitual
      rate over {promotionRate}% as promotion candidates. Nothing else is sent.'
---

# Feature discovery to adoption

Slash command: /feature-discovery-adoption

## Step 1: Email the weekly feature adoption digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users per feature, a feature being one target id, over the last 21 d against the 21 d before, and writes per feature: users who discovered it (feature discovery event with page url containing the feature path); of those, users who tried it (feature click event with that target_id within 21 d); users using it 3+ times within 21 d; habitual users, active with it on 3 or more days in the last 5 d; discovery-to-habitual rate %; the top 3 features by habitual users and by habitual rate. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. The email lists features with more than 1000 discoverers and a habitual rate under 5% as low stickiness, features with discovery-to-trial under 20% as weak discovery, and features with a habitual rate over 25% as promotion candidates. Nothing else is sent.
