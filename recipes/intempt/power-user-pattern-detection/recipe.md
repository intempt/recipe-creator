---
description: 'Detects users with daily or batch patterns of repeated manual work: 5+ same task in 7 days, one-at-a-time batch operations, or repeat exports.'
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
---

# Power user pattern detection

Slash command: /power-user-pattern-detection

## Step 1: Spot work done the hard way

Create an AI-derived attribute 'detected_manual_patterns' on the User object, refreshed daily. Detects repeated manual sequences that have automated counterparts in the product. Example patterns: (a) user runs same multi-step report 5+ times in 7 days (has unused 'scheduled reports' feature), (b) user exports data manually 3+ times in 7 days (has unused API/webhook feature), (c) user assigns same task type repeatedly (has unused task templates feature), (d) user filters dashboard same way 10+ times in 14 days (has unused saved-view feature). Output: list of detected patterns with the automate-it feature name and adoption-likelihood score (based on user's plan, skill level, prior automation adoption).

## Step 2: Find who could automate it

Build a segment 'Manual-pattern detected' capturing paying users where detected_manual_patterns is non-empty AND the user hasn't yet used the recommended automation feature. Partitioned by feature-to-introduce. Excludes users who have dismissed feature-recommendations 3+ times (respect the no) and users with plan limits that exclude the suggested feature. Use the result of "Spot work done the hard way".

## Step 3: Nudge them mid task

This step builds a page.
Generate in-app nudge content per detected pattern. Format: tooltip or floating card that appears WHEN the user is mid-pattern (e.g. on their 6th manual export). Content: 'You've done this 6 times this week: did you know [Product] can automate this?' + 60-second 'how it works' GIF + 'enable now' CTA + dismiss option. Renders at the exact moment of friction, not in a generic feature-discovery surface. The contextual timing is the magic: this is the 4x feature-adoption uplift pattern from the research. Use the result of "Spot work done the hard way", "Find who could automate it".

## Step 4: List their power features

Configure a recommendation surface 'Power features for your workflow' on the user's dashboard. Pulls: the top 3 detected_manual_patterns with their automate-it counterparts, ranked by adoption-likelihood. Each recommendation: 1-line description + 'try it' deep link. Updates when user adopts a feature (rotates in the next-best). Renders persistently for 30 days after detection. Use the result of "Spot work done the hard way", "Find who could automate it".

## Step 5: Ask adopters for a review

Generate follow-up email content sent 14 days after a user adopts a recommended automation feature. Content: 'Congrats on automating [feature]: you've saved an estimated [time] per week. Mind sharing your experience?' Two CTAs: write a review on G2/Capterra (with deep-link to the right product page), refer a peer (with referral program info). This is where power-user-detection becomes an advocacy pipeline: the user just had a positive experience, the moment is warm. Use the result of "Spot work done the hard way", "Find who could automate it".

## Step 6: Nudge, remind, then let it go

Build a journey wired to manual-pattern-detected segment. Touch 1 (real-time, on the 5th+ pattern repetition mid-session): in-app contextual nudge fires. Recommendation surface activates persistently. Touch 2 (Day 3, if user didn't dismiss): email reinforcement with the same feature pitch + a customer story of someone who automated it. Touch 3 (Day 14, IF user has adopted the feature): advocacy follow-up email asking for review/referral. Touch 4 (Day 14, IF user has NOT adopted): exit gracefully: pattern stays detected, surface stays active, but stop pushing. Exit on: feature adoption + advocacy ask sent, explicit dismiss, or 30-day timeout. Use the result of "Spot work done the hard way", "Find who could automate it", "Nudge them mid task", "List their power features", "Ask adopters for a review".

## Step 7: See which features stay hidden

Compose a power-user detection dashboard: top 10 detected manual patterns by frequency (which features have the biggest discoverability gap (informs in-app UI redesign priorities), in-app-nudge-to-adoption rate (the headline metric) target: 15%+, baseline generic feature emails get 4-6%), 30-day retention of adopters vs. non-adopters (proves the journey's value beyond direct adoption), and advocacy-ask conversion (% of adopters who write a review or refer: this is the unexpected revenue side-effect of feature discovery). Use the result of "Spot work done the hard way", "Find who could automate it", "Nudge them mid task", "List their power features", "Ask adopters for a review", "Nudge, remind, then let it go".
