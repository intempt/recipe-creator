---
frontmatter_id: compliance-setup
slash_command: /compliance-setup
description: A list of people who never gave marketing consent or have since opted out, so you can exclude them from every marketing send.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a suppression segment of people who never gave marketing consent or have since opted out, so they can be
    excluded from all marketing sends.
  parameters: []
  requirements:
  - slot: subscribed_event
    kind: event
    meaning: A customer gave marketing consent by subscribing
  - slot: unsubscribed_event
    kind: event
    meaning: A customer opted out of marketing by unsubscribing
  steps:
  - id: s1
    builds: segment
    uses:
    - subscribed_event
    - unsubscribed_event
    instruction: 'Build a segment named "Marketing Consent Suppression List". A user is in the segment when any of these is
      true: they have never done {subscribed_event}; or they did {unsubscribed_event} after their most recent {subscribed_event}.'
---

# Marketing consent suppression list

Slash command: /compliance-setup

## Step 1: Build the suppression list

Build a segment of users named "Marketing Consent Suppression List".
A user is in the segment when any of these is true:
- they have never done the Subscribed consent event
- they did the Unsubscribed consent event after their most recent Subscribed consent event
