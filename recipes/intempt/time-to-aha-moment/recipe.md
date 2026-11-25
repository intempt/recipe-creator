---
frontmatter_id: time-to-aha-moment
slash_command: /time-to-aha-moment
description: Emails a weekly digest of how long new users take to reach their first activation goal, with the median, the
  share who never activate and the split by signup source.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Emails a weekly digest of time from signup to first activation goal, with median, share within 24 hours, never-activated
    share and signup source split.
  parameters:
  - name: activation_journey_id
    type: string
    label: Journey whose goal marks activation
    required: true
  - name: cohort_window
    type: duration
    label: Signup cohort window
    default: 90 d
  - name: activation_window
    type: duration
    label: Activation window
    default: 14 d
  - name: top_sources
    type: number
    label: Number of top signup sources to break down
    default: 6
  - name: never_alert_threshold
    type: number
    label: Alert threshold for share of users who never activate (%)
    default: 50
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: user_created_event
    kind: event
    meaning: A new user account was created (signup)
  - slot: journey_goal_completed_event
    kind: event
    meaning: A user completed a journey goal in the activation journey
    properties:
    - name: journey_id
      type: string
      meaning: Identifier of the journey the goal belongs to
      optional: false
  - slot: user_utm_source_attribute
    kind: attribute
    meaning: The user's first-touch signup source (UTM source)
  steps:
  - id: s1
    builds: automation
    uses:
    - user_created_event
    - journey_goal_completed_event
    - user_utm_source_attribute
    - activation_journey_id
    - cohort_window
    - activation_window
    - top_sources
    - never_alert_threshold
    - digest_recipients
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did {user_created_event}
      between {activation_window} and {cohort_window} ago, and the time from {user_created_event} to their first {journey_goal_completed_event}
      with {journey_goal_completed_event.journey_id} equal to {activation_journey_id}. It writes: the % activated within 30
      minutes, 2 hours, 24 hours, 3 days, 7 days and {activation_window}; the % that never activated within {activation_window};
      the median time to activate; the same median per {user_utm_source_attribute} for the top {top_sources} sources, naming
      the slowest. Then it emails these figures as plain-text lines, each with its window, to {digest_recipients}. When the
      never-activated share is above {never_alert_threshold}%, the email''s first line says so. It compares the 24-hour share
      with 10% (median) and 30% (top quartile). Nothing else is sent.'
---

# Time to first value

Slash command: /time-to-aha-moment

## Step 1: Email the weekly time to value digest

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes users who did user created event between 14 d and 90 d ago, and the time from user created event to their first journey goal completed event with journey id equal to the journey whose goal marks activation. It writes: the % activated within 30 minutes, 2 hours, 24 hours, 3 days, 7 days and 14 d; the % that never activated within 14 d; the median time to activate; the same median per user utm source attribute for the top 6 sources, naming the slowest. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. When the never-activated share is above 50%, the email's first line says so. It compares the 24-hour share with 10% (median) and 30% (top quartile). Nothing else is sent.
