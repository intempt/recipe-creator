---
frontmatter_id: abm-account-personalization
author:
  name: Intempt
  last_name: Technologies
  org_name: intempt
---
# Named-account homepage hero

## Step 1: Set up the account variants

Create a website personalization titled "ABM Account Personalization" on the homepage and on the pricing and demo pages. This personalization is audience-driven, not randomly split: each variant binds to a firmographic audience, and a visitor sees the variant matching their identified account, or the Control if their account has not been identified or does not match any audience.
Variants:
- Control: the standard homepage hero, shown to visitors whose account is not identified or does not match another variant's audience.
- Variant B: shown to visitors from accounts where the account's industry is Enterprise SaaS and employee count is more than 1000. The hero states that the product is built for SaaS companies at this scale and names the account by its company name, read from the matched account record.
- Variant C: shown to visitors from accounts where the account's industry is Banking, Financial Services or Insurance and employee count is more than 500. The hero leads with the product's compliance posture, specifically SOC 2 and PCI DSS, and names the account by its company name.
- Variant D: shown to visitors from accounts where the account's industry is Healthcare, Health Tech or Medical Devices and employee count is more than 100. The hero leads with the product's HIPAA posture and names the account by its company name.
Targeting: homepage, pricing and demo pages; any device; always shown within the targeting rules above.
Metrics: the demo-request form submission rate per audience; the primary call-to-action click rate per audience; and account-level page-view count within the targeting window, to see whether personalized accounts engage more broadly across the site.
Schedule: continuous.

## Step 2: Measure engagement by audience

Compose a dashboard titled "ABM Personalization Performance" showing, for each of the three audiences and the Control: the demo-request submission rate, the primary call-to-action click rate, and the account-level page-view count, each compared week over week. Flag any audience whose demo-request rate is below the Control's rate for 2 consecutive weeks, since that audience's hero is underperforming the generic one. Use the result of "Set up the account variants".

## Step 3: Route engaged accounts to sales

Build a workflow triggered when an identified account from Variant B, C or D submits the demo-request form or exceeds 5 page views within a session. Create a task for the account's assigned account executive, or for the sales development queue when no account executive is yet assigned, naming which audience the account matched and the pages it viewed. Use the result of "Set up the account variants", "Measure engagement by audience".
