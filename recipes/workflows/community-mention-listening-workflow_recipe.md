---
name: community-mention-listening-workflow
description: Use when a user mentions "community mention listening", "reddit listening workflow", "brand mention monitoring", or asks for related help. Scrape relevant subreddits, forums, and review sites for trigger phrases ('looking for [category]', 'alternative to [competitor]', 'anyone using [your product]') to AI classifies intent + sentiment to creates AE task for active-intent posts + logs brand mentions for marketing tracking. The Reddit-listening pattern.
arguments: []
intempt:
  id: community-mention-listening-workflow
  title: "Community mention listening"
  version: 1.0.0
  slashCommand: /community-mention-listening-workflow
  group: Workflows
  shortDescription: "Watches Reddit, forums and review sites for people shopping in your category or naming you, and hands the real ones to a human. It never auto replies."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales, marketing]
    agent: workflow-builder
    mode: [b2b, saas]
    complexity: advanced
    executionMode: live
    tags: [community-listening, intent-detection, brand-monitoring]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    integrations:
      - { value: slack, severity: recommended }
  invokesCommands:
    - create_workflow
    - configure_workflow_wait_until_step
    - configure_web_scrape_step
    - configure_workflow_branch_step
    - configure_ai_research_step
    - configure_workflow_multi_split_step
    - configure_create_task_step
    - configure_slack_step
    - publish_workflow
  procedure:
    - step: 1
      title: "Watch where buyers talk"
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: "Monitors the subreddits, forums, review sites and social mentions you configure for phrases relevant to your category, so you catch someone in market at the moment they say so in public."
      prompt: 'Create a workflow ''Community mention listening'' that monitors public discussion surfaces (configured subreddits, Hacker News, Indie Hackers, G2/Capterra reviews, X/Twitter mentions) for trigger phrases relevant to the product category. Goal: catch in-market intent at the moment it surfaces publicly, when speed-to-helpful-response converts.'
    - step: 2
      title: "Check every 30 minutes"
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: "Polls during business hours, tracking the last check per source so only new posts are processed."
      prompt: 'Configure scheduled trigger: poll every 30 minutes during business hours (cheap enough to be near-real-time, expensive enough to respect rate limits). Track last-checked-timestamp per source so only new posts are processed.'
    - step: 3
      title: "Pull the new posts"
      command: configure_web_scrape_step
      produces: step
      bindsAs: scrape
      dependsOn:
      - workflow
      - schedule
      description: "Scrapes the configured sources, using RSS where it exists, and returns the posts and comments added since the last run with the author, time, text and source."
      prompt: 'Configure web scrape step for the configured list of community sources (subreddits like r/saas / r/CRM / r/marketing depending on workspace; specific forums; review sites). Use RSS where available (faster, lower-stakes scraping). Output: list of new posts/comments since last check, with author/timestamp/text/source.'
    - step: 4
      title: "Keep only what matters"
      command: configure_workflow_branch_step
      produces: step
      bindsAs: filter
      dependsOn:
      - workflow
      - scrape
      description: "Posts are matched against your trigger phrases: shopping language such as looking for, recommend, alternative to a competitor or best tool for, plus any mention of your own name. Everything else, which is most of it, stops here."
      prompt: 'Configure branch step: scan posts for trigger phrases (configurable). Active-intent triggers: ''looking for'', ''recommend'', ''alternative to [competitor]'', ''best tool for''. Brand-mention triggers: ''[your product name]'' (positive/negative/neutral). Skip posts matching neither (most of them). Continues only with matching posts.'
    - step: 5
      title: "Judge intent and fit"
      command: configure_ai_research_step
      produces: step
      bindsAs: classify
      dependsOn:
      - workflow
      - filter
      description: "Each matched post is classified by what it is: active shopping, a brand mention, a complaint or general chat, plus sentiment, urgency, and whether replying there would be welcome or would break that community's norms."
      prompt: 'Configure AI step that classifies each matched post: intent_type (active-shopping / brand-mention / complaint / general-discussion), sentiment (positive / neutral / negative), urgency (immediate / browsing / casual), and ''is this post a good place to respond authentically?'' (avoid posts where commercial response would be off-topic / against community norms / clearly hostile). Output: classification + reasoning.'
    - step: 6
      title: "Route by what it is"
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: split
      dependsOn:
      - workflow
      - classify
      description: "Active shopping where a reply would fit goes to an SDR or AE task. Brand mentions are logged for marketing, with a Slack alert if negative. A complaint naming you raises an urgent CX task. General chat is archived as trend data."
      prompt: 'Configure multi-split: ACTIVE-SHOPPING + good-response-fit to SDR/AE task with link to engage authentically (humans only: never auto-reply); BRAND-MENTION (any sentiment) to log to marketing dashboard, Slack alert if negative; COMPLAINT-MENTIONING-YOU to urgent CX task; GENERAL-DISCUSSION to archive (just data for trend tracking).'
    - step: 7
      title: "Ask a human to reply"
      command: configure_create_task_step
      produces: step
      bindsAs: task
      dependsOn:
      - workflow
      - split
      description: "The task carries the link, the full text, the classification and how to approach it: answer the question honestly first and mention the product only where it is genuinely relevant. Humans reply, never automation, because automated replies get banned fast."
      prompt: 'On active-shopping branch: create SDR/AE task with the post link, full text, AI classification, suggested response approach (''engage authentically with a helpful answer, then mention our product only if relevant (strict no-spam discipline''). Critical: tasks instruct humans to reply, not automation) automated community replies trigger spam-bans fast.'
    - step: 8
      title: "Post the brand mentions"
      command: configure_slack_step
      produces: step
      bindsAs: slack
      dependsOn:
      - workflow
      - split
      description: "Every mention goes to the community channel with its sentiment and a link, giving marketing and product a live read. Negative ones tag the CX lead."
      prompt: 'Configure Slack step on brand-mention branch: post to #community-mentions channel with the mention, sentiment, and link. Surfaces real-time brand-pulse for marketing + product. Special handling for negative mentions: tag CX lead.'
    - step: 9
      title: "Publish with no auto replies"
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - task
      - slack
      description: "Validated and published, tracking posts per source per week, how accurate the classification is on a human graded sample, and how many community conversations turn into meetings. The one hard rule is that nothing ever replies automatically."
      prompt: 'Validate and publish. Monitor: post-volume per source per week, intent-detection precision (sample human-rate the AI classifications), conversion from community-engagement-task to meeting (community-sourced leads typically convert higher when handled authentically). Critical guardrail: zero auto-replies: community trust requires humans.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---
<!-- generated from the frontmatter by scripts/rebuild_bodies.py -->

# Community mention listening

Watches Reddit, forums and review sites for people shopping in your category or naming you, and hands the real ones to a human. It never auto replies.

## Before you run it

- Connect slack

## What it does

1. **Watch where buyers talk** (`create_workflow`)

   Monitors the subreddits, forums, review sites and social mentions you configure for phrases relevant to your category, so you catch someone in market at the moment they say so in public.

2. **Check every 30 minutes** (`configure_workflow_wait_until_step`)

   Polls during business hours, tracking the last check per source so only new posts are processed.

3. **Pull the new posts** (`configure_web_scrape_step`)

   Scrapes the configured sources, using RSS where it exists, and returns the posts and comments added since the last run with the author, time, text and source.

4. **Keep only what matters** (`configure_workflow_branch_step`)

   Posts are matched against your trigger phrases: shopping language such as looking for, recommend, alternative to a competitor or best tool for, plus any mention of your own name. Everything else, which is most of it, stops here.

5. **Judge intent and fit** (`configure_ai_research_step`)

   Each matched post is classified by what it is: active shopping, a brand mention, a complaint or general chat, plus sentiment, urgency, and whether replying there would be welcome or would break that community's norms.

6. **Route by what it is** (`configure_workflow_multi_split_step`)

   Active shopping where a reply would fit goes to an SDR or AE task. Brand mentions are logged for marketing, with a Slack alert if negative. A complaint naming you raises an urgent CX task. General chat is archived as trend data.

7. **Ask a human to reply** (`configure_create_task_step`)

   The task carries the link, the full text, the classification and how to approach it: answer the question honestly first and mention the product only where it is genuinely relevant. Humans reply, never automation, because automated replies get banned fast.

8. **Post the brand mentions** (`configure_slack_step`)

   Every mention goes to the community channel with its sentiment and a link, giving marketing and product a live read. Negative ones tag the CX lead.

9. **Publish with no auto replies** (`publish_workflow`)

   Validated and published, tracking posts per source per week, how accurate the classification is on a human graded sample, and how many community conversations turn into meetings. The one hard rule is that nothing ever replies automatically.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.
