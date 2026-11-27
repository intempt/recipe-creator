---
frontmatter_id: conditional-enrichment-by-tier
slash_command: /conditional-enrichment-by-tier
description: Enriches each new account with a basic look first, then goes deep only on enterprise accounts and standard on
  mid-market ones, and emails a monthly count of accounts per tier.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds an automation that enriches new accounts by tier, so paid enrichment goes mostly to high-value accounts,
    plus a monthly digest of new accounts per tier.
  parameters:
  - name: enterprise_min_company_size
    type: number
    label: Employees above which an account is enterprise
    default: 500
    required: false
  - name: mid_market_min_company_size
    type: number
    label: Smallest mid-market company (employees)
    default: 50
    required: false
  - name: target_industries
    type: string
    label: Industries that count as mid-market fit (comma separated)
    required: true
  - name: cost_report_window
    type: duration
    label: Window counted in the monthly digest
    default: 30 d
    required: false
  - name: brief_recipients
    type: string
    label: Email addresses that get the enterprise account briefs
    required: true
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: account_created_event
    kind: event
    meaning: An account was created
    properties:
    - name: company_size
      type: number
      meaning: Number of employees at the company
      optional: false
    - name: industry
      type: string
      meaning: Industry of the company
      optional: false
    - name: country
      type: string
      meaning: Country of the company
      optional: true
    - name: domain
      type: string
      meaning: Company web domain
      optional: false
  steps:
  - id: s1
    builds: automation
    uses:
    - account_created_event
    - enterprise_min_company_size
    - mid_market_min_company_size
    - target_industries
    - brief_recipients
    instruction: 'Build an automation that starts when an account does {account_created_event}. It splits by tier first, before
      any enrichment, on {account_created_event.company_size} and {account_created_event.industry} as the event carries them
      (an account with no company size goes to the last branch): (a) company size above {enterprise_min_company_size}: enrich
      the record in full, using {account_created_event.domain}, with company data, technology stack, decision-makers by title,
      funding and recent news, then add an analysis step that writes a short brief on the account''s priorities, competitive
      position and buying signals and emails it to {brief_recipients}; (b) company size from {mid_market_min_company_size}
      to {enterprise_min_company_size} and industry in {target_industries}: enrich the record, using {account_created_event.domain},
      with basic company data, one main contact (CEO, founder or owner) and the company technology stack; (c) every other
      account (the default branch): no enrichment at all, so it costs nothing. Then Blu asks to start it.'
  - id: s2
    builds: automation
    uses:
    - s1
    - account_created_event
    - enterprise_min_company_size
    - mid_market_min_company_size
    - target_industries
    - cost_report_window
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes accounts
      that did {account_created_event} in the last {cost_report_window} and writes these figures: the number of new accounts;
      how many fell into each tier of the automation from "Enrich new accounts by tier": enterprise (company size above {enterprise_min_company_size}),
      mid-market (company size from {mid_market_min_company_size} to {enterprise_min_company_size} and industry in {target_industries})
      and low-fit (all others); each tier''s share of new accounts; the same counts for the {cost_report_window} before. Then
      it emails these figures as plain-text lines, each with its window, to {digest_recipients}. Nothing else is sent.'
---

# Enrich by account tier

Slash command: /conditional-enrichment-by-tier

## Step 1: Enrich new accounts by tier

Build an automation that starts when an account does account created event. It splits by tier first, before any enrichment, on company size and industry as the event carries them (an account with no company size goes to the last branch): (a) company size above 500: enrich the record in full, using domain, with company data, technology stack, decision-makers by title, funding and recent news, then add an analysis step that writes a short brief on the account's priorities, competitive position and buying signals and emails it to the email addresses that get the enterprise account briefs; (b) company size from 50 to 500 and industry in the industries that count as mid-market fit (comma separated): enrich the record, using domain, with basic company data, one main contact (CEO, founder or owner) and the company technology stack; (c) every other account (the default branch): no enrichment at all, so it costs nothing. Then Blu asks to start it.

## Step 2: Email the monthly tier digest

Build an automation that runs on the 1st of every month at 08:00 on a schedule. Each run it analyzes accounts that did account created event in the last 30 d and writes these figures: the number of new accounts; how many fell into each tier of the automation from "Enrich new accounts by tier": enterprise (company size above 500), mid-market (company size from 50 to 500 and industry in the industries that count as mid-market fit (comma separated)) and low-fit (all others); each tier's share of new accounts; the same counts for the 30 d before. Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
