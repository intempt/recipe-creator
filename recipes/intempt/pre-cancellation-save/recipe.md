---
description: Catches people who open the cancel flow but have not finished it, and answers the reason they gave with a pause, a downgrade, a discount or a call.
author:
  first_name: Somya
  last_name: Nayak
  job_title: Marketing Lead
  avatar: https://cdn.intempt.com/assets/author-profile-pics/somya.png
  company: Intempt
org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - media
---

# Save them before they cancel

Slash command: /pre-cancellation-save

## Step 1: Catch cancel intent live

Create an AI-derived attribute 'cancel_intent_signal' on the User object. Computed in real-time. Inputs: (a) visited /cancel or /downgrade page in last 14 days; (b) clicked 'cancel subscription' button (which triggers cancel-modal not cancellation); (c) submitted cancel reason in cancel-flow form without confirming. Output: object with intent_level (browsing / interacting / committing), stated_reason if captured (price / unused / competitor / feature-gap / pause-needed / other), and timestamp. The signal expires after 7 days of no further activity.

## Step 2: Find who is halfway out

Build a segment 'Cancel-intent active' capturing paying users where cancel_intent_signal.intent_level is 'interacting' or 'committing' AND subscription is still active (not yet cancelled, once cancelled, post-cancel-winback takes over). Excludes users on trial (different motion) and users who have already received a cancel-save offer in last 90 days (no spam). Use the result of "Catch cancel intent live".

## Step 3: Write one offer per reason

This step builds a designed marketing email (HTML).
Generate branched save-offer content per cancel reason. (a) Price reason: offer 20% retention discount for 3 months OR downgrade-to-lighter-plan option; (b) Unused reason: offer 60-day pause OR a 1:1 onboarding call to drive activation; (c) Competitor reason: offer a 1:1 call with PM to address feature gaps + competitive comparison sheet; (d) Feature-gap reason: roadmap visibility for the specific missing feature + interim workaround; (e) Pause-needed reason: 1-click pause for up to 90 days (preserves data); (f) Other/no-reason: ask 'what would have made you stay?' + offer 1:1 call. Send-from: the customer's CSM if assigned, else success@ address. Use the result of "Catch cancel intent live", "Find who is halfway out".

## Step 4: Make one matched offer

Build a branched journey triggered when cancel_intent_signal becomes 'interacting' or 'committing'. Branch on stated_reason: each user gets ONE save offer matched to their stated reason. Touch 1 (within 1 hour of intent signal): the matched save offer email. Touch 2 (Day 2, if no engagement): softer follow-up reinforcing the offer. For high-LTV customers (top 10% by ARR), additionally create urgent CSM task at intent detection: human save attempt parallel to email. Exit on: save_offer_accepted (recorded as retention_win event), subscription_canceled (proceed to post-cancel-winback), or 14-day timeout. Use the result of "Catch cancel intent live", "Find who is halfway out", "Write one offer per reason".

## Step 5: See which saves actually work

Compose a save-flow dashboard: cancel-intent volume by week, save rate (intent users who DON'T cancel within 30 days), save rate by stated reason (which save offers actually work), save rate by offer type (discount vs. pause vs. downgrade vs. 1:1 call: informs offer strategy), and ARR saved this quarter. Also surface: stated cancel reasons distribution (voice-of-customer for product/pricing teams) and cohorts where save attempts fail consistently (deep churn signal: those segments need product fixes, not save offers). Use the result of "Catch cancel intent live", "Find who is halfway out", "Write one offer per reason", "Make one matched offer".
