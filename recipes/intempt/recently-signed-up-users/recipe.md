---
frontmatter_id: recently-signed-up-users
slash_command: /recently-signed-up-users
description: Everyone whose first session was within the last 30 days, with a welcome email drafted and a note drafted for the onboarding team while the activation window is still open.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a list of users whose first session fell within the last 30 days, then drafts a welcome email and an onboarding
    team note for them while the activation window is open.
  parameters:
  - name: window
    type: duration
    label: Recent signup window
    default: 30 d
    required: false
  - name: welcome_tone
    type: enum
    label: Welcome email tone
    default: warm and encouraging
    required: false
    options:
    - warm and encouraging
    - neutral
    - formal
  - name: welcome_sentences
    type: number
    label: Welcome email length in sentences
    default: 3
    required: false
  requirements:
  - slot: session_start
    kind: event
    meaning: A customer started a session in the product
  - slot: onboarding_team_list
    kind: destination
    meaning: Distribution list for the onboarding team that receives internal notes
    channel: email
  - slot: first_week_action
    kind: knowledge
    meaning: The single product action most worth taking in a new user's first week, with its in-product link
  steps:
  - id: s1
    builds: segment
    uses:
    - session_start
    - window
    instruction: Build a segment named "Recently Signed-Up Users" of users who did {session_start} at least once in the last
      {window} and did not do {session_start} more than {window} ago.
  - id: s2
    builds: email
    uses:
    - s1
    - first_week_action
    - welcome_sentences
    - welcome_tone
    instruction: Generate a designed marketing email for the users in "Recently Signed-Up Users" welcoming them and pointing
      to {first_week_action}. Write {welcome_sentences} sentences in a {welcome_tone} tone with no discount language. Include
      one button linking to that action inside the product. This drafts the email only; a person still sends it. If the brand
      kit has no logo, use the brand name as a plain text header; the button links to the URL chosen for this run.
  - id: s3
    builds: email_plain
    uses:
    - s1
    - onboarding_team_list
    instruction: 'Generate a plain-text email addressed to {onboarding_team_list}. For each user in "Recently Signed-Up Users",
      name their email address so the team can check in while the activation window is still open. This drafts the email only;
      a person still sends it. Plain text only: no HTML tags, no markup and no unsubscribe line. Take the names or addresses
      from the member list of the step that built the segment (at most 20, then how many more); never write a placeholder
      or ask the reader to paste anything in. If no member list is available, name the segment and say it can be opened in
      Segments.'
---

# Recently Signed-Up Users

Slash command: /recently-signed-up-users

## Step 1: Build the new signup list

Build a segment of users named "Recently Signed-Up Users". A user is in the segment only when all of these are true: they did the Session start event at least once in the last 30 days; they did not do the Session start event more than 30 days ago.

## Step 2: Draft a welcome email

Generate a designed marketing email for the users in "Recently Signed-Up Users" welcoming them and pointing to the one action most worth taking in their first week. Three sentences, warm and encouraging tone, no discount language, one button linking to the first-week action URL chosen for this run. If the brand kit has no logo, use the brand name as a plain text header. Use the result of "Build the new signup list". This drafts the email only; a person still sends it.

## Step 3: Draft a note for onboarding

Generate a plain-text email to the onboarding team distribution list. List the email addresses of the users in "Recently Signed-Up Users", taken from the member list in the result of "Build the new signup list" (at most 20, then say how many more there are). If that result carries no member list, write no placeholder and do not ask the reader to paste anything in; say instead that the users are saved as the segment "Recently Signed-Up Users" and can be opened in Segments. Say the team can check in while the activation window is still open. Plain text only: no HTML tags, no formatting markup and no unsubscribe line, because this is an internal note to the team. This drafts the email only; a person still sends it.
