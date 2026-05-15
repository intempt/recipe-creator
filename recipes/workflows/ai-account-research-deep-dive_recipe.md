---
name: ai-account-research-deep-dive
description: Use when a user mentions "AI account research deep dive", "account research agent", "company research workflow", or asks for related help. AI agent autonomously researches a target account — scrapes website, summarizes news, extracts decision-makers, scores ICP fit, drafts an opening hypothesis — and populates the Account record. The Claygent-style deep-research workflow that turns 30 minutes of SDR research into 2 minutes of AI work.
arguments: []
intempt:
  id: ai-account-research-deep-dive
  version: 1.0.0
  slashCommand: /ai-account-research-deep-dive
  group: Workflows
  shortDescription: "AI agent autonomously researches a target account — scrapes website, summarizes news, extracts decision-makers, scores ICP fit, drafts an opening hypothesis — and populates the Account record. The Claygent-style deep-research workflow that turns 30 minutes of SDR research into 2 minutes of AI work."
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
      title: Build the AI Research Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''AI account deep research'' triggered by account_created (high-tier accounts only — by ICP fit or domain-tier flag) OR manual trigger from a list view (''research these 50 accounts''). Goal: produce a structured account-intelligence brief that a rep can act on without doing their own research.'
      prompt: 'Create a workflow ''AI account deep research'' triggered by account_created (high-tier accounts only — by ICP fit or domain-tier flag) OR manual trigger from a list view (''research these 50 accounts''). Goal: produce a structured account-intelligence brief that a rep can act on without doing their own research.'
    - step: 2
      title: Scrape Company Website
      command: configure_web_scrape_step
      produces: step
      bindsAs: scrape
      dependsOn:
      - workflow
      description: 'Configure web scrape step targeting the account''s domain. Fetch: homepage hero copy, About page, Team/Leadership page, Pricing page (if exists), Customers page, recent blog posts. Returns raw page content to feed into the AI summarization step. Respect robots.txt; rate-limit per domain.'
      prompt: 'Configure web scrape step targeting the account''s domain. Fetch: homepage hero copy, About page, Team/Leadership page, Pricing page (if exists), Customers page, recent blog posts. Returns raw page content to feed into the AI summarization step. Respect robots.txt; rate-limit per domain.'
    - step: 3
      title: AI-Summarize What the Company Does
      command: configure_ai_research_step
      produces: step
      bindsAs: summarize
      dependsOn:
      - workflow
      - scrape
      description: 'Configure AI research step that takes the scraped content and produces a structured summary: (a) one-sentence company description, (b) primary product/service, (c) ICP signals (target market, stated customer types), (d) recent priorities inferred from homepage / blog (e.g. ''expanding internationally'', ''launching AI features''), (e) decision-maker names + titles from leadership page, (f) any mentioned competitors / partners, (g) confidence score on each finding.'
      prompt: 'Configure AI research step that takes the scraped content and produces a structured summary: (a) one-sentence company description, (b) primary product/service, (c) ICP signals (target market, stated customer types), (d) recent priorities inferred from homepage / blog (e.g. ''expanding internationally'', ''launching AI features''), (e) decision-maker names + titles from leadership page, (f) any mentioned competitors / partners, (g) confidence score on each finding.'
    - step: 4
      title: Score ICP Fit
      command: configure_ai_research_step
      produces: step
      bindsAs: icp_score
      dependsOn:
      - workflow
      - summarize
      description: 'Configure a second AI step that scores ICP fit using the company summary + a provided ICP definition (industry, size, tech, use cases). Output: numeric 0-100 score + reasoning string (''Strong fit because they are a B2B SaaS in [target industry] with ~50 employees and recently raised Series A — matches our ICP for growth-stage teams''). Records a structured fit_score + fit_reasoning attribute.'
      prompt: 'Configure a second AI step that scores ICP fit using the company summary + a provided ICP definition (industry, size, tech, use cases). Output: numeric 0-100 score + reasoning string (''Strong fit because they are a B2B SaaS in [target industry] with ~50 employees and recently raised Series A — matches our ICP for growth-stage teams''). Records a structured fit_score + fit_reasoning attribute.'
    - step: 5
      title: AI-Draft Opening Hypothesis
      command: configure_write_with_ai_step
      produces: step
      bindsAs: draft_opening
      dependsOn:
      - workflow
      - summarize
      - icp_score
      description: 'Configure AI write step that produces a draft outreach opener referencing specific findings (not generic). Format: 2-3 sentences referencing a SPECIFIC fact from the research (''I saw your team is expanding into APAC...''), then a value-hypothesis (''Teams growing internationally typically struggle with X — that''s where we help''), then a soft CTA. Output stored on the account for SDR review-and-edit, never auto-sent.'
      prompt: 'Configure AI write step that produces a draft outreach opener referencing specific findings (not generic). Format: 2-3 sentences referencing a SPECIFIC fact from the research (''I saw your team is expanding into APAC...''), then a value-hypothesis (''Teams growing internationally typically struggle with X — that''s where we help''), then a soft CTA. Output stored on the account for SDR review-and-edit, never auto-sent.'
    - step: 6
      title: Update Account with Research Brief
      command: configure_update_attribute_step
      produces: step
      bindsAs: update_account
      dependsOn:
      - workflow
      - summarize
      - icp_score
      - draft_opening
      description: 'Write back to the Account record: company_description, primary_product, recent_priorities, decision_makers_inferred (array), competitors_mentioned, fit_score, fit_reasoning, ai_drafted_opening, research_completed_at. The SDR sees a fully-formed account brief without doing any manual research.'
      prompt: 'Write back to the Account record: company_description, primary_product, recent_priorities, decision_makers_inferred (array), competitors_mentioned, fit_score, fit_reasoning, ai_drafted_opening, research_completed_at. The SDR sees a fully-formed account brief without doing any manual research.'
    - step: 7
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - update_account
      description: Validate workflow DAG and publish. Add a daily summary digest of new accounts researched + their average fit scores so SDR managers can audit which accounts AI is flagging as best-fit.
      prompt: Validate workflow DAG and publish. Add a daily summary digest of new accounts researched + their average fit scores so SDR managers can audit which accounts AI is flagging as best-fit.
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Ai Account Research Deep Dive

## Procedure

1. **Build the AI Research Workflow** [`create_workflow`] — Create a workflow 'AI account deep research' triggered by account_created (high-tier accounts only — by ICP fit or domain-tier flag) OR manual trigger from a list view ('research these 50 accounts'). Goal: produce a structured account-intelligence brief that a rep can act on without doing their own research. → produces: workflow
2. **Scrape Company Website** [`configure_web_scrape_step`] — Configure web scrape step targeting the account's domain. Fetch: homepage hero copy, About page, Team/Leadership page, Pricing page (if exists), Customers page, recent blog posts. Returns raw page content to feed into the AI summarization step. Respect robots.txt; rate-limit per domain. → produces: step
3. **AI-Summarize What the Company Does** [`configure_ai_research_step`] — Configure AI research step that takes the scraped content and produces a structured summary: (a) one-sentence company description, (b) primary product/service, (c) ICP signals (target market, stated customer types), (d) recent priorities inferred from homepage / blog (e.g. 'expanding internationally', 'launching AI features'), (e) decision-maker names + titles from leadership page, (f) any mentioned competitors / partners, (g) confidence score on each finding. → produces: step
4. **Score ICP Fit** [`configure_ai_research_step`] — Configure a second AI step that scores ICP fit using the company summary + a provided ICP definition (industry, size, tech, use cases). Output: numeric 0-100 score + reasoning string ('Strong fit because they are a B2B SaaS in [target industry] with ~50 employees and recently raised Series A — matches our ICP for growth-stage teams'). Records a structured fit_score + fit_reasoning attribute. → produces: step
5. **AI-Draft Opening Hypothesis** [`configure_write_with_ai_step`] — Configure AI write step that produces a draft outreach opener referencing specific findings (not generic). Format: 2-3 sentences referencing a SPECIFIC fact from the research ('I saw your team is expanding into APAC...'), then a value-hypothesis ('Teams growing internationally typically struggle with X — that's where we help'), then a soft CTA. Output stored on the account for SDR review-and-edit, never auto-sent. → produces: step
6. **Update Account with Research Brief** [`configure_update_attribute_step`] — Write back to the Account record: company_description, primary_product, recent_priorities, decision_makers_inferred (array), competitors_mentioned, fit_score, fit_reasoning, ai_drafted_opening, research_completed_at. The SDR sees a fully-formed account brief without doing any manual research. → produces: step
7. **Validate and Publish** [`publish_workflow`] — Validate workflow DAG and publish. Add a daily summary digest of new accounts researched + their average fit scores so SDR managers can audit which accounts AI is flagging as best-fit. → produces: workflow
