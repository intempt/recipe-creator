---
description: Shows how many people encounter a feature and go on to try it for the first time, using feature interaction events.
author:
  first_name: Aman
  last_name: Tiwari
  job_title: Product Manager
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
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
