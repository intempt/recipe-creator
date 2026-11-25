---
frontmatter_id: power-user-pattern-detection
slash_command: /power-user-pattern-detection
description: Detects paying users who repeat manual work (the same report run, repeat exports, the same filter), nudges them
  toward the automation feature that fits, and asks adopters for a review.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Detects users repeating manual work, nudges them in the app and by email toward the automation feature that fits,
    and asks those who adopt it for a review.
  parameters:
  - name: repeat_window
    type: duration
    label: Window repeated reports and exports are counted in
    default: 7 d
    required: false
  - name: repeat_threshold
    type: number
    label: Report runs that count as repeated
    default: 5
    required: false
  - name: export_threshold
    type: number
    label: Exports that count as repeated
    default: 3
    required: false
  - name: filter_threshold
    type: number
    label: Filter uses that count as repeated
    default: 10
    required: false
  - name: filter_window
    type: duration
    label: Window filter uses are counted in
    default: 14 d
    required: false
  - name: dismiss_limit
    type: number
    label: Dismissals before a user is left alone
    default: 3
    required: false
  - name: followup_delay
    type: duration
    label: Wait before the tip email
    default: 3 d
    required: false
  - name: review_delay
    type: duration
    label: Wait after adoption before the review ask
    default: 14 d
    required: false
  requirements:
  - slot: manual_work_events
    kind: event
    meaning: A customer performed a manual action in the product, such as running a report, exporting data or applying a filter
    properties:
    - name: action_type
      type: string
      meaning: 'The kind of action: report_run, export or filter_applied'
      optional: false
  - slot: feature_adoption
    kind: event
    meaning: A customer started using an automation feature such as scheduled reports, the API or saved views
    properties:
    - name: feature_name
      type: string
      meaning: The feature adopted
      optional: false
  - slot: feature_dismissal
    kind: event
    meaning: A customer dismissed a feature suggestion
  - slot: plan_attribute
    kind: attribute
    meaning: The user's current plan name
  - slot: email_channel
    kind: destination
    meaning: Email channel for the tip and review emails
    channel: email
  - slot: review_site_page
    kind: knowledge
    meaning: The public review page link where customers can post a review
    optional: true
  steps:
  - id: s1
    builds: attribute
    uses:
    - manual_work_events
    - repeat_window
    - repeat_threshold
    - export_threshold
    - filter_threshold
    - filter_window
    instruction: 'Create a computed user attribute named "automation_suggestion", refreshed daily. The first rule that matches
      sets the value: "scheduled_reports" when the user did {manual_work_events} with {manual_work_events.action_type} "report_run"
      {repeat_threshold} or more times in the last {repeat_window}; "api_export" when they did it with action_type "export"
      {export_threshold} or more times in the last {repeat_window}; "saved_views" when they did it with action_type "filter_applied"
      {filter_threshold} or more times in the last {filter_window}. Otherwise it is empty.'
  - id: s2
    builds: segment
    uses:
    - s1
    - plan_attribute
    - feature_adoption
    - feature_dismissal
    - dismiss_limit
    dependsOn:
    - s1
    instruction: 'Build a new segment of users named "Manual Work Repeaters". A user is in it when all of these are true:
      their automation_suggestion attribute from "Spot work done the hard way" has a value; their {plan_attribute} attribute
      has a value and is not "free" or "trial"; they did not do {feature_adoption} in the last 90 days; they did {feature_dismissal}
      fewer than {dismiss_limit} times in the last 30 days.'
  - id: s3
    builds: page
    uses:
    - s2
    - repeat_threshold
    dependsOn:
    - s2
    instruction: 'Create an in-app nudge for users in the segment from "Find who could automate it", shown as a small card
      at the moment they repeat the manual action again. Copy by their automation_suggestion attribute: scheduled_reports
      "You have run this report {repeat_threshold} times this week. Schedule it and it lands in your inbox."; api_export "Exporting
      again? Connect the API and the data flows on its own."; saved_views "Save this filter as a view and open it in one click."
      Each card has an "Enable now" button that opens the feature and a dismiss option.'
  - id: s4
    builds: email
    uses:
    - s2
    - review_site_page
    dependsOn:
    - s2
    instruction: 'Write two emails for users in the segment from "Find who could automate it". Email 1, the tip: by their
      automation_suggestion attribute (scheduled reports, API export or saved views), how the feature replaces the work they
      repeat, in three short steps, with one button that opens the feature. Email 2, the review ask, for users who adopted
      the feature: congratulate them on automating it and ask for a short review on the page from {review_site_page}, with
      one button to it. If the brand kit has no logo, use the brand name as a plain text header.'
  - id: s5
    builds: automation
    uses:
    - s2
    - s4
    - feature_adoption
    - feature_dismissal
    - email_channel
    - followup_delay
    - review_delay
    dependsOn:
    - s2
    - s4
    instruction: Build an automation triggered when a user enters the segment from "Find who could automate it". After {followup_delay},
      if the user has not done {feature_adoption} or {feature_dismissal} since entering, it sends email 1 (the tip) from "Write
      the tip and review emails" through {email_channel}. When the user does {feature_adoption} within 30 days of entering,
      it waits {review_delay} and sends email 2 (the review ask) from the same step. Each user gets each email at most once
      in 90 days; nothing else is sent.
---

# Power user pattern detection

Slash command: /power-user-pattern-detection

## Step 1: Spot work done the hard way

Create a computed user attribute named "automation_suggestion", refreshed daily. The first rule that matches sets the value: "scheduled_reports" when the user did manual work events with action type "report_run" 5 or more times in the last 7 d; "api_export" when they did it with action_type "export" 3 or more times in the last 7 d; "saved_views" when they did it with action_type "filter_applied" 10 or more times in the last 14 d. Otherwise it is empty.

## Step 2: Find who could automate it

Build a new segment of users named "Manual Work Repeaters". A user is in it when all of these are true: their automation_suggestion attribute from "Spot work done the hard way" has a value; their plan attribute attribute has a value and is not "free" or "trial"; they did not do feature adoption in the last 90 days; they did feature dismissal fewer than 3 times in the last 30 days.

## Step 3: Nudge them mid task

Create an in-app nudge for users in the segment from "Find who could automate it", shown as a small card at the moment they repeat the manual action again. Copy by their automation_suggestion attribute: scheduled_reports "You have run this report 5 times this week. Schedule it and it lands in your inbox."; api_export "Exporting again? Connect the API and the data flows on its own."; saved_views "Save this filter as a view and open it in one click." Each card has an "Enable now" button that opens the feature and a dismiss option.

## Step 4: Write the tip and review emails

Write two emails for users in the segment from "Find who could automate it". Email 1, the tip: by their automation_suggestion attribute (scheduled reports, API export or saved views), how the feature replaces the work they repeat, in three short steps, with one button that opens the feature. Email 2, the review ask, for users who adopted the feature: congratulate them on automating it and ask for a short review on the page from review site page, with one button to it. If the brand kit has no logo, use the brand name as a plain text header.

## Step 5: Nudge, remind, then let it go

Build an automation triggered when a user enters the segment from "Find who could automate it". After 3 d, if the user has not done feature adoption or feature dismissal since entering, it sends email 1 (the tip) from "Write the tip and review emails" through email channel. When the user does feature adoption within 30 days of entering, it waits 14 d and sends email 2 (the review ask) from the same step. Each user gets each email at most once in 90 days; nothing else is sent.
