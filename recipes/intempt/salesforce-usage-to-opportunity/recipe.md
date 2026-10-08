---
description: Keeps the usage fields on an open opportunity current, so the forecast reflects what the account is doing rather than what was said on a call.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - b2b-saas
  - ecommerce
---

# Usage onto the Salesforce opportunity

Slash command: /salesforce-usage-to-opportunity

## Step 1: Describe usage for the forecast

Create account attributes describing engagement in the terms the forecast cares about: active seats, weekly active proportion, depth of feature adoption, trend over the last month. These are what a rep would otherwise assert from memory.

## Step 2: Update the open opportunity

Create a workflow that finds the open opportunity for the account and updates the usage fields on it. Only fields Intempt owns are written: never stage, never amount, never close date, which belong to the rep. A CDP that silently moves a stage is a forecasting incident that presents as an integration. Use the result of "Describe usage for the forecast".
