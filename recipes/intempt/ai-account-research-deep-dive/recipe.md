---
frontmatter_id: ai-account-research-deep-dive
slash_command: /ai-account-research-deep-dive
description: Reads a target account's website, pulls out the decision makers, scores the fit against your ICP, and drafts an opener for the rep to edit.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - saas-b2b-tech
portable:
  summary: Reads a target account's website, pulls out decision makers, scores ICP fit, and drafts a review-only opener so
    reps can act without manual research.
  parameters:
  - name: fit_window
    type: duration
    label: Lookback window for recent blog posts
    default: 30 d
    required: false
  - name: high_tier_only
    type: boolean
    label: Research only high-tier accounts
    default: true
    required: false
  - name: opener_tone
    type: enum
    label: Tone of drafted opener
    default: conversational
    required: false
    options:
    - formal
    - conversational
    - direct
  - name: digest_frequency
    type: enum
    label: Digest frequency for SDR managers
    default: daily
    required: false
    options:
    - daily
    - weekly
  requirements:
  - slot: high_tier_account_created
    kind: event
    meaning: An account was created that qualifies as high-tier by ICP fit or domain-tier flag
    properties:
    - name: icp_fit
      type: number
      meaning: ICP fit indicator of the account
      optional: true
    - name: domain_tier
      type: string
      meaning: Domain tier flag of the account
      optional: true
  - slot: target_account_list
    kind: segment
    meaning: A list of target accounts selected by a rep from a list view for research
    optional: true
  - slot: account_domain
    kind: attribute
    meaning: The web domain of an account
  - slot: icp_definition
    kind: knowledge
    meaning: 'The ideal customer profile: target industry, company size, technology, and use cases'
  - slot: account_research_fields
    kind: attribute
    meaning: 'Account attributes to store research output: company description, primary product, recent priorities, decision
      makers, competitors, fit score, fit reasoning, drafted opener, research completed timestamp'
  - slot: sdr_manager_team
    kind: destination
    meaning: A destination where SDR managers receive the daily research digest
    optional: true
    channel: email
  steps:
  - id: s1
    builds: automation
    uses:
    - high_tier_account_created
    - target_account_list
    - high_tier_only
    instruction: 'Create a workflow ''AI account deep research'' triggered by {high_tier_account_created} when high-tier filtering
      is enabled by {high_tier_only}, OR by a manual trigger from a list view on {target_account_list} (for example, research
      these 50 accounts). Goal: produce a structured account-intelligence brief a rep can act on without doing their own research.'
  - id: s2
    builds: workflow
    uses:
    - account_domain
    - fit_window
    - s1
    instruction: Configure a web scrape step targeting the account's {account_domain}. Fetch the homepage hero copy, About
      page, Team/Leadership page, Pricing page (if it exists), Customers page, and blog posts published within {fit_window}.
      Return raw page content for the summarization step. Respect robots.txt and rate-limit requests per domain.
  - id: s3
    builds: knowledge
    uses:
    - s1
    - s2
    instruction: 'Configure an AI research step that takes the scraped content from "Read their website" and produces a structured
      summary with: (a) a one-sentence company description, (b) primary product or service, (c) ICP signals including target
      market and stated customer types, (d) recent priorities inferred from homepage and blog (for example ''expanding internationally'',
      ''launching AI features''), (e) decision-maker names and titles from the leadership page, (f) mentioned competitors
      and partners, and (g) a confidence score for each finding.'
  - id: s4
    builds: attribute
    uses:
    - s1
    - s3
    - icp_definition
    - account_research_fields
    instruction: 'Configure a second AI step that scores ICP fit using the "Summarise what they do" output and {icp_definition}
      (industry, size, technology, use cases). Output a numeric score from 0 to 100 and a reasoning string in the form ''Strong
      fit because they are a B2B SaaS company in the target industry with about 50 employees and recent Series A funding:
      matches our ICP for growth-stage teams''. Store the result as fit_score and fit_reasoning on {account_research_fields}.'
  - id: s5
    builds: email
    uses:
    - s1
    - s3
    - s4
    - opener_tone
    instruction: 'Configure an AI write step that drafts an outreach opener in a {opener_tone} tone, referencing a specific
      fact from "Summarise what they do" (not generic). Structure it as 2-3 sentences: first a specific fact from the research
      (for example ''I saw your team is expanding into APAC...''), then a value hypothesis (for example ''Teams growing internationally
      typically struggle with X: that is where we help''), then a soft call to action. Store the draft on the account as ai_drafted_opening
      for SDR review and editing. Never send automatically.'
  - id: s6
    builds: attribute
    uses:
    - s1
    - s3
    - s4
    - s5
    - account_research_fields
    instruction: 'Write the results back to the account record in {account_research_fields}: company_description, primary_product,
      recent_priorities, decision_makers_inferred (as an array), competitors_mentioned, fit_score, fit_reasoning, ai_drafted_opening,
      and research_completed_at.'
  - id: s7
    builds: report
    uses:
    - s1
    - s6
    - sdr_manager_team
    - digest_frequency
    instruction: Validate the workflow graph and publish it. Add a {digest_frequency} digest to {sdr_manager_team} summarizing
      new accounts researched and their average fit scores, so SDR managers can audit which accounts the research flags as
      best-fit.
---

# AI account research

Slash command: /ai-account-research-deep-dive

## Step 1: Start on a high value account

Create a workflow 'AI account deep research' triggered by account_created (high-tier accounts only: by ICP fit or domain-tier flag) OR manual trigger from a list view ('research these 50 accounts'). Goal: produce a structured account-intelligence brief that a rep can act on without doing their own research.

## Step 2: Read their website

This step builds a workflow.
Configure web scrape step targeting the account's domain. Fetch: homepage hero copy, About page, Team/Leadership page, Pricing page (if exists), Customers page, recent blog posts. Returns raw page content to feed into the AI summarization step. Respect robots.txt; rate-limit per domain. Use the result of "Start on a high value account".

## Step 3: Summarise what they do

This step builds a workflow.
Configure AI research step that takes the scraped content and produces a structured summary: (a) one-sentence company description, (b) primary product/service, (c) ICP signals (target market, stated customer types), (d) recent priorities inferred from homepage / blog (e.g. 'expanding internationally', 'launching AI features'), (e) decision-maker names + titles from leadership page, (f) any mentioned competitors / partners, (g) confidence score on each finding. Use the result of "Start on a high value account", "Read their website".

## Step 4: Score them against your ICP

This step builds a workflow.
Configure a second AI step that scores ICP fit using the company summary + a provided ICP definition (industry, size, tech, use cases). Output: numeric 0-100 score + reasoning string ('Strong fit because they are a B2B SaaS in [target industry] with ~50 employees and recently raised Series A: matches our ICP for growth-stage teams'). Records a structured fit_score + fit_reasoning attribute. Use the result of "Start on a high value account", "Summarise what they do".

## Step 5: Draft the opening line

This step builds a workflow.
Configure AI write step that produces a draft outreach opener referencing specific findings (not generic). Format: 2-3 sentences referencing a SPECIFIC fact from the research ('I saw your team is expanding into APAC...'), then a value-hypothesis ('Teams growing internationally typically struggle with X: that's where we help'), then a soft CTA. Output stored on the account for SDR review-and-edit, never auto-sent. Use the result of "Start on a high value account", "Summarise what they do", "Score them against your ICP".

## Step 6: Write it onto the account

This step builds a workflow.
Write back to the Account record: company_description, primary_product, recent_priorities, decision_makers_inferred (array), competitors_mentioned, fit_score, fit_reasoning, ai_drafted_opening, research_completed_at. The SDR sees a fully-formed account brief without doing any manual research. Use the result of "Start on a high value account", "Summarise what they do", "Score them against your ICP", "Draft the opening line".

## Step 7: Publish and check the picks

Validate workflow DAG and publish. Add a daily summary digest of new accounts researched + their average fit scores so SDR managers can audit which accounts AI is flagging as best-fit. Use the result of "Start on a high value account", "Write it onto the account".
