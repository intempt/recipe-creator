---
frontmatter_id: salesforce-segment-to-campaign
slash_command: /salesforce-segment-to-campaign
description: Adds each member of a chosen segment to a Salesforce campaign, which is how an audience built here becomes something
  a sales team can run against.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
prerequisites:
  integrations:
    - { value: salesforce, severity: blocking }
portable:
  summary: Adds every member of a segment you choose to a Salesforce campaign, once each, so sales works the same audience.
  parameters:
  - name: campaign_member_status
    type: string
    label: Campaign member status given to added members
    default: Sent
    required: false
  requirements:
  - slot: audience_source
    kind: segment
    meaning: The existing segment whose members belong in the Salesforce campaign
  - slot: salesforce_account
    kind: integration
    channel: salesforce
    meaning: A connected Salesforce account with access to the target campaign
  - slot: target_campaign
    kind: destination
    channel: salesforce
    meaning: The Salesforce campaign that segment members are added to
  steps:
  - id: s1
    builds: automation
    uses:
    - audience_source
    - salesforce_account
    - target_campaign
    - campaign_member_status
    instruction: Build an automation that starts when a user enters the segment {audience_source} and adds that user to {target_campaign}
      in {salesforce_account} with campaign member status {campaign_member_status}. A user already in the campaign is left
      as is, never added twice. Users who leave the segment are not removed from the campaign.
---

# Segment into a Salesforce campaign

Slash command: /salesforce-segment-to-campaign

## Step 1: Add members without doubling

Build an automation that starts when a user enters the segment audience source and adds that user to target campaign in salesforce account with campaign member status Sent. A user already in the campaign is left as is, never added twice. Users who leave the segment are not removed from the campaign.
