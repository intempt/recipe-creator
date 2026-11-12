---
frontmatter_id: salesforce-segment-to-campaign
slash_command: /salesforce-segment-to-campaign
description: Puts a segment's members into a Salesforce campaign, which is how an audience built here becomes something a sales team can run against.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Adds members of a segment to a Salesforce campaign once each, so an audience built here can be worked by the sales
    team without duplicate campaign records.
  parameters:
  - name: campaign_member_status
    type: string
    label: Campaign member status to assign
    default: <UNKNOWN>
    required: true
  - name: audience_name
    type: string
    label: Name for the audience segment
    default: Salesforce campaign audience
    required: false
  requirements:
  - slot: salesforce_account
    kind: integration
    meaning: A connected Salesforce account with access to the target campaign
    channel: salesforce
  - slot: target_campaign
    kind: destination
    meaning: The Salesforce campaign that segment members should be added to
    channel: salesforce
  - slot: audience_source
    kind: segment
    meaning: The audience whose members belong in the Salesforce campaign
    creatable: true
    definition: users who make up the audience to be added to the Salesforce campaign
  steps:
  - id: s1
    builds: segment
    uses:
    - audience_name
    instruction: Create the segment {audience_name} whose members belong in the campaign. Keep the definition here rather
      than duplicating it in Salesforce, so there is one answer to who is in the audience.
  - id: s2
    builds: automation
    uses:
    - s1
    - audience_source
    - target_campaign
    - salesforce_account
    - campaign_member_status
    instruction: 'Create a workflow that adds each member of {audience_source} to {target_campaign} in {salesforce_account}
      with campaign member status {campaign_member_status}. Adding is idempotent: a member already in the campaign is left
      alone rather than duplicated. Removal is not part of this workflow. Use the segment from "Define the audience once".'
---

# Segment into a Salesforce campaign

Slash command: /salesforce-segment-to-campaign

## Step 1: Define the audience once

Create the segment whose members belong in the campaign. Keep the definition here rather than duplicating it in Salesforce, so there is one answer to who is in the audience.

## Step 2: Add members without doubling

Create a workflow that adds each member to the named Salesforce campaign with a campaign member status. Adding is idempotent (a member already in the campaign is left alone rather than duplicated) and removal is deliberately not part of this recipe, because campaign membership is a record of who was contacted and deleting it destroys attribution. Use the result of "Define the audience once".
