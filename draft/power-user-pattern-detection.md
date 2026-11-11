---
frontmatter_id: power-user-pattern-detection
author:
  name: Intempt
  last_name: Technologies
  org_name: intempt
---
# Power user pattern detection

## Step 1: Spot work done the hard way

Create an AI-derived attribute "detected_manual_patterns" on the User object, refreshed daily. Detects repeated manual sequences that have an automated counterpart in the product: running the same multi-step report 5 or more times in 7 days, where a scheduled-reports feature exists and is unused; exporting data manually 3 or more times in 7 days, where an API or webhook export feature exists and is unused; assigning the same task type repeatedly, where a task-template feature exists and is unused; and filtering a dashboard the same way 10 or more times in 14 days, where a saved-view feature exists and is unused. Output: a list of detected patterns, each naming the automate-it feature and an adoption-likelihood score based on the user's plan, skill level and prior automation adoption.

## Step 2: Find who could automate it

Build a segment of users named "Manual-pattern detected". A paying user is in the segment only when their detected_manual_patterns list is not empty and they have not yet used the recommended automation feature. Partition the segment by which feature is being recommended. Exclude users who have dismissed a feature recommendation 3 or more times, and users whose plan does not include the recommended feature. Use the result of "Spot work done the hard way".

## Step 3: Nudge them mid task

This step builds a page.
Generate an in-app nudge for each detected pattern, shown while the user is in the middle of the manual pattern, such as on their sixth manual export this week. Content: a statement of how many times they have repeated the task this week, a short explanation of the automated alternative with a link to a short walkthrough, an enable-now action, and a dismiss option. Render it at the moment of friction, not in a generic feature-discovery surface. Use the result of "Spot work done the hard way", "Find who could automate it".

## Step 4: List their power features

Configure a recommendation surface named "Power features for your workflow" on the user's dashboard. Source it from the user's top 3 detected_manual_patterns and their automate-it counterparts, ranked by adoption-likelihood score, each with a one-line description and a try-it link. Update the list when the user adopts a feature, rotating in the next-best pattern. Keep it rendered for 30 days after detection. Use the result of "Spot work done the hard way", "Find who could automate it".

## Step 5: Ask adopters for a review

Generate a follow-up email sent 14 days after a user adopts a recommended automation feature. Content: a note naming the feature they adopted and the estimated time saved per week based on how often they previously did the task manually, followed by two actions: write a review with a deep link to the review page for the product, or refer a peer with the referral program link. Use the result of "Spot work done the hard way", "Find who could automate it".

## Step 6: Nudge, remind, then let it go

Build a journey wired to the "Manual-pattern detected" segment. In real time, on the fifth or later repetition of the pattern mid-session: fire the in-app nudge from "Nudge them mid task" and activate the recommendation surface from "List their power features". Day 3, if the user has not dismissed it: send an email reinforcement with the same feature recommendation and a relevant customer story. Day 14, if the user has adopted the feature: send the advocacy email from "Ask adopters for a review". Day 14, if the user has not adopted it: stop sending touches, but keep the pattern detected and the recommendation surface active. Exit the journey when the feature is adopted and the advocacy email is sent, on explicit dismissal, or after a 30-day timeout. Use the result of "Spot work done the hard way", "Find who could automate it", "Nudge them mid task", "List their power features", "Ask adopters for a review".

## Step 7: See which features stay hidden

Compose a power-user detection dashboard showing: the top 10 detected manual patterns by frequency, as a discoverability-gap signal for product design; the conversion rate from in-app nudge to feature adoption, against a 15 percent target, with generic feature-announcement emails as the baseline comparison at 4 to 6 percent; the 30-day retention of adopters against non-adopters; and the conversion rate from feature adoption to a review or referral. Use the result of "Spot work done the hard way", "Find who could automate it", "Nudge them mid task", "List their power features", "Ask adopters for a review", "Nudge, remind, then let it go".
