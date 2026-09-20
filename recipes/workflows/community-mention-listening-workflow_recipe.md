---
name: community-mention-listening-workflow
description: Use when a user mentions "community mention listening", "reddit listening workflow", "brand mention monitoring", or asks for related help. Scrape relevant subreddits, forums, and review sites for trigger phrases ('looking for [category]', 'alternative to [competitor]', 'anyone using [your product]') → AI classifies intent + sentiment → creates AE task for active-intent posts + logs brand mentions for marketing tracking. The Reddit-listening pattern.
arguments: []
intempt:
  id: community-mention-listening-workflow
  version: 1.0.0
  slashCommand: /community-mention-listening-workflow
  group: Workflows
  shortDescription: 'Scrape relevant subreddits, forums, and review sites for trigger phrases (''looking for [category]'', ''alternative to [competitor]'', ''anyone using [your product]'') to AI classifies intent + sentiment to creates AE task for active-intent posts + logs brand mentions for marketing tracking. The Reddit-listening pattern.'
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
      title: Build the Listening Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Community mention listening'' that monitors public discussion surfaces (configured subreddits, Hacker News, Indie Hackers, G2/Capterra reviews, X/Twitter mentions) for trigger phrases relevant to the product category. Goal: catch in-market intent at the moment it surfaces publicly, when speed-to-helpful-response converts.'
      prompt: 'Create a workflow ''Community mention listening'' that monitors public discussion surfaces (configured subreddits, Hacker News, Indie Hackers, G2/Capterra reviews, X/Twitter mentions) for trigger phrases relevant to the product category. Goal: catch in-market intent at the moment it surfaces publicly, when speed-to-helpful-response converts.'
    - step: 2
      title: Scheduled Polling Trigger
      command: configure_workflow_wait_until_step
      produces: step
      bindsAs: schedule
      dependsOn:
      - workflow
      description: 'Configure scheduled trigger: poll every 30 minutes during business hours (cheap enough to be near-real-time, expensive enough to respect rate limits). Track last-checked-timestamp per source so only new posts are processed.'
      prompt: 'Configure scheduled trigger: poll every 30 minutes during business hours (cheap enough to be near-real-time, expensive enough to respect rate limits). Track last-checked-timestamp per source so only new posts are processed.'
    - step: 3
      title: Scrape Configured Sources
      command: configure_web_scrape_step
      produces: step
      bindsAs: scrape
      dependsOn:
      - workflow
      - schedule
      description: 'Configure web scrape step for the configured list of community sources (subreddits like r/saas / r/CRM / r/marketing depending on workspace; specific forums; review sites). Use RSS where available (faster, lower-stakes scraping). Output: list of new posts/comments since last check, with author/timestamp/text/source.'
      prompt: 'Configure web scrape step for the configured list of community sources (subreddits like r/saas / r/CRM / r/marketing depending on workspace; specific forums; review sites). Use RSS where available (faster, lower-stakes scraping). Output: list of new posts/comments since last check, with author/timestamp/text/source.'
    - step: 4
      title: Filter by Trigger Phrases
      command: configure_workflow_branch_step
      produces: step
      bindsAs: filter
      dependsOn:
      - workflow
      - scrape
      description: 'Configure branch step: scan posts for trigger phrases (configurable). Active-intent triggers: ''looking for'', ''recommend'', ''alternative to [competitor]'', ''best tool for''. Brand-mention triggers: ''[your product name]'' (positive/negative/neutral). Skip posts matching neither (most of them). Continues only with matching posts.'
      prompt: 'Configure branch step: scan posts for trigger phrases (configurable). Active-intent triggers: ''looking for'', ''recommend'', ''alternative to [competitor]'', ''best tool for''. Brand-mention triggers: ''[your product name]'' (positive/negative/neutral). Skip posts matching neither (most of them). Continues only with matching posts.'
    - step: 5
      title: AI Classify Intent and Sentiment
      command: configure_ai_research_step
      produces: step
      bindsAs: classify
      dependsOn:
      - workflow
      - filter
      description: 'Configure AI step that classifies each matched post: intent_type (active-shopping / brand-mention / complaint / general-discussion), sentiment (positive / neutral / negative), urgency (immediate / browsing / casual), and ''is this post a good place to respond authentically?'' (avoid posts where commercial response would be off-topic / against community norms / clearly hostile). Output: classification + reasoning.'
      prompt: 'Configure AI step that classifies each matched post: intent_type (active-shopping / brand-mention / complaint / general-discussion), sentiment (positive / neutral / negative), urgency (immediate / browsing / casual), and ''is this post a good place to respond authentically?'' (avoid posts where commercial response would be off-topic / against community norms / clearly hostile). Output: classification + reasoning.'
    - step: 6
      title: Multi-Split by Classification
      command: configure_workflow_multi_split_step
      produces: step
      bindsAs: split
      dependsOn:
      - workflow
      - classify
      description: 'Configure multi-split: ACTIVE-SHOPPING + good-response-fit → SDR/AE task with link to engage authentically (humans only — never auto-reply); BRAND-MENTION (any sentiment) → log to marketing dashboard, Slack alert if negative; COMPLAINT-MENTIONING-YOU → urgent CX task; GENERAL-DISCUSSION → archive (just data for trend tracking).'
      prompt: 'Configure multi-split: ACTIVE-SHOPPING + good-response-fit → SDR/AE task with link to engage authentically (humans only — never auto-reply); BRAND-MENTION (any sentiment) → log to marketing dashboard, Slack alert if negative; COMPLAINT-MENTIONING-YOU → urgent CX task; GENERAL-DISCUSSION → archive (just data for trend tracking).'
    - step: 7
      title: Create Outreach Task
      command: configure_create_task_step
      produces: step
      bindsAs: task
      dependsOn:
      - workflow
      - split
      description: 'On active-shopping branch: create SDR/AE task with the post link, full text, AI classification, suggested response approach (''engage authentically with a helpful answer, then mention our product only if relevant — strict no-spam discipline''). Critical: tasks instruct humans to reply, not automation — automated community replies trigger spam-bans fast.'
      prompt: 'On active-shopping branch: create SDR/AE task with the post link, full text, AI classification, suggested response approach (''engage authentically with a helpful answer, then mention our product only if relevant — strict no-spam discipline''). Critical: tasks instruct humans to reply, not automation — automated community replies trigger spam-bans fast.'
    - step: 8
      title: Slack Alert for Brand Mentions
      command: configure_slack_step
      produces: step
      bindsAs: slack
      dependsOn:
      - workflow
      - split
      description: 'Configure Slack step on brand-mention branch: post to #community-mentions channel with the mention, sentiment, and link. Surfaces real-time brand-pulse for marketing + product. Special handling for negative mentions: tag CX lead.'
      prompt: 'Configure Slack step on brand-mention branch: post to #community-mentions channel with the mention, sentiment, and link. Surfaces real-time brand-pulse for marketing + product. Special handling for negative mentions: tag CX lead.'
    - step: 9
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - task
      - slack
      description: 'Validate and publish. Monitor: post-volume per source per week, intent-detection precision (sample human-rate the AI classifications), conversion from community-engagement-task to meeting (community-sourced leads typically convert higher when handled authentically). Critical guardrail: zero auto-replies — community trust requires humans.'
      prompt: 'Validate and publish. Monitor: post-volume per source per week, intent-detection precision (sample human-rate the AI classifications), conversion from community-engagement-task to meeting (community-sourced leads typically convert higher when handled authentically). Critical guardrail: zero auto-replies — community trust requires humans.'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Community Mention Listening Workflow

## Procedure

1. **Build the Listening Workflow** [`create_workflow`] — Create a workflow 'Community mention listening' that monitors public discussion surfaces (configured subreddits, Hacker News, Indie Hackers, G2/Capterra reviews, X/Twitter mentions) for trigger phrases relevant to the product category. Goal: catch in-market intent at the moment it surfaces publicly, when speed-to-helpful-response converts. → produces: workflow
2. **Scheduled Polling Trigger** [`configure_workflow_wait_until_step`] — Configure scheduled trigger: poll every 30 minutes during business hours (cheap enough to be near-real-time, expensive enough to respect rate limits). Track last-checked-timestamp per source so only new posts are processed. → produces: step
3. **Scrape Configured Sources** [`configure_web_scrape_step`] — Configure web scrape step for the configured list of community sources (subreddits like r/saas / r/CRM / r/marketing depending on workspace; specific forums; review sites). Use RSS where available (faster, lower-stakes scraping). Output: list of new posts/comments since last check, with author/timestamp/text/source. → produces: step
4. **Filter by Trigger Phrases** [`configure_workflow_branch_step`] — Configure branch step: scan posts for trigger phrases (configurable). Active-intent triggers: 'looking for', 'recommend', 'alternative to [competitor]', 'best tool for'. Brand-mention triggers: '[your product name]' (positive/negative/neutral). Skip posts matching neither (most of them). Continues only with matching posts. → produces: step
5. **AI Classify Intent and Sentiment** [`configure_ai_research_step`] — Configure AI step that classifies each matched post: intent_type (active-shopping / brand-mention / complaint / general-discussion), sentiment (positive / neutral / negative), urgency (immediate / browsing / casual), and 'is this post a good place to respond authentically?' (avoid posts where commercial response would be off-topic / against community norms / clearly hostile). Output: classification + reasoning. → produces: step
6. **Multi-Split by Classification** [`configure_workflow_multi_split_step`] — Configure multi-split: ACTIVE-SHOPPING + good-response-fit → SDR/AE task with link to engage authentically (humans only — never auto-reply); BRAND-MENTION (any sentiment) → log to marketing dashboard, Slack alert if negative; COMPLAINT-MENTIONING-YOU → urgent CX task; GENERAL-DISCUSSION → archive (just data for trend tracking). → produces: step
7. **Create Outreach Task** [`configure_create_task_step`] — On active-shopping branch: create SDR/AE task with the post link, full text, AI classification, suggested response approach ('engage authentically with a helpful answer, then mention our product only if relevant — strict no-spam discipline'). Critical: tasks instruct humans to reply, not automation — automated community replies trigger spam-bans fast. → produces: step
8. **Slack Alert for Brand Mentions** [`configure_slack_step`] — Configure Slack step on brand-mention branch: post to #community-mentions channel with the mention, sentiment, and link. Surfaces real-time brand-pulse for marketing + product. Special handling for negative mentions: tag CX lead. → produces: step
9. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: post-volume per source per week, intent-detection precision (sample human-rate the AI classifications), conversion from community-engagement-task to meeting (community-sourced leads typically convert higher when handled authentically). Critical guardrail: zero auto-replies — community trust requires humans. → produces: workflow
