---
description: Every upgrade from free to paid creates a CSM kickoff task carrying the customer's whole free period history, due inside five working days.
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
  - finance
  - media
---

# Free to paid CSM kickoff

Slash command: /free-to-paid-csm-kickoff

## Step 1: Find genuine upgrades

Build a segment 'Free-to-paid converters - last 7 days' capturing users where subscription_created fired in the last 7 days AND the user previously had subscription_status = free OR trialing (true conversion, not net-new direct-paid signup, those go through a different flow). Excludes users where the subscription is < $50 MRR (consumer-tier; doesn't get CSM motion).

## Step 2: Write the pre call brief

Create an AI-derived attribute 'preconversion_history' on the User object, computed at subscription_created time. Capture: (a) days from signup to paid conversion; (b) features most-used in free period; (c) features NEVER touched (potential expansion drivers later); (d) team-member signal: how many users from the same account are also on free / paid; (e) source: how they got to signup (organic / paid / referral / outbound). This becomes the CSM's pre-call brief.

## Step 3: Assign a CSM and kick off

Create a workflow firing on subscription_created for free-to-paid converters. Step sequence: (1) compute preconversion_history attribute; (2) assign CSM via territory + plan-tier rules (enterprise tier gets named CSM, SMB tier gets pooled CSM); (3) create CSM kickoff task with the preconversion history pre-attached, due within 5 business days; (4) trigger the structured onboarding journey (separate recipe) for the user; (5) update account lifecycle to 'new-customer'; (6) post Slack notification to the assigned CSM and a celebration message to #wins. Use the result of "Find genuine upgrades", "Write the pre call brief".

## Step 4: Prove the handoff matters

Compose a PLG-to-CS handoff quality dashboard: free-to-paid conversion volume per week, CSM-task completion rate within 5 business days (target: 95%+), median days from signup-to-conversion (PLG funnel speed), and 90-day retention of free-to-paid converters split by 'CSM kickoff completed within 5 days' vs. 'CSM kickoff missed': typically the gap is 15-25 percentage points (the proof-of-value for human CSM motion). Use the result of "Find genuine upgrades", "Write the pre call brief", "Assign a CSM and kick off".
