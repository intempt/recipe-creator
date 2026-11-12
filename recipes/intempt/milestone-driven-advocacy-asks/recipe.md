---
frontmatter_id: milestone-driven-advocacy-asks
slash_command: /milestone-driven-advocacy-asks
description: Asks for a review, a referral or a case study just after a customer wins something, and never asks the same person twice inside 90 days.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Sends well-timed advocacy asks (review, referral, case study, speaker or feedback) right after a customer win,
    never asking the same person twice within 90 days.
  parameters:
  - name: lookback_window
    type: duration
    label: Window to find a recent goodwill moment
    default: 7 d
  - name: cooldown_window
    type: duration
    label: Minimum gap between advocacy asks to the same person
    default: 90 d
  - name: follow_up_delay
    type: duration
    label: Delay before the light follow-up
    default: 7 d
  - name: journey_timeout
    type: duration
    label: Journey timeout with no action
    default: 14 d
  - name: ask_delay
    type: duration
    label: Delay after a moment is detected before the first ask
    default: 1 d
  - name: advocate_threshold
    type: number
    label: Advocacy actions needed to be a top advocate
    default: 3
  - name: sender_role
    type: enum
    label: Role that sends the asks
    default: csm
    options:
    - csm
    - success_lead
  requirements:
  - slot: first_value_event
    kind: event
    meaning: A customer reached its first-value or key activation milestone
    properties:
    - name: milestone
      type: text
      meaning: Name of the milestone reached
      optional: true
    optional: true
  - slot: expansion_event
    kind: event
    meaning: A customer completed an expansion or upgrade of its plan
    properties:
    - name: plan
      type: text
      meaning: Plan the customer upgraded to
      optional: true
    optional: true
  - slot: renewal_event
    kind: event
    meaning: A customer closed a renewal for another term
    properties:
    - name: term_length
      type: text
      meaning: Length of the renewed term
      optional: true
    optional: true
  - slot: engagement_streak_event
    kind: event
    meaning: A customer sustained a streak of consecutive weeks of strong activity
    properties:
    - name: streak_weeks
      type: number
      meaning: Number of consecutive active weeks
      optional: true
    optional: true
  - slot: success_milestone_event
    kind: event
    meaning: A customer reached a usage benchmark or completed its initial use case
    properties:
    - name: milestone
      type: text
      meaning: Benchmark or use case completed
      optional: true
    optional: true
  - slot: positive_sentiment_event
    kind: event
    meaning: A customer gave explicit positive feedback to support
    properties:
    - name: sentiment_score
      type: number
      meaning: Sentiment score of the feedback
      optional: true
    optional: true
  - slot: friction_signal
    kind: event
    meaning: A customer raised an open friction issue or shows a churn-risk signal
    optional: true
  - slot: advocacy_moment_attribute
    kind: attribute
    meaning: 'A user attribute holding the detected advocacy moment: type, strength (high or medium), recommended ask and
      recipient role'
  - slot: advocacy_ask_sent_event
    kind: event
    meaning: A user was sent an advocacy ask
    properties:
    - name: ask_type
      type: text
      meaning: Type of advocacy ask sent
      optional: true
    optional: true
  - slot: advocacy_action_event
    kind: event
    meaning: A customer completed an advocacy action such as a review, referral, case study agreement or speaking commitment
    properties:
    - name: action_type
      type: text
      meaning: Type of advocacy action completed
      optional: true
    optional: true
  - slot: advocacy_decline_event
    kind: event
    meaning: A customer explicitly declined an advocacy request
    optional: true
  - slot: advocacy_ready_segment
    kind: segment
    meaning: Users with a high-strength advocacy moment in the last week, not asked in the last 90 days, and no active friction
      signal
    creatable: true
    definition: users where advocacy_moment_attribute is high-strength in the last {lookback_window} AND no advocacy_ask_sent_event
      in the last {cooldown_window} AND no friction_signal active, partitioned by recommended ask
  - slot: sending_identity
    kind: integration
    meaning: An email sending connection that can send from a named CSM or success lead
    channel: email
  - slot: in_app_surface
    kind: destination
    meaning: An in-app recommendation surface shown on the customer dashboard
    optional: true
    channel: email
  - slot: active_advocate_tag
    kind: attribute
    meaning: A user attribute marking a customer as an active advocate
    optional: true
  - slot: review_platform_links
    kind: knowledge
    meaning: Approved review site links and pre-fill rules for customer reviews
    optional: true
  - slot: referral_program
    kind: knowledge
    meaning: Referral program terms, codes and rewards
    optional: true
  - slot: product_brand
    kind: brand
    meaning: The product name and tone guidelines for customer-facing messages
  steps:
  - id: s1
    builds: attribute
    uses:
    - first_value_event
    - expansion_event
    - renewal_event
    - engagement_streak_event
    - success_milestone_event
    - positive_sentiment_event
    - friction_signal
    instruction: 'Create an AI-derived user or account attribute ''active_advocacy_moment'' that detects natural advocacy
      windows when goodwill is highest. Inputs: {first_value_event} with {first_value_event.milestone}, {expansion_event}
      with {expansion_event.plan}, {renewal_event} with {renewal_event.term_length}, {engagement_streak_event} with {engagement_streak_event.streak_weeks},
      {success_milestone_event} with {success_milestone_event.milestone}, {positive_sentiment_event} with {positive_sentiment_event.sentiment_score}.
      Exclude any user with an active {friction_signal}. Output an object with moment_type, moment_strength (high or medium),
      recommended_ask (review, referral, case-study, speaker-opportunity or roadmap-feedback) and ask_recipient_role (champion,
      economic-buyer or power-user).'
  - id: s2
    builds: segment
    uses:
    - s1
    - advocacy_ready_segment
    - advocacy_moment_attribute
    - advocacy_ask_sent_event
    - friction_signal
    - lookback_window
    - cooldown_window
    instruction: Build the segment {advocacy_ready_segment} of users whose {advocacy_moment_attribute} from "Spot the goodwill
      moments" is high-strength within {lookback_window}, who have no {advocacy_ask_sent_event} within {cooldown_window},
      and who have no active {friction_signal}. Partition the segment by recommended_ask so the journey routes each user to
      the matching ask.
  - id: s3
    builds: email
    uses:
    - s2
    - sender_role
    - review_platform_links
    - referral_program
    - product_brand
    instruction: 'Write one advocacy ask email per recommended_ask, sent from a named {sender_role} and never from a generic
      marketing address, in a peer-respectful tone that is never transactional. Review ask: say the customer just reached
      a milestone and ask whether they would share their experience publicly, noting it takes about 3 minutes, with one-click
      links to approved review sites from {review_platform_links}, pre-filled where the platform allows. Referral ask: say
      the customer is in a top share of users, has just expanded or has just renewed, ask whether they know anyone who would
      benefit from {product_brand}, and include their referral code and reward from {referral_program}. Case-study ask: name
      the specific achievement, ask whether they would be willing to share it as a customer case study, and say the marketing
      team does all the writing. Speaker-opportunity ask: mention an upcoming conference or webinar and ask whether they would
      be interested in speaking. Roadmap-feedback ask: say they are using {product_brand} in interesting ways and ask for
      20 minutes of product roadmap feedback.'
  - id: s4
    builds: recommendation
    uses:
    - s2
    - advocacy_ready_segment
    - in_app_surface
    instruction: Configure an in-app recommendation surface on the customer dashboard that activates for users in {advocacy_ready_segment}.
      Show two or three advocacy actions for the user to choose from, each with an effort estimate (3 min, 15 min or 1 hour)
      and the return it offers (recognition, referral reward or speaking visibility). Keep it soft and discoverable, not interruptive,
      so users can volunteer.
  - id: s5
    builds: journey
    uses:
    - s2
    - s3
    - s4
    - advocacy_ready_segment
    - advocacy_action_event
    - advocacy_decline_event
    - active_advocate_tag
    - ask_delay
    - follow_up_delay
    - journey_timeout
    instruction: 'Build a journey on {advocacy_ready_segment}. Touch 1 at {ask_delay} after the moment is detected: send the
      advocacy ask email matching the user''s recommended ask from "Write one ask per moment". Touch 2 on the same day as
      touch 1: activate the in-app surface from "Let them volunteer in the app". Touch 3 at {follow_up_delay} after touch
      1, only if the user engaged with touch 1 or the in-app surface: send a light follow-up with one concrete next step,
      such as the referral link for referral asks. If the user completes an advocacy action, log an advocacy event and tag
      the user as an {active_advocate_tag} for cross-team awareness, and prioritize them for future advocacy opportunities.
      Exit on a completed action, an explicit decline from {advocacy_decline_event}, or a timeout of {journey_timeout}. Never
      send more than these touches.'
  - id: s6
    builds: report
    uses:
    - s1
    - s2
    - s3
    - s4
    - s5
    - advocate_threshold
    - advocacy_ask_sent_event
    - advocacy_action_event
    instruction: 'Compose an advocacy program dashboard showing: weekly advocacy-moment detection volume; ask-to-action conversion
      rate by ask type from {advocacy_ask_sent_event.ask_type} against {advocacy_action_event.action_type}, comparing referral
      volume with review long-term value; a top advocates list of users with {advocate_threshold} or more completed {advocacy_action_event}
      actions as the inner-circle list; and downstream attribution of reviews to review-site score, referrals to new pipeline,
      and case studies to sales materials.'
---

# Advocacy asks at the right moment

Slash command: /milestone-driven-advocacy-asks

## Step 1: Spot the goodwill moments

Create an AI-derived attribute 'active_advocacy_moment' on the User/Account object. Detects natural advocacy windows (when goodwill is highest). Inputs: (a) first-value-achieved events (key activation milestone), (b) expansion-completed events (account just upgraded), (c) renewal-closed events (just renewed for another term), (d) high-engagement-streak (consecutive weeks of strong activity), (e) customer-success-milestone (reached usage benchmark, completed initial use case), (f) explicit positive support sentiment, (g) NOT during friction or churn-risk. Output: object with moment_type, moment_strength (high/medium), recommended_ask (review / referral / case-study / speaker-opportunity / roadmap-feedback), and ask_recipient_role (champion / economic-buyer / power-user).

## Step 2: Find who is ready to be asked

Build a segment 'Advocacy-ready' capturing users where active_advocacy_moment is high-strength in the last 7 days AND the user hasn't been asked for an advocacy action in the last 90 days (avoid donor fatigue) AND there's no active friction/churn signal (the timing is genuinely good, not just numerically positive). Partitioned by recommended_ask so the journey routes accordingly. Use the result of "Spot the goodwill moments".

## Step 3: Write one ask per moment

Generate advocacy-ask email variants per recommended_ask. Review ask: 'You just [hit milestone]: would you share your experience publicly? Takes 3 minutes.' Includes one-click links to G2, Capterra, or the relevant review site, pre-filled where the platform allows. Referral ask: 'You're [in top X% of users / just expanded / just renewed]: know anyone who'd benefit from [Product]? Here's your referral code for [reward].' Case-study ask: 'Your team's [specific achievement] is a great story: would you be willing to share it as a customer case study? Our marketing team will do all the writing.' Speaker-opportunity ask: 'We have a [conference / webinar] coming up (would you be interested in speaking?' Roadmap-feedback ask: 'You're using [Product] in such interesting ways) can we get 20 minutes for product roadmap feedback?' Tone: peer-respectful, never transactional. Send-from: named CSM or success lead, never marketing@. Use the result of "Spot the goodwill moments", "Find who is ready to be asked".

## Step 4: Let them volunteer in the app

Configure a recommendation surface 'Advocacy opportunities' that activates for advocacy-ready users in the in-app dashboard. Shows the user 2-3 advocacy actions they could take, each with a clear effort estimate ('3 min', '15 min', '1 hour') and what the user gets in return (recognition, referral reward, speaking visibility). Soft-surface, discoverable not interruptive. Lets the user volunteer rather than only being asked. Use the result of "Spot the goodwill moments", "Find who is ready to be asked".

## Step 5: Ask once, follow up once

Build a journey wired to advocacy-ready segment. Touch 1 (Day 1 after moment detected): advocacy-ask email matched to recommended_ask. Touch 2 (Day 0 of touch 1): activate recommendation surface in-app. Touch 3 (Day 7, ONLY if user engaged with touch 1 OR rec-surface): light follow-up with concrete next step ('You said you'd love to refer someone: here's the link to send them'). Branch: if user submits an advocacy action (review left / referral submitted / case-study agreed / etc), tag the user as 'active advocate' for cross-team awareness AND ensure they're prioritized for future advocacy opportunities. Exit on: action completed (success: log advocacy_event), explicit decline (respect), or 14-day timeout. No badgering. Use the result of "Spot the goodwill moments", "Find who is ready to be asked", "Write one ask per moment", "Let them volunteer in the app".

## Step 6: See which asks get a yes

Compose an advocacy program dashboard: advocacy-moment detection volume per week, ask-to-action conversion rate by ask type (which advocacy asks actually convert: referrals usually beat reviews in volume but reviews beat referrals in long-term value), top advocates (users who have completed 3+ advocacy actions: this is the inner-circle list to nurture specially), and downstream attribution (reviews influencing G2 score, referrals creating new pipeline, case studies appearing in sales decks). Reframes CS work from 'retention cost-center' to 'pipeline contributor'. Use the result of "Spot the goodwill moments", "Find who is ready to be asked", "Write one ask per moment", "Let them volunteer in the app", "Ask once, follow up once".
