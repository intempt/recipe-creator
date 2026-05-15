---
name: funding-event-triggered-outreach
description: Use when a user mentions "funding event triggered outreach", "funding signal workflow", "newly-funded prospect outreach", or asks for related help. When an account in your CRM raises new funding (detected via web monitoring or webhook from a signal provider), enrich the account, identify newly-empowered decision-makers, AI-draft a congratulatory outreach with budget angle, and create an AE task. Signal-qualified prospecting drives 4-7x higher conversion than cold.
arguments: []
intempt:
  id: funding-event-triggered-outreach
  version: 1.0.0
  slashCommand: /funding-event-triggered-outreach
  group: Workflows
  shortDescription: "When an account in your CRM raises new funding (detected via web monitoring or webhook from a signal provider), enrich the account, identify newly-empowered decision-makers, AI-draft a congratulatory outreach with budget angle, and create an AE task. Signal-qualified prospecting drives 4-7x higher conversion than cold."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [sales]
    agent: workflow-builder
    mode: [b2b]
    complexity: advanced
    executionMode: live
    tags: [signal-triggered, funding-event, intent-data]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: true
  prerequisites:
    events:
      - { value: external_signal_received, severity: blocking }
  invokesCommands:
    - create_workflow
    - configure_webhook_step
    - configure_find_records_step
    - configure_enrich_step
    - configure_write_with_ai_step
    - configure_create_task_step
    - configure_slack_step
    - publish_workflow
  procedure:
    - step: 1
      title: Build the Funding-Signal Workflow
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      description: 'Create a workflow ''Funding-event-triggered outreach'' triggered by webhook from a signal provider (Crunchbase, PitchBook, or scraped TechCrunch RSS) OR by a scheduled scrape of funding news for target-account domains. Goal: be among the first to reach out post-funding when budget is fresh and growth-investment mood is high.'
      prompt: 'Create a workflow ''Funding-event-triggered outreach'' triggered by webhook from a signal provider (Crunchbase, PitchBook, or scraped TechCrunch RSS) OR by a scheduled scrape of funding news for target-account domains. Goal: be among the first to reach out post-funding when budget is fresh and growth-investment mood is high.'
    - step: 2
      title: Webhook Trigger Setup
      command: configure_webhook_step
      produces: step
      bindsAs: webhook
      dependsOn:
      - workflow
      description: 'Configure the webhook trigger to receive funding-event payloads from external sources. Expected payload: company_domain, round_type (seed/A/B/C/etc), amount_raised, investors, announcement_date. Validate payload schema; reject malformed events.'
      prompt: 'Configure the webhook trigger to receive funding-event payloads from external sources. Expected payload: company_domain, round_type (seed/A/B/C/etc), amount_raised, investors, announcement_date. Validate payload schema; reject malformed events.'
    - step: 3
      title: Match to Existing Account or Create New
      command: configure_find_records_step
      produces: step
      bindsAs: match
      dependsOn:
      - workflow
      - webhook
      description: Configure find-records step that matches the funding-event company_domain to an existing Account in the CRM. If match exists, proceed with that account (existing pipeline / customer / prospect). If no match, create a new Account record with the funding context attached so SDR/AE knows where this came from.
      prompt: Configure find-records step that matches the funding-event company_domain to an existing Account in the CRM. If match exists, proceed with that account (existing pipeline / customer / prospect). If no match, create a new Account record with the funding context attached so SDR/AE knows where this came from.
    - step: 4
      title: Refresh Account Enrichment
      command: configure_enrich_step
      produces: step
      bindsAs: enrich
      dependsOn:
      - workflow
      - match
      description: Re-enrich the account post-funding — funding rounds frequently coincide with new exec hires, expanded headcount, new initiatives. Pull latest decision-makers, team size, recent hires. Funding announcements often trigger immediate org changes; the account data on file is now stale.
      prompt: Re-enrich the account post-funding — funding rounds frequently coincide with new exec hires, expanded headcount, new initiatives. Pull latest decision-makers, team size, recent hires. Funding announcements often trigger immediate org changes; the account data on file is now stale.
    - step: 5
      title: AI-Draft Funding-Context Outreach
      command: configure_write_with_ai_step
      produces: step
      bindsAs: draft
      dependsOn:
      - workflow
      - enrich
      description: Configure AI write step that drafts a personalized outreach email/message referencing the specific funding event ('Congrats on the Series B — your investors include [name], which suggests focus on [inference about strategy]'), then connecting to a relevant value hypothesis ('Teams raising at this stage typically face X challenge — we help with that'), then a soft meeting CTA. Draft saved to the AE task; never auto-sent — funding events deserve human review before reaching out.
      prompt: Configure AI write step that drafts a personalized outreach email/message referencing the specific funding event ('Congrats on the Series B — your investors include [name], which suggests focus on [inference about strategy]'), then connecting to a relevant value hypothesis ('Teams raising at this stage typically face X challenge — we help with that'), then a soft meeting CTA. Draft saved to the AE task; never auto-sent — funding events deserve human review before reaching out.
    - step: 6
      title: Create High-Priority AE Task
      command: configure_create_task_step
      produces: step
      bindsAs: task
      dependsOn:
      - workflow
      - enrich
      - draft
      description: 'Configure task creation: assign to the right AE (territory rules, account ownership, or round-robin if unassigned). Task priority: HIGH (funding signals decay fast — within 14 days is golden). Task body: structured brief with funding context, refreshed account data, AI-drafted outreach, suggested meeting times. SLA: AE outreach within 24 hours of funding announcement.'
      prompt: 'Configure task creation: assign to the right AE (territory rules, account ownership, or round-robin if unassigned). Task priority: HIGH (funding signals decay fast — within 14 days is golden). Task body: structured brief with funding context, refreshed account data, AI-drafted outreach, suggested meeting times. SLA: AE outreach within 24 hours of funding announcement.'
    - step: 7
      title: Slack Alert to Sales Channel
      command: configure_slack_step
      produces: step
      bindsAs: slack
      dependsOn:
      - workflow
      - task
      description: 'Configure Slack step posting to the #sales-signals channel: ''🚀 [Account] raised [amount] [round]. Assigned to [AE name]. Outreach SLA: 24hr.'' Includes link to the task and account record. Surfaces the signal velocity for the team — funding events visible to everyone create healthy competitive urgency.'
      prompt: 'Configure Slack step posting to the #sales-signals channel: ''🚀 [Account] raised [amount] [round]. Assigned to [AE name]. Outreach SLA: 24hr.'' Includes link to the task and account record. Surfaces the signal velocity for the team — funding events visible to everyone create healthy competitive urgency.'
    - step: 8
      title: Validate and Publish
      command: publish_workflow
      produces: workflow
      bindsAs: published
      dependsOn:
      - workflow
      - slack
      description: 'Validate and publish. Monitor: AE response SLA, funding-event-to-meeting-booked rate, funding-event-to-deal-closed rate. The benchmark to beat: 4-7x higher conversion vs. unsignaled cold outreach (per Landbase research).'
      prompt: 'Validate and publish. Monitor: AE response SLA, funding-event-to-meeting-booked rate, funding-event-to-deal-closed rate. The benchmark to beat: 4-7x higher conversion vs. unsignaled cold outreach (per Landbase research).'
  outputs:
    - { name: workflow, type: workflow, cardinality: single, description: "Workflow produced by this recipe." }
    - { name: step, type: step, cardinality: multiple, description: "Workflow Step produced by this recipe." }
---

# Funding Event Triggered Outreach

## Procedure

1. **Build the Funding-Signal Workflow** [`create_workflow`] — Create a workflow 'Funding-event-triggered outreach' triggered by webhook from a signal provider (Crunchbase, PitchBook, or scraped TechCrunch RSS) OR by a scheduled scrape of funding news for target-account domains. Goal: be among the first to reach out post-funding when budget is fresh and growth-investment mood is high. → produces: workflow
2. **Webhook Trigger Setup** [`configure_webhook_step`] — Configure the webhook trigger to receive funding-event payloads from external sources. Expected payload: company_domain, round_type (seed/A/B/C/etc), amount_raised, investors, announcement_date. Validate payload schema; reject malformed events. → produces: step
3. **Match to Existing Account or Create New** [`configure_find_records_step`] — Configure find-records step that matches the funding-event company_domain to an existing Account in the CRM. If match exists, proceed with that account (existing pipeline / customer / prospect). If no match, create a new Account record with the funding context attached so SDR/AE knows where this came from. → produces: step
4. **Refresh Account Enrichment** [`configure_enrich_step`] — Re-enrich the account post-funding — funding rounds frequently coincide with new exec hires, expanded headcount, new initiatives. Pull latest decision-makers, team size, recent hires. Funding announcements often trigger immediate org changes; the account data on file is now stale. → produces: step
5. **AI-Draft Funding-Context Outreach** [`configure_write_with_ai_step`] — Configure AI write step that drafts a personalized outreach email/message referencing the specific funding event ('Congrats on the Series B — your investors include [name], which suggests focus on [inference about strategy]'), then connecting to a relevant value hypothesis ('Teams raising at this stage typically face X challenge — we help with that'), then a soft meeting CTA. Draft saved to the AE task; never auto-sent — funding events deserve human review before reaching out. → produces: step
6. **Create High-Priority AE Task** [`configure_create_task_step`] — Configure task creation: assign to the right AE (territory rules, account ownership, or round-robin if unassigned). Task priority: HIGH (funding signals decay fast — within 14 days is golden). Task body: structured brief with funding context, refreshed account data, AI-drafted outreach, suggested meeting times. SLA: AE outreach within 24 hours of funding announcement. → produces: step
7. **Slack Alert to Sales Channel** [`configure_slack_step`] — Configure Slack step posting to the #sales-signals channel: '🚀 [Account] raised [amount] [round]. Assigned to [AE name]. Outreach SLA: 24hr.' Includes link to the task and account record. Surfaces the signal velocity for the team — funding events visible to everyone create healthy competitive urgency. → produces: step
8. **Validate and Publish** [`publish_workflow`] — Validate and publish. Monitor: AE response SLA, funding-event-to-meeting-booked rate, funding-event-to-deal-closed rate. The benchmark to beat: 4-7x higher conversion vs. unsignaled cold outreach (per Landbase research). → produces: workflow
