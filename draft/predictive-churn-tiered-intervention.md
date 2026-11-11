---
frontmatter_id: predictive-churn-tiered-intervention
author:
  name: Intempt
  last_name: Technologies
  org_name: intempt
---
# Tiered churn intervention

## Step 1: Score churn risk daily

Create an AI-derived attribute "churn_risk_score" on the User object, refreshed daily and again on every significant behavioral event. Inputs: engagement velocity (sessions trend over the last 30, 14 and 7 days), feature usage decay, support sentiment trajectory, billing-status signals, peer-cohort churn patterns, and account-level usage for business accounts. Output: a numeric score from 0 to 100 with a tier label: low is 0 to 29, medium is 30 to 59, high is 60 to 79, critical is 80 to 100. The score is never collapsed to a single at-risk flag: medium and high tiers receive different treatments in the steps below.

## Step 2: Take everyone above the low tier

Build a segment of users named "Churn risk, paying users". A user is in the segment only when all of these are true: they are a paying user; their churn_risk_score is 30 or more; their account is more than 14 days old; they are not already in an active save flow from another journey. Use the result of "Score churn risk daily".

## Step 3: Write an email per band

Generate per-tier email content for the users in "Churn risk, paying users". Medium tier: educational content matched to the underutilized feature with the strongest retention correlation for that user's cohort, plus a personalized "pick up where you left off" deep link. Tone is helpful, not alarmed. High tier: value reinforcement naming the specific use case the account is under-using, a note that their customer success manager is available, and a concrete offer of a short walkthrough of that use case. Critical tier: a personal note from the founder asking directly whether anything is wrong, with a direct calendar link to book time. Medium-tier email is sent from the success team address; high-tier email is sent from the account's named customer success manager; critical-tier email is sent from the founder. Use the result of "Score churn risk daily", "Take everyone above the low tier".

## Step 4: Catch them when they log in

This step builds a page.
Generate in-app messages for high-tier users shown only when they log in. Format: a contextual banner referencing the account's most-likely-success path, naming the specific underused feature and offering a short walkthrough of it. For critical-tier users, on a rare login show a full-screen interrupt offering a direct one-to-one call with their customer success manager or the founder. Show this only when the AI signal for that user is strong; never show it on every login. Use the result of "Score churn risk daily", "Take everyone above the low tier", "Write an email per band".

## Step 5: Recommend what keeps people

Configure a recommendation surface for high and critical tier users that surfaces the features their cohort uses successfully but this user has not adopted, prioritized by how strongly each feature correlates with retention in this user's segment. Render it in-app on the dashboard, inside the email content from "Write an email per band", and in any page personalization the user encounters. Use the result of "Score churn risk daily", "Take everyone above the low tier".

## Step 6: Treat each band differently

Build a tiered journey wired to the "Churn risk, paying users" segment. Branch on churn_risk_score tier at entry, and re-evaluate weekly. Low tier: a single light-touch nurture email on day 7, with no urgency, just value content. Medium tier: an email on day 0 with a helpful tip, an in-app message at the user's next login with a deep link to the under-used retention feature, and a day-7 email carrying the recommendation surface from "Recommend what keeps people". High tier: a day-0 email from the customer success manager offering help, an urgent in-app banner at the next session, and a same-day task for the customer success manager. Critical tier: within 4 hours, the founder's personal email, an offer of a hand-off to a live conversation, an urgent task for the customer success manager, and a task for an executive sponsor. Recompute the tier weekly: a user whose score drops below 30 for 14 or more consecutive days exits the journey and is logged as a retention win; a user whose score rises moves to the tier-appropriate next touch. Exit the journey entirely on Subscription canceled, handing off to "win-back", or on unsubscribe. Use the result of "Score churn risk daily", "Take everyone above the low tier", "Write an email per band", "Catch them when they log in", "Recommend what keeps people".

## Step 7: See if the bands hold up

Compose a tiered churn intervention dashboard showing: the distribution of users across tiers per week; the save rate per tier, meaning the percent of users in each tier who exit risk rather than churn; the critical-tier response time from entry to the customer success manager's first human touch, against a 4-hour target; the ARR-weighted save value by tier; and tier-migration tracking, where a move from high to medium counts as a success and a move from medium to high counts as an early warning. Compare the predicted churn_risk_score against actual churn at 30, 60 and 90 days. Use the result of "Score churn risk daily", "Take everyone above the low tier", "Write an email per band", "Catch them when they log in", "Recommend what keeps people", "Treat each band differently".
