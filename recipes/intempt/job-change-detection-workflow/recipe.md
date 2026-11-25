---
frontmatter_id: job-change-detection-workflow
slash_command: /job-change-detection-workflow
description: When a champion contact changes employer, emails the account owner to protect the old account, with likely replacement
  contacts, and flags the new company as a warm lead.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Alerts the team by email when a champion changes jobs, with replacement contacts at the old account and the new
    company to pursue.
  parameters:
  - name: sla_business_days
    type: number
    label: Business days the owner has to reach out
    default: 5
    required: false
  - name: warm_window
    type: duration
    label: How recent a move counts as warm
    default: 30 d
    required: false
  - name: alert_recipients
    type: string
    label: Email addresses of the AE / CSM and SDR team alerted about champion moves
    required: true
  requirements:
  - slot: champion_contact
    kind: attribute
    meaning: User attribute that is true when the person is a champion or economic buyer on a customer account or open deal
  - slot: job_change_event
    kind: event
    meaning: A contact changed employer
    properties:
    - name: previous_company
      type: string
      meaning: Company the contact left
      optional: false
    - name: new_company
      type: string
      meaning: Company the contact joined
      optional: false
  - slot: ae_owner
    kind: attribute
    meaning: Name of the AE or CSM assigned to the contact's account
    optional: true
  - slot: product_activity
    kind: event
    meaning: A user used the product (a session or feature action)
  steps:
  - id: s1
    builds: segment
    uses:
    - champion_contact
    - job_change_event
    - warm_window
    instruction: Build a new segment of users named "Champions who changed jobs". A user is in it when their {champion_contact}
      attribute is true and they did {job_change_event} in the last {warm_window}.
  - id: s2
    builds: automation
    uses:
    - s1
    - job_change_event
    - ae_owner
    - product_activity
    - sla_business_days
    - alert_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that starts when a user enters the segment from "Find champions who moved". It analyzes
      the user''s old account and finds the 3 other users at that account with the most {product_activity} events in the last
      30 days, as replacement contacts. Then it emails {alert_recipients} one plain-text alert with: the champion''s name,
      {job_change_event.previous_company}, {job_change_event.new_company}, their {ae_owner}; the 3 replacement contacts with
      name and email; a line asking the owner to reach the old account within {sla_business_days} business days; and a line
      flagging {job_change_event.new_company} as a warm lead for outreach. Nothing is sent to the champion.'
---

# Follow a champion who moves

Slash command: /job-change-detection-workflow

## Step 1: Find champions who moved

Build a new segment of users named "Champions who changed jobs". A user is in it when their champion contact attribute is true and they did job change event in the last 30 d.

## Step 2: Run both plays on a move

Build an automation that starts when a user enters the segment from "Find champions who moved". It analyzes the user's old account and finds the 3 other users at that account with the most product activity events in the last 30 days, as replacement contacts. Then it emails the email addresses of the AE / CSM and SDR team alerted about champion moves one plain-text alert with: the champion's name, previous company, new company, their ae owner; the 3 replacement contacts with name and email; a line asking the owner to reach the old account within 5 business days; and a line flagging new company as a warm lead for outreach. Nothing is sent to the champion.
