---
frontmatter_id: usage-spike-expansion-play
slash_command: /usage-spike-expansion-play
description: This recipe spots customer accounts whose usage is surging and runs a coordinated two-week outreach to both the day-to-day champion and the budget holder, pointing them toward a higher plan. It is built for B2B product and growth teams working with account executives on expansion.
author:
  name: Intempt Technologies
  first_name: Intempt
  last_name: Technologies
  org_name: intempt
---

# Expansion play on a usage spike

## Step 1: Score the expansion signals

Create an AI-derived attribute "expansion_signal_score" on the Account object. Inputs: active-user growth rate, meaning new users added from the account's domain in the last 30 days against the trailing 90-day baseline; feature-depth expansion, meaning the count of distinct features used per active user trending up; multi-team adoption, meaning users from different functions at the account based on email domain or profile data; usage-cap proximity, meaning how close the account is to its seat, API call, event or storage limit; and integration-attach, meaning new integrations connected in the period. Output: a score from 0 to 100 with a reasoning string naming which signals are firing.

## Step 2: Find accounts outgrowing the plan

Build a segment of accounts named "Expansion-ready customer accounts". An account is in the segment only when both of these are true: its expansion_signal_score is 70 or more in the last 14 days; it has no active expansion deal already in progress. Partition the segment by the account's dominant signal type, meaning whichever of user-growth, feature-depth or usage-cap is driving the score, so the journey in a later step can branch on it. Use the result of "Score the expansion signals".

## Step 3: Write to the champion

Generate email content for the most active user at the account, the champion. Write one variant per dominant signal type. For user-growth: tell them their team's active-user count has grown and that teams at this scale typically benefit from the account's higher-tier organization features. For feature-depth: tell them their usage is deeper than most accounts on their current plan and name the next capability most similar accounts adopt after reaching this depth. For usage-cap: tell them their team is approaching its plan's resource limit and name the limit directly. Tone is peer-to-peer enablement, not a sales pitch: the champion should feel recognized, not pitched. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan".

## Step 4: Write to the budget holder

Generate email content for the account's economic buyer, the admin, manager or finance owner who is not the day-to-day user. Write one variant per dominant signal type. For user-growth: summarize the quarter's growth in active users as a business case. For feature-depth: state the account's percentile usage depth against similar accounts and propose discussing expansion options. For usage-cap: compare the cost of upgrading against the cost of continuing to pay overage at the current usage level. Tone is business-formal. Set the reply-to address to the account's assigned account executive. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion".

## Step 5: Show the plan above theirs

Configure a recommendation surface named "Expansion features" that activates for accounts in "Expansion-ready customer accounts". Source the recommendations from the features available on the account's next-higher plan tier that are most used by accounts with a similar usage pattern to this one. Render it in-app on the account's admin dashboard and inside the email content from "Write to the champion" and "Write to the budget holder". Use the result of "Score the expansion signals", "Find accounts outgrowing the plan".

## Step 6: Work the account over two weeks

Build a multi-stakeholder journey triggered when an account enters "Expansion-ready customer accounts". Day 0: send the champion email from "Write to the champion". Day 3: activate the upgrade-comparison recommendation surface for admin users at the account on their next session. Day 7: send the budget-holder email from "Write to the budget holder", with a call to action to meet the account's account executive. Day 14: if no meeting has been scheduled, create a task for the account executive with the full account context, meaning the signals that fired, the identified decision-makers, and the recommended package. Keep the recommendation surface active for 60 days from entry. Exit the journey when a meeting is scheduled, handing off to the account executive; when the account upgrades, logged as a success; when a deal is created, handed to the account executive from there; or when the expansion_signal_score drops below 50 for 30 consecutive days, exited as a false signal. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion", "Write to the budget holder", "Show the plan above theirs".

## Step 7: Measure the expansion it makes

Compose an expansion performance dashboard showing: the weekly volume of expansion signals by dominant signal type; the conversion rate from expansion signal to meeting scheduled; the conversion rate from expansion signal to deal created; the ARR uplift from journey-attributed accounts against a holdout group not run through the journey; and which signal type converts best, to inform where expansion-oriented product and marketing investment goes next. Use the result of "Score the expansion signals", "Find accounts outgrowing the plan", "Write to the champion", "Write to the budget holder", "Show the plan above theirs", "Work the account over two weeks".
