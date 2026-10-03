---
id: ai-account-research-deep-dive
title: AI account research
slash_command: /ai-account-research-deep-dive
group: Workflows
owner: intempt
curator: trishik
summary: Reads a target account's website, pulls out the decision makers, scores the fit against your
  ICP, and drafts an opener for the rep to edit.
description: >-
  AI agent autonomously researches a target account (scrapes website, summarizes news, extracts decision-makers,
  scores ICP fit, drafts an opening hypothesis) and populates the Account record. The Claygent-style deep-research
  workflow that turns 30 minutes of SDR research into 2 minutes of AI work.
version: 2.0.0
classification:
  product:
    - sales
  agent: workflow-builder
  mode:
    - b2b
  complexity: advanced
  executionMode: live
  tags:
    - ai-research
    - account-intelligence
    - sdr-productivity
prerequisites:
  events:
    - value: account_created
      severity: blocking
touches:
  reads:
    - The account_created event in your project
  writes:
    - A new workflow, from step 1 "Start on a high value account"
    - A new workflow, from step 2 "Read their website"
    - A new workflow, from step 3 "Summarise what they do"
    - A new workflow, from step 4 "Score them against your ICP"
    - A new workflow, from step 5 "Draft the opening line"
    - A new workflow, from step 6 "Write it onto the account"
    - A new workflow, from step 7 "Publish and check the picks"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Start on a high value account
    summary: >-
      Runs when a high tier account is created, or on demand against a list of accounts. The job is a
      brief a rep can act on without doing any research of their own.
    builds: workflow
    description: >-
      Create a workflow 'AI account deep research' triggered by account_created (high-tier accounts only:
      by ICP fit or domain-tier flag) OR manual trigger from a list view ('research these 50 accounts').
      Goal: produce a structured account-intelligence brief that a rep can act on without doing their
      own research.
  - id: s2
    title: Read their website
    summary: >-
      Fetches the homepage, the about page, the leadership page, pricing if there is one, the customers
      page and recent blog posts. It honours robots.txt and rate limits per domain.
    builds: workflow
    description: >-
      Configure web scrape step targeting the account's domain. Fetch: homepage hero copy, About page,
      Team/Leadership page, Pricing page (if exists), Customers page, recent blog posts. Returns raw page
      content to feed into the AI summarization step. Respect robots.txt; rate-limit per domain. Use the
      result of "Start on a high value account".
    dependsOn:
      - s1
  - id: s3
    title: Summarise what they do
    summary: >-
      From those pages: a one sentence description, the main product, who they sell to, what they are
      pushing on right now, the leadership names and titles, any competitors or partners mentioned, and
      a confidence score on each finding.
    builds: workflow
    description: >-
      Configure AI research step that takes the scraped content and produces a structured summary: (a)
      one-sentence company description, (b) primary product/service, (c) ICP signals (target market, stated
      customer types), (d) recent priorities inferred from homepage / blog (e.g. 'expanding internationally',
      'launching AI features'), (e) decision-maker names + titles from leadership page, (f) any mentioned
      competitors / partners, (g) confidence score on each finding. Use the result of "Start on a high
      value account", "Read their website".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Score them against your ICP
    summary: >-
      A 0 to 100 fit score built from that summary against your ICP definition of industry, size, technology
      and use case, with a written reason for the number.
    builds: workflow
    description: >-
      Configure a second AI step that scores ICP fit using the company summary + a provided ICP definition
      (industry, size, tech, use cases). Output: numeric 0-100 score + reasoning string ('Strong fit because
      they are a B2B SaaS in [target industry] with ~50 employees and recently raised Series A: matches
      our ICP for growth-stage teams'). Records a structured fit_score + fit_reasoning attribute. Use
      the result of "Start on a high value account", "Summarise what they do".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Draft the opening line
    summary: >-
      Two or three sentences citing something specific from the research, then a hypothesis about the
      problem that creates, then a soft ask. Saved for the rep to edit, never sent automatically.
    builds: workflow
    description: >-
      Configure AI write step that produces a draft outreach opener referencing specific findings (not
      generic). Format: 2-3 sentences referencing a SPECIFIC fact from the research ('I saw your team
      is expanding into APAC...'), then a value-hypothesis ('Teams growing internationally typically struggle
      with X: that's where we help'), then a soft CTA. Output stored on the account for SDR review-and-edit,
      never auto-sent. Use the result of "Start on a high value account", "Summarise what they do", "Score
      them against your ICP".
    dependsOn:
      - s1
      - s3
      - s4
  - id: s6
    title: Write it onto the account
    summary: >-
      The description, main product, current priorities, decision makers, competitors, fit score, reasoning,
      drafted opener and the time it ran, all onto the account record.
    builds: workflow
    description: >-
      Write back to the Account record: company_description, primary_product, recent_priorities, decision_makers_inferred
      (array), competitors_mentioned, fit_score, fit_reasoning, ai_drafted_opening, research_completed_at.
      The SDR sees a fully-formed account brief without doing any manual research. Use the result of "Start
      on a high value account", "Summarise what they do", "Score them against your ICP", "Draft the opening
      line".
    dependsOn:
      - s1
      - s3
      - s4
      - s5
  - id: s7
    title: Publish and check the picks
    summary: >-
      The workflow is validated and published, with a daily digest of accounts researched and their average
      fit scores so managers can see what the AI is rating highly.
    builds: workflow
    description: >-
      Validate workflow DAG and publish. Add a daily summary digest of new accounts researched + their
      average fit scores so SDR managers can audit which accounts AI is flagging as best-fit. Use the
      result of "Start on a high value account", "Write it onto the account".
    dependsOn:
      - s1
      - s6
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s6
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# AI account research

Reads a target account's website, pulls out the decision makers, scores the fit against your ICP, and drafts an opener for the rep to edit.

## Steps

1. **Start on a high value account** (builds workflow)

   Runs when a high tier account is created, or on demand against a list of accounts. The job is a brief a rep can act on without doing any research of their own.

2. **Read their website** (builds workflow)

   Fetches the homepage, the about page, the leadership page, pricing if there is one, the customers page and recent blog posts. It honours robots.txt and rate limits per domain.

3. **Summarise what they do** (builds workflow)

   From those pages: a one sentence description, the main product, who they sell to, what they are pushing on right now, the leadership names and titles, any competitors or partners mentioned, and a confidence score on each finding.

4. **Score them against your ICP** (builds workflow)

   A 0 to 100 fit score built from that summary against your ICP definition of industry, size, technology and use case, with a written reason for the number.

5. **Draft the opening line** (builds workflow)

   Two or three sentences citing something specific from the research, then a hypothesis about the problem that creates, then a soft ask. Saved for the rep to edit, never sent automatically.

6. **Write it onto the account** (builds workflow)

   The description, main product, current priorities, decision makers, competitors, fit score, reasoning, drafted opener and the time it ran, all onto the account record.

7. **Publish and check the picks** (builds workflow)

   The workflow is validated and published, with a daily digest of accounts researched and their average fit scores so managers can see what the AI is rating highly.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- The account_created event in your project

Writes:

- A new workflow, from step 1 "Start on a high value account"
- A new workflow, from step 2 "Read their website"
- A new workflow, from step 3 "Summarise what they do"
- A new workflow, from step 4 "Score them against your ICP"
- A new workflow, from step 5 "Draft the opening line"
- A new workflow, from step 6 "Write it onto the account"
- A new workflow, from step 7 "Publish and check the picks"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
