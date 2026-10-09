---
name: ai-account-research-deep-dive
description: Use when a user mentions "AI account research deep dive", "account research agent", "company research workflow", or asks for related help. AI agent autonomously researches a target account (scrapes website, summarizes news, extracts decision-makers, scores ICP fit, drafts an opening hypothesis) and populates the Account record. The Claygent-style deep-research workflow that turns 30 minutes of SDR research into 2 minutes of AI work.
arguments: []
intempt:
  id: ai-account-research-deep-dive
  title: "AI account research"
  version: 1.0.0
  slashCommand: /ai-account-research-deep-dive
  group: Workflows
  shortDescription: "Reads a target account's website, pulls out the decision makers, scores the fit against your ICP, and drafts an opener for the rep to edit."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [ai-research, account-intelligence, sdr-productivity]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: account_created, severity: blocking }
  invokesCommands:
    - create_workflow
    - configure_web_scrape_step
    - configure_ai_research_step
    - configure_write_with_ai_step
    - configure_update_attribute_step
    - publish_workflow
  procedure:
    - step: 1
      title: "Start on a high value account"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Runs when a high tier account is created, or on demand against a list of accounts. The job is a brief a rep can act on without doing any research of their own."
      prompt: 'Create a workflow ''AI account deep research'' triggered by Account created (high-tier accounts only: by ICP fit or domain-tier flag) OR manual trigger from a list view (''research these 50 accounts''). Goal: produce a structured account-intelligence brief that a rep can act on without doing their own research.'
    - step: 2
      title: "Read their website"
      command: configure_web_scrape_step
      produces: step
      bindsAs: scrape
      dependsOn:
      - workflow
      description: "Fetches the homepage, the about page, the leadership page, pricing if there is one, the customers page and recent blog posts. It honours robots.txt and rate limits per domain."
      prompt: 'Configure web scrape step targeting the account''s domain. Fetch: homepage hero copy, About page, Team/Leadership page, Pricing page (if exists), Customers page, recent blog posts. Returns raw page content to feed into the AI summarization step. Respect robots.txt; rate-limit per domain.'
    - step: 3
      title: "Summarise what they do"
      command: configure_ai_research_step
      produces: step
      bindsAs: summarize
      dependsOn:
      - workflow
      - scrape
      description: "From those pages: a one sentence description, the main product, who they sell to, what they are pushing on right now, the leadership names and titles, any competitors or partners mentioned, and a confidence score on each finding."
      prompt: 'Configure AI research step that takes the scraped content and produces a structured summary: (a) one-sentence company description, (b) primary product/service, (c) ICP signals (target market, stated customer types), (d) recent priorities inferred from homepage / blog (e.g. ''expanding internationally'', ''launching AI features''), (e) decision-maker names + titles from leadership page, (f) any mentioned competitors / partners, (g) confidence score on each finding.'
    - step: 4
      title: "Score them against your ICP"
      command: configure_ai_research_step
      produces: step
      bindsAs: icp_score
      dependsOn:
      - workflow
      - summarize
      description: "A 0 to 100 fit score built from that summary against your ICP definition of industry, size, technology and use case, with a written reason for the number."
      prompt: 'Configure a second AI step that scores ICP fit using the company summary + a provided ICP definition (industry, size, tech, use cases). Output: numeric 0-100 score + reasoning string (''Strong fit because they are a B2B SaaS in [target industry] with ~50 employees and recently raised Series A: matches our ICP for growth-stage teams''). Records a structured fit score and fit reasoning attribute.'
    - step: 5
      title: "Draft the opening line"
      command: configure_write_with_ai_step
      produces: step
      bindsAs: draft_opening
      dependsOn:
      - workflow
      - summarize
      - icp_score
      description: "Two or three sentences citing something specific from the research, then a hypothesis about the problem that creates, then a soft ask. Saved for the rep to edit, never sent automatically."
      prompt: 'Configure AI write step that produces a draft outreach opener referencing specific findings (not generic). Format: 2-3 sentences referencing a SPECIFIC fact from the research (''I saw your team is expanding into APAC...''), then a value-hypothesis (''Teams growing internationally typically struggle with X: that''s where we help''), then a soft CTA. Output stored on the account for SDR review-and-edit, never auto-sent.'
    - step: 6
      title: "Write it onto the account"
      command: configure_update_attribute_step
      produces: step
      bindsAs: update_account
      dependsOn:
      - workflow
      - summarize
      - icp_score
      - draft_opening
      description: "The description, main product, current priorities, decision makers, competitors, fit score, reasoning, drafted opener and the time it ran, all onto the account record."
      prompt: 'Write back to the account record: company description, primary product, recent priorities, inferred decision makers (array), competitors mentioned, fit score, fit reasoning, AI-drafted opening, and research completed date. The SDR sees a fully-formed account brief without doing any manual research.'
    - step: 7
      title: "Publish and check the picks"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - update_account
      description: "The workflow is validated and published, with a daily digest of accounts researched and their average fit scores so managers can see what the AI is rating highly."
      prompt: Validate workflow DAG and publish. Add a daily summary digest of new accounts researched + their average fit scores so SDR managers can audit which accounts AI is flagging as best-fit.
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# AI account research

Reads a target account's website, pulls out the decision makers, scores the fit against your ICP, and drafts an opener for the rep to edit.

## Before you run it

- Send the `account_created` event

## What it does

1. **Start on a high value account** (`create_workflow`)

   Runs when a high tier account is created, or on demand against a list of accounts. The job is a brief a rep can act on without doing any research of their own.

2. **Read their website** (`configure_web_scrape_step`)

   Fetches the homepage, the about page, the leadership page, pricing if there is one, the customers page and recent blog posts. It honours robots.txt and rate limits per domain.

3. **Summarise what they do** (`configure_ai_research_step`)

   From those pages: a one sentence description, the main product, who they sell to, what they are pushing on right now, the leadership names and titles, any competitors or partners mentioned, and a confidence score on each finding.

4. **Score them against your ICP** (`configure_ai_research_step`)

   A 0 to 100 fit score built from that summary against your ICP definition of industry, size, technology and use case, with a written reason for the number.

5. **Draft the opening line** (`configure_write_with_ai_step`)

   Two or three sentences citing something specific from the research, then a hypothesis about the problem that creates, then a soft ask. Saved for the rep to edit, never sent automatically.

6. **Write it onto the account** (`configure_update_attribute_step`)

   The description, main product, current priorities, decision makers, competitors, fit score, reasoning, drafted opener and the time it ran, all onto the account record.

7. **Publish and check the picks** (`publish_workflow`)

   The workflow is validated and published, with a daily digest of accounts researched and their average fit scores so managers can see what the AI is rating highly.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
