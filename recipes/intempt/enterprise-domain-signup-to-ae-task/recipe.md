---
description: Spots when a self serve signup comes from a large company, enriches it, and puts it in front of an AE instead of leaving it in the free funnel.
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

# Enterprise signup to AE task

Slash command: /enterprise-domain-signup-to-ae-task

## Step 1: Work out the account tier

Create an AI-derived attribute 'account_tier' on the Account object. Computed at signup from email domain. Output: enterprise / mid-market / smb / consumer (generic email). Logic: cross-reference against (a) target-account list, (b) employee-count enrichment if available (1000+ = enterprise, 100-1000 = mid-market), (c) public-company indicator, (d) ICP industry match. Generic email domains (gmail, outlook) to tier: consumer (likely not a buyer).

## Step 2: Find enterprise signups with no AE

Build a segment 'Enterprise signups - last 30 days' capturing accounts where account_tier = enterprise AND the account was created in last 30 days AND no AE has been assigned. Used for both the workflow audit and post-hoc analysis of enterprise-lead conversion. Use the result of "Work out the account tier".

## Step 3: Hand it to the right AE

Create a workflow firing on user_signed_up. Step sequence: (1) compute account_tier from the email domain; (2) if tier = enterprise or mid-market: immediately enrich (firmographics, decision-makers, tech stack); (3) check whether the account is already in the CRM or part of target-account list; (4) create an enterprise-tier AE task with priority HIGH, assigned by territory + named-account rules (preserving any pre-assigned account owner); (5) post a high-visibility Slack alert to #enterprise-alerts with account context, decision-maker contacts, and current product activity; (6) suppress this user from the standard self-serve nurture journey (different motion for enterprise: sales-led, not marketing-led). Use the result of "Work out the account tier", "Find enterprise signups with no AE".

## Step 4: Watch the response time

Compose an enterprise-lead dashboard: enterprise signup volume per week, AE response time (target: <2hr business hours), enterprise-signup-to-meeting conversion, enterprise-signup-to-deal conversion (typically takes 60+ days), enterprise pipeline value sourced this way (separate from outbound), and account-tier mix (enterprise / mid-market / smb / consumer) of all signups so leadership can see ICP attraction trends. Use the result of "Work out the account tier", "Find enterprise signups with no AE", "Hand it to the right AE".
