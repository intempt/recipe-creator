---
frontmatter_id: feature-discovery-adoption
slash_command: /feature-discovery-adoption
description: Shows how many people encounter a feature and go on to try it for the first time, using feature interaction events.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Shows how many people discover a feature, try it for the first time, and become habitual users, with conversion
    rates and flags for low-stickiness features.
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
    builds: report
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
    instruction: 'Create a funnel report named "Feature Discovery to Adoption" with these steps: (1) View page where page
      URL contains the feature path, labeled "Discovered Feature" (first exposure); alternatively, click on where target_id
      matches a feature-tour or tooltip element. (2) Click on where target_id matches the feature interaction handle, labeled
      "Tried Feature" (first use). (3) Click on with the same target_id as step 2, at least {habitualUseThreshold} times by
      the same user within {habitualWindow}, labeled "Used 3+ Times". (4) Click on with the same target_id, active on at least
      {habitualActiveDays} distinct days within the last {recentDayWindow}, labeled "Habitual User". Set the conversion window
      to {conversionWindow}. Break down by target_id (feature handle). Compare against the previous {comparisonPeriod}. For
      each feature, also show discovery-to-habitual conversion rate (step 4 divided by step 1) and median time from discovery
      to habitual status in days. Annotations: flag features with more than {highDiscoveryThreshold} discovered users and
      habitual conversion below {lowStickinessRate}% as high-discovery, low-stickiness for UX investigation; flag features
      with discovery-to-trial conversion below {lowTrialRate}% as having a weak discovery moment; highlight features with
      discovery-to-habitual conversion above {promotionRate}% as promotion candidates. Surface the top {topN} features by
      absolute habitual-user count and the top {topN} by habitual-conversion rate.'
---

# Feature discovery to adoption

Slash command: /feature-discovery-adoption

## Step 1: Follow a feature from first look

Create a Funnel report called "Feature Discovery to Adoption".
Steps:
1. Event "View page" where Page URL contains the feature path: "Discovered Feature" (first exposure)
 (alternative: Click on where target_id matches a feature-tour or tooltip element)
2. Event "Click on" where target_id matches the feature interaction handle: "Tried Feature" (first use)
3. Event "Click on" with same target_id as Step 2, count >= 3 by the same user within 21 days: "Used 3+ Times"
4. Event "Click on" with same target_id, frequency: at least 3 distinct days of use in the last 5 days: "Habitual User"
Conversion window: 21 days
Breakdown: By target_id (feature handle)
Compare: Previous period (prior 21 days)
For each feature, also surface:
- Discovery to Habitual conversion rate (Step 4 / Step 1)
- Median time-to-habitual (days from discovery to habitual)
Annotations:
- Flag features with discovery > 1000 users AND habitual conversion < 5%: high-discovery, low-stickiness; investigate UX.
- Flag features where discovery to trial conversion < 20%: discovery moment isn't compelling.
- Highlight features with discovery to habitual conversion > 25%: surface candidates for promotion.
Surface the top 3 features by absolute habitual-user count and the top 3 by habitual-conversion rate.
Taxonomy notes:
- "feature_discovered" and "feature_habitual" as standalone events do not exist. Feature interactions are tracked via Click on with stable target_id values per feature.
- Step 4 ("Habitual User") requires Lovable to compute the "3 of last 5 days" rule from Click on event timestamps grouped by user.
