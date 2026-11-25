---
frontmatter_id: ai-account-research-deep-dive
slash_command: /ai-account-research-deep-dive
description: When a high-tier account is created, reads its website, pulls out the decision makers, scores the fit against
  your ICP and emails the rep a research brief with a draft opener to edit.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: 'Emails reps a research brief for each new high-tier account: what the company does, decision makers, ICP fit score
    with reasons and a draft opener to edit, never sent.'
  parameters:
  - name: fit_window
    type: duration
    label: How far back blog posts are read
    default: 30 d
    required: false
  - name: opener_tone
    type: enum
    label: Tone of the draft opener
    default: conversational
    required: false
    options:
    - conversational
    - formal
    - direct
  - name: alert_recipients
    type: string
    label: Email addresses of the reps who get the briefs
    required: true
  requirements:
  - slot: high_tier_account_created
    kind: event
    meaning: An account was created that qualifies as high-tier by ICP fit or domain tier
    properties:
    - name: domain_tier
      type: string
      meaning: The account's domain tier
      optional: false
  - slot: account_domain
    kind: attribute
    meaning: The web domain of an account
  - slot: icp_definition
    kind: knowledge
    meaning: 'The ideal customer profile: target industry, company size, technology and use cases'
  steps:
  - id: s1
    builds: automation
    uses:
    - high_tier_account_created
    - account_domain
    - icp_definition
    - fit_window
    - opener_tone
    - alert_recipients
    instruction: 'Build an automation triggered when {high_tier_account_created} happens for an account. It runs an analysis
      step that reads the public website at the account''s {account_domain} attribute (home, about, team or leadership, pricing,
      customers, and blog posts from the last {fit_window}) and writes: a one-sentence company description; primary product;
      target market; recent priorities; decision makers with names and titles from the leadership page; competitors and partners
      mentioned; an ICP fit score from 0 to 100 against {icp_definition} with a one-sentence reason; and a 2 to 3 sentence
      outreach opener in a {opener_tone} tone that starts from one specific fact found on the site. Every finding names the
      page it came from; a finding the site does not support is left out. Then it emails this brief as plain text to {alert_recipients},
      with the account name in the subject. Nothing is sent to the account.'
---

# AI account research

Slash command: /ai-account-research-deep-dive

## Step 1: Research each new high-tier account

Build an automation triggered when high tier account created happens for an account. It runs an analysis step that reads the public website at the account's account domain attribute (home, about, team or leadership, pricing, customers, and blog posts from the last 30 d) and writes: a one-sentence company description; primary product; target market; recent priorities; decision makers with names and titles from the leadership page; competitors and partners mentioned; an ICP fit score from 0 to 100 against icp definition with a one-sentence reason; and a 2 to 3 sentence outreach opener in a conversational tone that starts from one specific fact found on the site. Every finding names the page it came from; a finding the site does not support is left out. Then it emails this brief as plain text to the email addresses of the reps who get the briefs, with the account name in the subject. Nothing is sent to the account.
