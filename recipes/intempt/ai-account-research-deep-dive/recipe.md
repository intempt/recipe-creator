---
description: Reads a target account's website, pulls out the decision makers, scores the fit against your ICP, and drafts an opener for the rep to edit.
author:
  first_name: Trishik
  last_name: Shrestha
  job_title: Growth Marketer
  avatar: https://cdn.intempt.com/assets/author-profile-pics/trishik.png
  company: Intempt
  org_name: intempt
classification:
  industry:
  - ai
  - b2b-saas
  - ecommerce
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
