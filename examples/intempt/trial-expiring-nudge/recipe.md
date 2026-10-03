---
id: trial-expiring-nudge
title: Nudge trials before they expire
slash_command: /trial-expiring-nudge
group: Segments
owner: intempt
summary: >-
  Finds trial users whose trial ends this week and who have not upgraded, then sends them a
  short upgrade email.
description: >-
  For SaaS teams with a free trial who want to convert more trials in the final week.
version: 1.0.0
classification:
  product:
    - segments
    - marketing
  mode:
    - saas
  complexity: quick
  tags:
    - trial
    - conversion
prerequisites:
  events:
    - value: subscription_created
      severity: blocking
steps:
  - id: s1
    title: Find trials ending this week
    summary: >-
      Users on the trial plan whose trial ends in the next 7 days and who have not
      subscribed in the last 14 days.
    builds: segment
    description: |-
      Build a segment of users named "Trials ending this week".
      Include users whose plan_name attribute is "trial"
      and whose end_date attribute is within the next 7 days.
      Exclude users who did the subscription_created event in the last 14 days.
      Refresh the segment daily.
  - id: s2
    title: Write the upgrade email
    summary: >-
      A three-sentence email that says when the trial ends and how to keep their work.
    builds: email_html
    description: |-
      Write a designed email for the users in "Find trials ending this week".
      Subject line under 50 characters that names the day the trial ends.
      Three sentences in the brand voice: the trial ends on their end_date, their data stays
      if they upgrade, and one button labelled "Keep my workspace" that links to the billing page.
      No discount.
    dependsOn:
      - s1
outputs:
  - key: trials_ending
    producedByStep: s1
    type: segment
    description: Trial users whose trial ends in the next 7 days.
  - key: upgrade_email
    producedByStep: s2
    type: email_html
    description: The upgrade email for that segment.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Nudge trials before they expire

Finds trial users whose trial ends this week and who have not upgraded, then sends them a short upgrade email.

## Steps

1. **Find trials ending this week** (builds segment)

   Users on the trial plan whose trial ends in the next 7 days and who have not subscribed in the last 14 days.

2. **Write the upgrade email** (builds email_html)

   A three-sentence email that says when the trial ends and how to keep their work.

## What you end up with

- **trials_ending** (segment): Trial users whose trial ends in the next 7 days.
- **upgrade_email** (email_html): The upgrade email for that segment.

## Availability

Install now: every step builds something the engine supports today.
