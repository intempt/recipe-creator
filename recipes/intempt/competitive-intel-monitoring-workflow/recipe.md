---
frontmatter_id: competitive-intel-monitoring-workflow
slash_command: /competitive-intel-monitoring-workflow
description: Weekly scheduled AI agent scrapes competitor websites, review sites, social, and news, then posts a summarized competitive intel briefing to Slack.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
visibility: draft
rejected: It depends wholly on a research agent scraping competitor websites, review sites and news; Blu does not build research
  agents.
portable:
  summary: Every Monday morning an AI agent scrapes competitor sites, reviews, social and news, then posts a structured competitive
    intel briefing to Slack.
  parameters:
  - name: run_time
    type: string
    label: Weekly run time (local)
    default: 07:00
    required: false
  - name: run_day
    type: enum
    label: Weekly run day
    default: monday
    required: false
    options:
    - monday
    - tuesday
    - wednesday
    - thursday
    - friday
  - name: rate_limit_delay
    type: duration
    label: Delay between competitor iterations
    default: 10 s
    required: false
  - name: scrape_window
    type: duration
    label: Blog and news lookback window
    default: 7 d
    required: false
  - name: tag_leads_for_major_moves
    type: boolean
    label: Tag product and marketing leads for major moves
    default: true
    required: false
  - name: workflow_name
    type: string
    label: Workflow name
    default: Weekly competitive intel
    required: false
  requirements:
  - slot: competitor_list
    kind: knowledge
    meaning: A configured list of competitor domains (typically 3-7) for this workspace
  - slot: competitor_intel_channel
    kind: integration
    meaning: A Slack channel for competitive intel briefings, such as a competitive-intel channel
    channel: slack
  - slot: product_and_marketing_leads
    kind: segment
    meaning: The product and marketing leads who should be tagged for major competitive moves
    optional: true
  - slot: competitor_snapshot_history
    kind: knowledge
    meaning: Stored weekly snapshots of competitor public pages from prior runs, used for week-over-week comparison
  steps:
  - id: s1
    builds: automation
    uses:
    - workflow_name
    - run_day
    - run_time
    instruction: Create a workflow named "{workflow_name}" scheduled to run every {run_day} at {run_time} local time. Its
      goal is to replace the manual weekly check of competitor activity with a structured AI-generated briefing that product
      and sales teams can read in about 3 minutes.
  - id: s2
    builds: automation
    uses:
    - s1
    - competitor_list
    - run_day
    - run_time
    dependsOn:
    - s1
    instruction: Configure the scheduled trigger to run every {run_day} at {run_time} local time. Skip the run if the workspace
      is paused or if no competitors are configured in {competitor_list}. Store a last-run timestamp so each weekly scrape
      fetches only content published since the prior run.
  - id: s3
    builds: automation
    uses:
    - s1
    - s2
    - competitor_list
    - rate_limit_delay
    dependsOn:
    - s1
    instruction: Configure a loop that iterates over each competitor domain in {competitor_list}. For each competitor, run
      the scrape and analysis steps that follow. Wait {rate_limit_delay} between iterations to be polite to sources.
  - id: s4
    builds: automation
    uses:
    - s1
    - s3
    - scrape_window
    dependsOn:
    - s1
    instruction: 'For each competitor, scrape these public sources: pricing page, product and features pages, blog posts from
      the last {scrape_window}, changelog or release notes page, careers page (hiring signals), review-site summary from G2
      and Capterra, and recent press releases. Respect robots.txt. Cache content and skip re-fetching pages that have not
      changed since the last run.'
  - id: s5
    builds: automation
    uses:
    - s1
    - s4
    - competitor_snapshot_history
    dependsOn:
    - s1
    instruction: 'Use an AI research step to compare this week''s scraped content for each competitor against the last stored
      snapshot in {competitor_snapshot_history} and flag material changes. Material changes are: pricing changes, newly announced
      features, leadership changes found on careers or about pages, large customer wins from press releases, sentiment shifts
      on review sites, and hiring trends suggesting expansion in a product area. For each competitor, output a structured
      briefing with three parts: what changed, what did not change, and what to watch.'
  - id: s6
    builds: automation
    uses:
    - s1
    - s5
    dependsOn:
    - s1
    instruction: 'Use an AI writing step to consolidate the per-competitor findings from "Compare against last week" into
      one weekly briefing with these sections: (a) top 3 most material competitive moves this week, (b) per-competitor highlights,
      (c) watch-list for next week covering developing stories, and (d) recommended responses, for example: a competitor launched
      a feature, our differentiator is still X, and product marketing may want to update positioning. Use a factual, concise,
      scannable tone.'
  - id: s7
    builds: automation
    uses:
    - s1
    - s6
    - competitor_intel_channel
    - product_and_marketing_leads
    - tag_leads_for_major_moves
    dependsOn:
    - s1
    instruction: Post the briefing from "Write the briefing" to {competitor_intel_channel} using a rich block layout with
      sections and links to each source page. Open a thread under the post for team discussion. If {tag_leads_for_major_moves}
      is true, tag {product_and_marketing_leads} on any major move.
  - id: s8
    builds: automation
    uses:
    - s1
    - s7
    dependsOn:
    - s1
    instruction: 'Validate the workflow and publish it. Monitor three things: weekly briefing delivery, which must not fail
      silently; team engagement, measured by reactions and thread replies; and accuracy, through an occasional human spot-check
      that the AI correctly identified material changes.'
---

# Weekly competitive intel briefing

Slash command: /competitive-intel-monitoring-workflow

## Step 1: Replace the Monday check

Create a workflow named "Weekly competitive intel" scheduled to run every monday at 07:00 local time. Its goal is to replace the manual weekly check of competitor activity with a structured AI-generated briefing that product and sales teams can read in about 3 minutes.

## Step 2: Run it Monday at 7am

Configure the scheduled trigger to run every monday at 07:00 local time. Skip the run if the workspace is paused or if no competitors are configured in competitor list. Store a last-run timestamp so each weekly scrape fetches only content published since the prior run.

## Step 3: Go through each competitor

Configure a loop that iterates over each competitor domain in competitor list. For each competitor, run the scrape and analysis steps that follow. Wait 10 s between iterations to be polite to sources.

## Step 4: Read their public pages

For each competitor, scrape these public sources: pricing page, product and features pages, blog posts from the last 7 d, changelog or release notes page, careers page (hiring signals), review-site summary from G2 and Capterra, and recent press releases. Respect robots.txt. Cache content and skip re-fetching pages that have not changed since the last run.

## Step 5: Compare against last week

Use an AI research step to compare this week's scraped content for each competitor against the last stored snapshot in competitor snapshot history and flag material changes. Material changes are: pricing changes, newly announced features, leadership changes found on careers or about pages, large customer wins from press releases, sentiment shifts on review sites, and hiring trends suggesting expansion in a product area. For each competitor, output a structured briefing with three parts: what changed, what did not change, and what to watch.

## Step 6: Write the briefing

Use an AI writing step to consolidate the per-competitor findings from "Compare against last week" into one weekly briefing with these sections: (a) top 3 most material competitive moves this week, (b) per-competitor highlights, (c) watch-list for next week covering developing stories, and (d) recommended responses, for example: a competitor launched a feature, our differentiator is still X, and product marketing may want to update positioning. Use a factual, concise, scannable tone.

## Step 7: Post it to the channel

Post the briefing from "Write the briefing" to competitor intel channel using a rich block layout with sections and links to each source page. Open a thread under the post for team discussion. If True is true, tag product and marketing leads on any major move.

## Step 8: Publish and spot check it

Validate the workflow and publish it. Monitor three things: weekly briefing delivery, which must not fail silently; team engagement, measured by reactions and thread replies; and accuracy, through an occasional human spot-check that the AI correctly identified material changes.
