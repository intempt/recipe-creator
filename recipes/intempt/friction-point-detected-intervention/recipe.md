---
frontmatter_id: friction-point-detected-intervention
slash_command: /friction-point-detected-intervention
description: Detects where users get stuck in the product, shows in-app help at that spot, emails a fix if they stay stuck,
  and alerts the customer success team when a high-value user is still stuck.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Detects where users get stuck in the product and rescues them with in-app help, a tutorial email and an alert to
    customer success for high-value users who stay stuck.
  parameters:
  - name: friction_window
    type: duration
    label: Window friction is looked for in
    default: 7 d
    required: false
  - name: abandon_return_hours
    type: number
    label: Hours without return that make a setup step abandoned
    default: 24
    required: false
  - name: repeat_attempt_threshold
    type: number
    label: Failed attempts on the same element that count as stuck
    default: 3
    required: false
  - name: email_delay
    type: duration
    label: Wait before the fix email
    default: 4 h
    required: false
  - name: escalation_delay
    type: duration
    label: Wait before alerting customer success
    default: 24 h
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the customer success team that get the alert
    required: true
  requirements:
  - slot: product_usage_event
    kind: event
    meaning: A customer performed an action or hit an error inside the product (form submits, button clicks, setup steps,
      errors)
    properties:
    - name: element
      type: string
      meaning: The form, button or setup step acted on
      optional: false
    - name: location
      type: string
      meaning: Where in the product the action happened
      optional: false
    - name: outcome
      type: string
      meaning: 'Result of the action: success, failed, error, started'
      optional: false
  - slot: in_app_messaging
    kind: destination
    meaning: A destination that delivers emails to users
    channel: email
  - slot: high_value_flag
    kind: attribute
    meaning: A user attribute that is true for high-value users
  - slot: product_brand
    kind: brand
    meaning: The company brand voice and product name used in messages
  - slot: help_content_library
    kind: knowledge
    meaning: Product help articles and tutorials for common blockers
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - product_usage_event
    - friction_window
    - abandon_return_hours
    - repeat_attempt_threshold
    instruction: 'Create a computed user attribute named "friction_location". Its value is the {product_usage_event.location}
      of the user''s latest friction in the last {friction_window}, and empty when there is none. Friction is any one of:
      (a) {product_usage_event} with {product_usage_event.outcome} "failed" {repeat_attempt_threshold} or more times on the
      same {product_usage_event.element} within one hour; (b) {product_usage_event} with outcome "error" and no outcome "success"
      on the same element in the next hour; (c) outcome "started" on a setup step with no outcome "success" on that step and
      no {product_usage_event} at all for {abandon_return_hours} hours after it. Friction ends when the user does outcome
      "success" on that element.'
  - id: s2
    builds: segment
    uses:
    - s1
    dependsOn:
    - s1
    instruction: Build a new segment of users named "Stuck Users". A user is in it when their friction_location attribute
      from "Detect where people get stuck" has a value.
  - id: s3
    builds: page
    uses:
    - s2
    - help_content_library
    - product_brand
    dependsOn:
    - s2
    instruction: 'Create in-app help for users in the segment from "Find users who are stuck", shown at the product location
      named in their friction_location attribute while they are in the product. For a failed form or button: a help bubble
      with the two or three steps most users take there. For an error: a short explanation of the error and how to fix it,
      shown where it appeared. For an abandoned setup step: a tooltip at that step with the answer to the most common blocker.
      Content from {help_content_library}, in the voice of {product_brand}; friendly, never salesy; each piece can be dismissed.'
  - id: s4
    builds: email
    uses:
    - s2
    - help_content_library
    - product_brand
    dependsOn:
    - s2
    instruction: Write an email for users in the segment from "Find users who are stuck", in the voice of {product_brand}.
      The subject names the product location from their friction_location attribute, for example "Stuck on importing contacts?
      Here is the fix". The body gives the fix in three to five short steps from {help_content_library} and one button that
      takes them back to that location in the product. Specific to the location, never a generic "we noticed you got stuck".
      If the brand kit has no logo, use the brand name as a plain text header.
  - id: s5
    builds: automation
    uses:
    - s2
    - s4
    - in_app_messaging
    - high_value_flag
    - email_delay
    - escalation_delay
    - alert_recipients
    dependsOn:
    - s2
    - s4
    instruction: Build an automation triggered when a user enters the segment from "Find users who are stuck". After {email_delay},
      if the user is still in the segment, it sends the email from "Email the fix if that misses" through {in_app_messaging}.
      After a further {escalation_delay}, if the user is still in the segment and their {high_value_flag} attribute is true,
      it emails an alert to {alert_recipients} with the user's name, email and friction_location. It stops for a user as soon
      as they leave the segment. Each user gets the email at most once in 7 days.
---

# Friction rescue

Slash command: /friction-point-detected-intervention

## Step 1: Detect where people get stuck

Create a computed user attribute named "friction_location". Its value is the location of the user's latest friction in the last 7 d, and empty when there is none. Friction is any one of: (a) product usage event with outcome "failed" 3 or more times on the same element within one hour; (b) product usage event with outcome "error" and no outcome "success" on the same element in the next hour; (c) outcome "started" on a setup step with no outcome "success" on that step and no product usage event at all for 24 hours after it. Friction ends when the user does outcome "success" on that element.

## Step 2: Find users who are stuck

Build a new segment of users named "Stuck Users". A user is in it when their friction_location attribute from "Detect where people get stuck" has a value.

## Step 3: Help them inside the app

Create in-app help for users in the segment from "Find users who are stuck", shown at the product location named in their friction_location attribute while they are in the product. For a failed form or button: a help bubble with the two or three steps most users take there. For an error: a short explanation of the error and how to fix it, shown where it appeared. For an abandoned setup step: a tooltip at that step with the answer to the most common blocker. Content from help content library, in the voice of product brand; friendly, never salesy; each piece can be dismissed.

## Step 4: Email the fix if that misses

Write an email for users in the segment from "Find users who are stuck", in the voice of product brand. The subject names the product location from their friction_location attribute, for example "Stuck on importing contacts? Here is the fix". The body gives the fix in three to five short steps from help content library and one button that takes them back to that location in the product. Specific to the location, never a generic "we noticed you got stuck". If the brand kit has no logo, use the brand name as a plain text header.

## Step 5: Escalate if they stay stuck

Build an automation triggered when a user enters the segment from "Find users who are stuck". After 4 h, if the user is still in the segment, it sends the email from "Email the fix if that misses" through in app messaging. After a further 24 h, if the user is still in the segment and their high value flag attribute is true, it emails an alert to the email addresses of the customer success team that get the alert with the user's name, email and friction_location. It stops for a user as soon as they leave the segment. Each user gets the email at most once in 7 days.
