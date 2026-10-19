---
frontmatter_id: hubspot-pql-to-deal
slash_command: /hubspot-pql-to-deal
description: Update a HubSpot property, add a contact to a list, or create a HubSpot task when product usage signals readiness, so HubSpot reflects product evidence.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
---

# Product qualified signal to a HubSpot deal

Slash command: /hubspot-pql-to-deal

## Step 1: Define what ready to buy means

Create the segment describing the product-qualified account: the usage that means someone is ready to buy, agreed once and reused.

## Step 2: Open the deal, leave the rest

Create a workflow that creates a HubSpot deal for each qualifying account, matched on a key so a second signal updates the deal instead of opening a duplicate. Set only the fields Intempt owns (source, the signal that triggered it, the score) and leave stage and amount to the rep. Use the result of "Define what ready to buy means".
