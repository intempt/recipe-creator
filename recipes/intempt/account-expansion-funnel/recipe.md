---
frontmatter_id: account-expansion-funnel
slash_command: /account-expansion-funnel
description: Lists accounts that started an upgrade but did not finish, and emails a weekly digest of where accounts drop
  off between viewing pricing and upgrading, by starting plan, with bottleneck and slow-step flags.
author:
  name: Intempt
  last_name: Technologies
  company: Intempt
  org_name: intempt
classification:
  industry:
  - industry-agnostic
portable:
  summary: Builds a segment of accounts stalled on the way to an upgrade and emails a weekly digest of drop-off from pricing
    view to upgrade, by starting plan.
  parameters:
  - name: conversionWindow
    type: duration
    label: Window an account has to go from pricing view to upgrade
    default: 30 d
    required: false
  - name: slowStepThreshold
    type: duration
    label: Median step time that flags a slow step
    default: 7 d
    required: false
  - name: pricingPageUrlContains
    type: string
    label: Text in the pricing page URL
    default: /pricing
    required: false
  - name: upgradeCtaPattern
    type: string
    label: Text in the upgrade button id
    default: upgrade
    required: false
  - name: digest_recipients
    type: string
    label: Email addresses that get the digest
    required: true
  requirements:
  - slot: page_view_event
    kind: event
    meaning: A customer viewed a web page
    properties:
    - name: page_url
      type: string
      meaning: URL of the page
      optional: false
  - slot: click_event
    kind: event
    meaning: A customer clicked an element on the page
    properties:
    - name: target_id
      type: string
      meaning: Id of the clicked element
      optional: false
  - slot: checkout_created_event
    kind: event
    meaning: A customer created a checkout session
  - slot: subscription_updated_event
    kind: event
    meaning: A customer's subscription was updated to a higher plan
    properties:
    - name: plan_items
      type: string
      meaning: The plan after the update
      optional: false
  - slot: subscription_started_plan_attribute
    kind: attribute
    meaning: The plan a customer's subscription started on
  steps:
  - id: s1
    builds: segment
    uses:
    - click_event
    - checkout_created_event
    - subscription_updated_event
    - upgradeCtaPattern
    - conversionWindow
    instruction: Build a new segment of accounts named "Stalled Upgrade Accounts". An account is in it when the users in the
      account together did {checkout_created_event}, or {click_event} with {click_event.target_id} containing "{upgradeCtaPattern}",
      in the last {conversionWindow}, and none of its users did {subscription_updated_event} in the last {conversionWindow}.
  - id: s2
    builds: automation
    uses:
    - s1
    - page_view_event
    - click_event
    - checkout_created_event
    - subscription_updated_event
    - subscription_started_plan_attribute
    - conversionWindow
    - slowStepThreshold
    - pricingPageUrlContains
    - upgradeCtaPattern
    - digest_recipients
    dependsOn:
    - s1
    instruction: 'Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts through
      four steps in order, each within {conversionWindow} of the first: viewed pricing ({page_view_event} with {page_view_event.page_url}
      containing "{pricingPageUrlContains}"); clicked upgrade ({click_event} with {click_event.target_id} containing "{upgradeCtaPattern}");
      started checkout ({checkout_created_event}); upgraded ({subscription_updated_event}). It writes these figures for the
      last {conversionWindow} and the {conversionWindow} before: accounts at each step and conversion from step to step; the
      same split by {subscription_started_plan_attribute}; median days between steps; the step with the largest drop-off,
      named as the bottleneck; any step whose median time is over {slowStepThreshold}, named as slow; the number of accounts
      in the segment from "Find accounts stalled before upgrading". Then it emails these figures as plain-text lines, each
      with its window, to {digest_recipients}. Nothing else is sent.'
---

# Account expansion funnel

Slash command: /account-expansion-funnel

## Step 1: Find accounts stalled before upgrading

Build a new segment of accounts named "Stalled Upgrade Accounts". An account is in it when the users in the account together did checkout created event, or click event with target id containing "upgrade", in the last 30 d, and none of its users did subscription updated event in the last 30 d.

## Step 2: Chart the path to an upgrade

Build an automation that runs every Monday at 08:00 on a schedule. Each run it analyzes accounts through four steps in order, each within 30 d of the first: viewed pricing (page view event with page url containing "/pricing"); clicked upgrade (click event with target id containing "upgrade"); started checkout (checkout created event); upgraded (subscription updated event). It writes these figures for the last 30 d and the 30 d before: accounts at each step and conversion from step to step; the same split by subscription started plan attribute; median days between steps; the step with the largest drop-off, named as the bottleneck; any step whose median time is over 7 d, named as slow; the number of accounts in the segment from "Find accounts stalled before upgrading". Then it emails these figures as plain-text lines, each with its window, to the email addresses that get the digest. Nothing else is sent.
