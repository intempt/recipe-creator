---
description: Routes accounts by ICP tier and runs enrichment only on the tiers you choose. Provider selection stays the same across all branches.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
---

# Enrich by account tier

Slash command: /conditional-enrichment-by-tier

## Step 1: Stop enriching everything alike

Create a workflow 'Conditional enrichment by tier' triggered by account_created. Goal: only spend enrichment credits proportional to account value. The cost-saving Clay pattern: most teams blanket-enrich, which burns budget on accounts that don't convert.

## Step 2: Buy the cheapest look first

This step builds a workflow.
Configure a cheap initial enrichment step, basic firmographics only (company size, industry, country, domain reputation). Uses the cheapest provider. Goal is JUST to determine which tier the account falls into. Costs about 1-2 credits per record. Use the result of "Stop enriching everything alike".

## Step 3: Sort into three tiers

This step builds a workflow.
Configure a multi-split step routing accounts into 3 branches based on the basic firmographics + any target-account-list match. ENTERPRISE branch: company size >500 OR on target-account list OR enterprise domain (full enrichment cascade. MID-MARKET branch: company size 50-500 AND in target industries) standard enrichment. LOW-FIT branch: everything else: skip further enrichment, mark as deprioritized. Use the result of "Stop enriching everything alike", "Buy the cheapest look first".

## Step 4: Go deep on enterprise

This step builds a workflow.
Configure the enterprise-branch enrichment, premium providers, deep technographic, full decision-maker map (multiple titles per account), funding history, recent news. Costs 15-25 credits per record but reserved only for high-value accounts where the data justifies the spend. Use the result of "Stop enriching everything alike", "Sort into three tiers".

## Step 5: Research the strategic angle

This step builds a workflow.
On the enterprise branch only, add an AI research step for the strategic angle, recent priorities, competitive positioning, unique buying signals. The kind of research a human SDR would spend 30 minutes on, done in 2 minutes for accounts that warrant it. Use the result of "Stop enriching everything alike", "Go deep on enterprise".

## Step 6: Keep mid market standard

This step builds a workflow.
Configure the mid-market-branch enrichment, single mid-tier provider, basic decision-maker (CEO/founder/main contact), tech stack at company level (not per-person). Costs 5-8 credits per record. Use the result of "Stop enriching everything alike", "Sort into three tiers".

## Step 7: Publish and track the saving

Validate workflow DAG and publish. Add a monthly cost-tracking report showing credits consumed per tier, typically reveals you can serve 100% of accounts at 30-40% of blanket-enrichment cost. RevOps loves this report. Use the result of "Stop enriching everything alike", "Research the strategic angle", "Keep mid market standard".
