---
frontmatter_id: high-cart-value-abandoners
slash_command: /high-cart-value-abandoners
description: Visitors who just submitted a form, flagged to sales the same day so follow-up happens while interest is highest.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: slack, severity: recommended }
---

# Instant Lead Alert

Slash command: /high-cart-value-abandoners

## Step 1: Build the form submitter list

Build a segment of users named "Form Submitters Today". A user is in the segment only when all of these are true: triggered "Submit on" at least once in the last 1 day.

## Step 2: Alert sales

Generate a Slack message to the sales team channel. Say how many users are in "Form Submitters Today" right now, so reps know when a form submission just came in. Use the result of "Build the form submitter list".
