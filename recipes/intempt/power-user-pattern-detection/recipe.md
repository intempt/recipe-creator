---
frontmatter_id: power-user-pattern-detection
slash_command: /power-user-pattern-detection
description: 'Detects users with daily or batch patterns of repeated manual work: 5+ same task in 7 days, one-at-a-time batch operations, or repeat exports.'
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Detects users repeating manual work and nudges them, at the moment of friction, toward the automation feature that
    fits, then tracks adoption and asks adopters for reviews.
  parameters:
  - name: repeat_window
    type: duration
    label: Lookback window for repeated manual work
    default: 7 d
    required: false
  - name: repeat_threshold
    type: number
    label: Repeats of the same manual task that count as a pattern
    default: 5
    required: false
  - name: export_threshold
    type: number
    label: Manual exports in window that count as a pattern
    default: 3
    required: false
  - name: filter_threshold
    type: number
    label: Repeated dashboard filter uses that count as a pattern
    default: 10
    required: false
  - name: filter_window
    type: duration
    label: Lookback window for repeated dashboard filters
    default: 14 d
    required: false
  - name: dismiss_limit
    type: number
    label: Feature-recommendation dismissals before a user is excluded
    default: 3
    required: false
  - name: review_delay
    type: duration
    label: Delay before advocacy ask after adoption
    default: 14 d
    required: false
  - name: followup_delay
    type: duration
    label: Delay before reinforcement email
    default: 3 d
    required: false
  - name: journey_timeout
    type: duration
    label: Journey timeout
    default: 30 d
    required: false
  - name: adoption_target
    type: number
    label: Target in-app nudge-to-adoption rate (percent)
    default: 15
    required: false
  requirements:
  - slot: manual_work_events
    kind: event
    meaning: A customer performed a manual action in the product, such as running a report, exporting data, assigning a task,
      or filtering a dashboard
    properties:
    - name: action_type
      type: text
      meaning: The kind of manual action performed
      optional: false
    - name: occurred_at
      type: date
      meaning: When the action happened
      optional: false
  - slot: detected_manual_patterns
    kind: attribute
    meaning: A list of repeated manual patterns detected for a user, each with the matching automation feature and an adoption-likelihood
      score
  - slot: paying_customer
    kind: segment
    meaning: Users on a paid plan
  - slot: feature_adoption
    kind: event
    meaning: A customer started using an automation feature such as scheduled reports, API or webhooks, task templates, or
      saved views
    properties:
    - name: feature_name
      type: text
      meaning: The automation feature adopted
      optional: false
  - slot: feature_dismissal
    kind: event
    meaning: A customer dismissed a feature recommendation
    properties:
    - name: feature_name
      type: text
      meaning: The feature recommendation dismissed
      optional: false
  - slot: plan_limits
    kind: attribute
    meaning: The feature limits that apply to a customer's current plan
  - slot: in_app_messaging
    kind: integration
    meaning: A connected in-app messaging channel able to show contextual nudges and dashboard recommendations
    channel: email
  - slot: review_site_page
    kind: destination
    meaning: A public review profile page where customers can post product reviews
    optional: true
    channel: email
  - slot: referral_program
    kind: knowledge
    meaning: Information about the referral program offered to customers
    optional: true
  steps:
  - id: s1
    builds: attribute
    instruction: 'Create an AI-derived attribute {detected_manual_patterns} on the user record, refreshed daily, that detects
      repeated manual sequences in {manual_work_events} which have automated counterparts in the product. Patterns: (a) same
      multi-step report run {repeat_threshold}+ times in {repeat_window}, matched to unused scheduled reports; (b) manual
      data exports {export_threshold}+ times in {repeat_window}, matched to unused API or webhook feature; (c) same task type
      assigned repeatedly {repeat_threshold}+ times in {repeat_window}, matched to unused task templates; (d) same dashboard
      filter applied {filter_threshold}+ times in {filter_window}, matched to unused saved views. Output per user: list of
      detected patterns, the automation feature name, and an adoption-likelihood score based on plan, skill level and prior
      automation adoption.'
  - id: s2
    builds: segment
    instruction: Build a segment 'Manual-pattern detected' of users in {paying_customer} where {detected_manual_patterns}
      is non-empty and the user has not yet adopted the recommended automation feature. Partition the segment by feature to
      introduce. Exclude users with {dismiss_limit}+ dismissals in {feature_dismissal} and users whose {plan_limits} exclude
      the suggested feature. Uses the result of "Spot work done the hard way".
  - id: s3
    builds: page
    instruction: 'Create an in-app nudge per detected pattern, shown as a tooltip or floating card when the user is mid-pattern
      (for example on their 6th manual export), delivered through {in_app_messaging}. Copy: ''You''ve done this {repeat_threshold}
      times this week: did you know we can automate this?'' Include a 60-second how-it-works GIF, an ''Enable now'' call to
      action, and a dismiss option. Show at the moment of friction, not on a generic feature-discovery surface. Uses the result
      of "Spot work done the hard way" and "Find who could automate it".'
  - id: s4
    builds: recommendation
    instruction: Configure a dashboard recommendation surface 'Power features for your workflow' for users in the "Find who
      could automate it" segment. Show the top 3 entries of {detected_manual_patterns} ranked by adoption-likelihood, each
      with its automation counterpart, a one-line description and a 'Try it' deep link. When the user adopts a feature, rotate
      in the next-best pattern. Keep it visible for 30 days after detection. Uses the result of "Spot work done the hard way"
      and "Find who could automate it".
  - id: s5
    builds: email
    instruction: 'Write a follow-up email sent {review_delay} after a user adopts a recommended automation feature. Subject
      line and body: ''Congrats on automating {feature_adoption.feature_name}: you have saved an estimated weekly time. Would
      you share your experience?'' Include two calls to action: write a review on the review site ({review_site_page}) with
      a deep link to the correct product page, and refer a peer using the program described in {referral_program}. Uses the
      result of "Spot work done the hard way" and "Find who could automate it".'
  - id: s6
    builds: automation
    instruction: 'Build a journey on the "Manual-pattern detected" segment from "Find who could automate it". Touch 1 (real
      time, on the 5th or later repetition in session): fire the nudge from "Nudge them mid task" and activate the recommendation
      surface from "List their power features". Touch 2 (after {followup_delay}, if the user has not dismissed): send a reinforcement
      email with the same feature pitch and a customer story of someone who automated it. Touch 3 (after {review_delay}, only
      if the user adopted the feature): send the advocacy email from "Ask adopters for a review". Touch 4 (after {review_delay},
      only if the user has NOT adopted): stop pushing messages; the pattern and recommendation surface stay in place. Exit
      when the user adopts the feature and the advocacy ask is sent, when the user explicitly dismisses, or after {journey_timeout}.'
  - id: s7
    builds: dashboard
    instruction: Create a power-user detection dashboard with three panels. (1) Top 10 detected manual patterns by frequency,
      including each feature's discoverability gap to guide in-app UI priorities. (2) In-app nudge-to-adoption rate, the headline
      metric, with a target of {adoption_target}% or more, compared against a baseline of 4-6% for generic feature emails.
      (3) 30-day retention of adopters versus non-adopters, and advocacy-ask conversion (percent of adopters who write a review
      or refer). Uses the result of "Spot work done the hard way", "Find who could automate it", "Nudge them mid task", "List
      their power features", "Ask adopters for a review" and "Nudge, remind, then let it go".
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
