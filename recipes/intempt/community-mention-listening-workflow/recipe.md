---
id: community-mention-listening-workflow
title: Community mention listening
slash_command: /community-mention-listening-workflow
group: Workflows
owner: intempt
summary: Watches Reddit, forums and review sites for people shopping in your category or naming you, and
  hands the real ones to a human. It never auto replies.
description: >-
  Scrape relevant subreddits, forums, and review sites for trigger phrases ('looking for [category]',
  'alternative to [competitor]', 'anyone using [your product]') to AI classifies intent + sentiment to
  creates AE task for active-intent posts + logs brand mentions for marketing tracking. The Reddit-listening
  pattern.
version: 2.0.0
classification:
  product:
    - sales
    - marketing
  agent: workflow-builder
  mode:
    - b2b
    - saas
  complexity: advanced
  executionMode: live
  tags:
    - community-listening
    - intent-detection
    - brand-monitoring
prerequisites:
  integrations:
    - value: slack
      severity: recommended
touches:
  reads:
    - Your Slack connection
  writes:
    - A new workflow, from step 1 "Watch where buyers talk"
    - A new workflow, from step 2 "Check every 30 minutes"
    - A new workflow, from step 3 "Pull the new posts"
    - A new workflow, from step 4 "Keep only what matters"
    - A new workflow, from step 5 "Judge intent and fit"
    - A new workflow, from step 6 "Route by what it is"
    - A new workflow, from step 7 "Ask a human to reply"
    - A new workflow, from step 8 "Post the brand mentions"
    - A new workflow, from step 9 "Publish with no auto replies"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Watch where buyers talk
    summary: >-
      Monitors the subreddits, forums, review sites and social mentions you configure for phrases relevant
      to your category, so you catch someone in market at the moment they say so in public.
    builds: workflow
    description: >-
      Create a workflow 'Community mention listening' that monitors public discussion surfaces (configured
      subreddits, Hacker News, Indie Hackers, G2/Capterra reviews, X/Twitter mentions) for trigger phrases
      relevant to the product category. Goal: catch in-market intent at the moment it surfaces publicly,
      when speed-to-helpful-response converts.
  - id: s2
    title: Check every 30 minutes
    summary: >-
      Polls during business hours, tracking the last check per source so only new posts are processed.
    builds: workflow
    description: >-
      Configure scheduled trigger: poll every 30 minutes during business hours (cheap enough to be near-real-time,
      expensive enough to respect rate limits). Track last-checked-timestamp per source so only new posts
      are processed. Use the result of "Watch where buyers talk".
    dependsOn:
      - s1
  - id: s3
    title: Pull the new posts
    summary: >-
      Scrapes the configured sources, using RSS where it exists, and returns the posts and comments added
      since the last run with the author, time, text and source.
    builds: workflow
    description: >-
      Configure web scrape step for the configured list of community sources (subreddits like r/saas /
      r/CRM / r/marketing depending on workspace; specific forums; review sites). Use RSS where available
      (faster, lower-stakes scraping). Output: list of new posts/comments since last check, with author/timestamp/text/source.
      Use the result of "Watch where buyers talk", "Check every 30 minutes".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Keep only what matters
    summary: >-
      Posts are matched against your trigger phrases: shopping language such as looking for, recommend,
      alternative to a competitor or best tool for, plus any mention of your own name. Everything else,
      which is most of it, stops here.
    builds: workflow
    description: >-
      Configure branch step: scan posts for trigger phrases (configurable). Active-intent triggers: 'looking
      for', 'recommend', 'alternative to [competitor]', 'best tool for'. Brand-mention triggers: '[your
      product name]' (positive/negative/neutral). Skip posts matching neither (most of them). Continues
      only with matching posts. Use the result of "Watch where buyers talk", "Pull the new posts".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Judge intent and fit
    summary: >-
      Each matched post is classified by what it is: active shopping, a brand mention, a complaint or
      general chat, plus sentiment, urgency, and whether replying there would be welcome or would break
      that community's norms.
    builds: workflow
    description: >-
      Configure AI step that classifies each matched post: intent_type (active-shopping / brand-mention
      / complaint / general-discussion), sentiment (positive / neutral / negative), urgency (immediate
      / browsing / casual), and 'is this post a good place to respond authentically?' (avoid posts where
      commercial response would be off-topic / against community norms / clearly hostile). Output: classification
      + reasoning. Use the result of "Watch where buyers talk", "Keep only what matters".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Route by what it is
    summary: >-
      Active shopping where a reply would fit goes to an SDR or AE task. Brand mentions are logged for
      marketing, with a Slack alert if negative. A complaint naming you raises an urgent CX task. General
      chat is archived as trend data.
    builds: workflow
    description: >-
      Configure multi-split: ACTIVE-SHOPPING + good-response-fit to SDR/AE task with link to engage authentically
      (humans only: never auto-reply); BRAND-MENTION (any sentiment) to log to marketing dashboard, Slack
      alert if negative; COMPLAINT-MENTIONING-YOU to urgent CX task; GENERAL-DISCUSSION to archive (just
      data for trend tracking). Use the result of "Watch where buyers talk", "Judge intent and fit".
    dependsOn:
      - s1
      - s5
  - id: s7
    title: Ask a human to reply
    summary: >-
      The task carries the link, the full text, the classification and how to approach it: answer the
      question honestly first and mention the product only where it is genuinely relevant. Humans reply,
      never automation, because automated replies get banned fast.
    builds: workflow
    description: >-
      On active-shopping branch: create SDR/AE task with the post link, full text, AI classification,
      suggested response approach ('engage authentically with a helpful answer, then mention our product
      only if relevant (strict no-spam discipline'). Critical: tasks instruct humans to reply, not automation)
      automated community replies trigger spam-bans fast. Use the result of "Watch where buyers talk",
      "Route by what it is".
    dependsOn:
      - s1
      - s6
  - id: s8
    title: Post the brand mentions
    summary: >-
      Every mention goes to the community channel with its sentiment and a link, giving marketing and
      product a live read. Negative ones tag the CX lead.
    builds: workflow
    description: >-
      Configure Slack step on brand-mention branch: post to #community-mentions channel with the mention,
      sentiment, and link. Surfaces real-time brand-pulse for marketing + product. Special handling for
      negative mentions: tag CX lead. Use the result of "Watch where buyers talk", "Route by what it is".
    dependsOn:
      - s1
      - s6
  - id: s9
    title: Publish with no auto replies
    summary: >-
      Validated and published, tracking posts per source per week, how accurate the classification is
      on a human graded sample, and how many community conversations turn into meetings. The one hard
      rule is that nothing ever replies automatically.
    builds: workflow
    description: >-
      Validate and publish. Monitor: post-volume per source per week, intent-detection precision (sample
      human-rate the AI classifications), conversion from community-engagement-task to meeting (community-sourced
      leads typically convert higher when handled authentically). Critical guardrail: zero auto-replies:
      community trust requires humans. Use the result of "Watch where buyers talk", "Ask a human to reply",
      "Post the brand mentions".
    dependsOn:
      - s1
      - s7
      - s8
outputs:
  - key: workflow
    producedByStep: s1
    type: workflow
    description: Workflow produced by this recipe.
  - key: step
    producedByStep: s8
    type: step
    description: Workflow Step produced by this recipe.
---

<!-- generated from the frontmatter by scripts/rebuild_bodies.py; edit the frontmatter -->

# Community mention listening

Watches Reddit, forums and review sites for people shopping in your category or naming you, and hands the real ones to a human. It never auto replies.

## Steps

1. **Watch where buyers talk** (builds workflow)

   Monitors the subreddits, forums, review sites and social mentions you configure for phrases relevant to your category, so you catch someone in market at the moment they say so in public.

2. **Check every 30 minutes** (builds workflow)

   Polls during business hours, tracking the last check per source so only new posts are processed.

3. **Pull the new posts** (builds workflow)

   Scrapes the configured sources, using RSS where it exists, and returns the posts and comments added since the last run with the author, time, text and source.

4. **Keep only what matters** (builds workflow)

   Posts are matched against your trigger phrases: shopping language such as looking for, recommend, alternative to a competitor or best tool for, plus any mention of your own name. Everything else, which is most of it, stops here.

5. **Judge intent and fit** (builds workflow)

   Each matched post is classified by what it is: active shopping, a brand mention, a complaint or general chat, plus sentiment, urgency, and whether replying there would be welcome or would break that community's norms.

6. **Route by what it is** (builds workflow)

   Active shopping where a reply would fit goes to an SDR or AE task. Brand mentions are logged for marketing, with a Slack alert if negative. A complaint naming you raises an urgent CX task. General chat is archived as trend data.

7. **Ask a human to reply** (builds workflow)

   The task carries the link, the full text, the classification and how to approach it: answer the question honestly first and mention the product only where it is genuinely relevant. Humans reply, never automation, because automated replies get banned fast.

8. **Post the brand mentions** (builds workflow)

   Every mention goes to the community channel with its sentiment and a link, giving marketing and product a live read. Negative ones tag the CX lead.

9. **Publish with no auto replies** (builds workflow)

   Validated and published, tracking posts per source per week, how accurate the classification is on a human graded sample, and how many community conversations turn into meetings. The one hard rule is that nothing ever replies automatically.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- Your Slack connection

Writes:

- A new workflow, from step 1 "Watch where buyers talk"
- A new workflow, from step 2 "Check every 30 minutes"
- A new workflow, from step 3 "Pull the new posts"
- A new workflow, from step 4 "Keep only what matters"
- A new workflow, from step 5 "Judge intent and fit"
- A new workflow, from step 6 "Route by what it is"
- A new workflow, from step 7 "Ask a human to reply"
- A new workflow, from step 8 "Post the brand mentions"
- A new workflow, from step 9 "Publish with no auto replies"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
