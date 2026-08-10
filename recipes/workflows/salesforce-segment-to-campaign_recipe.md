---
name: salesforce-segment-to-campaign
description: Use when a user mentions "segment to salesforce campaign", "add leads to campaign", "campaign membership from segment", or asks for related help. Add a segment's members to a Salesforce campaign, which is how a CDP audience becomes something a sales team can actually run against.
arguments: []
intempt:
  id: salesforce-segment-to-campaign
  version: 1.0.0
  slashCommand: /salesforce-segment-to-campaign
  group: Workflows
  shortDescription: "Add a segment's members to a Salesforce campaign, which is how a CDP audience becomes something a sales team can actually run against."
  author: { type: intempt, name: "Intempt" }
  classification:
    product: [marketing]
    agent: revops-automator
    mode: [b2b]
    complexity: standard
    executionMode: live
    tags: [salesforce, campaign, audience-activation]
  scope: global
  visibility: published
  accessTier: free
  aiPassRequired: false
  prerequisites:
    integrations:
      - { value: salesforce, severity: blocking }
  invokesCommands:
    - create_segment
    - create_workflow
  procedure:
    - step: 1
      title: Define The Audience
      command: create_segment
      produces: segment
      bindsAs: audience
      description: 'Create the segment whose members belong in the campaign. Keep the definition here rather than duplicating it in Salesforce, so there is one answer to who is in the audience.'
      prompt: 'Create the segment whose members belong in the campaign. Keep the definition here rather than duplicating it in Salesforce, so there is one answer to who is in the audience.'
    - step: 2
      title: Add Them To The Campaign
      command: create_workflow
      produces: workflow
      bindsAs: workflow
      dependsOn:
      - audience
      description: 'Create a workflow that adds each member to the named Salesforce campaign with a campaign member status. Adding is idempotent — a member already in the campaign is left alone rather than duplicated — and removal is deliberately not part of this recipe, because campaign membership is a record of who was contacted and deleting it destroys attribution.'
      prompt: 'Create a workflow that adds each member to the named Salesforce campaign with a campaign member status. Adding is idempotent — a member already in the campaign is left alone rather than duplicated — and removal is deliberately not part of this recipe, because campaign membership is a record of who was contacted and deleting it destroys attribution.'
---
