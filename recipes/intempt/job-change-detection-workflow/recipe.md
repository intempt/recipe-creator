---
id: job-change-detection-workflow
title: Follow a champion who moves
slash_command: /job-change-detection-workflow
group: Workflows
owner: intempt
curator: trishik
summary: >-
  Given a known contact job change, routes two task plays: an AE task to protect the old account and an SDR
  task to pursue the new account.
description: >-
  Buildable with workflow routing and tasks. When a contact job change is known, branch into two plays: (a) AE
  task to re-establish at the old account and identify a replacement, (b) SDR task to pursue at the new
  account. It does not detect job changes or scrape LinkedIn.
version: 2.0.0
classification:
  product:
    - sales
  agent: workflow-builder
  mode:
    - b2b
  complexity: advanced
  executionMode: live
  tags:
    - signal-triggered
    - job-change
    - champion-tracking
prerequisites:
  events:
    - value: external_signal_received
      severity: blocking
touches:
  reads:
    - The external_signal_received event in your project
  writes:
    - A new workflow, from step 1 "Run both plays on a move"
    - A new workflow, from step 2 "Scan champions every Monday"
    - A new workflow, from step 3 "Refresh where they work"
    - A new workflow, from step 4 "Split by kind of account"
    - A new workflow, from step 5 "Find who replaces them"
    - A new workflow, from step 6 "Tell the CSM or AE to act"
    - A new workflow, from step 7 "Check if we know the new firm"
    - A new workflow, from step 8 "Chase them at the new place"
    - A new workflow, from step 9 "Publish and track both sides"
  never:
    - Nothing runs until you approve the plan in Blu.
steps:
  - id: s1
    title: Run both plays on a move
    summary: >-
      Triggered when a contact at a customer or open deal account changes employer, picked up by a scheduled
      enrichment refresh or a signal provider. It splits into two parallel plays: protect the old account,
      pursue the new one.
    builds: workflow
    description: >-
      Create a workflow 'Job-change detection and dual response' triggered when a contact at an existing
      customer/deal account changes employer (detected via scheduled enrichment refresh OR signal provider
      webhook). Branches into two parallel plays: protect the old account, pursue the new account.
  - id: s2
    title: Scan champions every Monday
    summary: >-
      Weekly, it goes through every contact marked champion or economic buyer on an active deal or a customer
      account. That cadence is the engine behind the whole workflow.
    builds: workflow
    description: >-
      Configure scheduled trigger: every Monday morning, scan all contacts marked as 'champion' or 'economic
      buyer' on active deals + customer accounts. The job-change-detection cadence is the key infrastructure
      for this workflow. Use the result of "Run both plays on a move".
    dependsOn:
      - s1
  - id: s3
    title: Refresh where they work
    summary: >-
      Employment data is refreshed for the tracked contacts, and most providers flag it when the mapping
      between an email domain and a company changes. The output is the list of people whose company has
      changed since the last run.
    builds: workflow
    description: >-
      Configure enrich step that refreshes employment data for tracked contacts. Most providers (Clearbit,
      Apollo, LinkedIn-feeds) flag when an email-domain to company mapping changes: that's the signal.
      Output: list of contacts whose company changed since last refresh. Use the result of "Run both plays
      on a move", "Scan champions every Monday".
    dependsOn:
      - s1
      - s2
  - id: s4
    title: Split by kind of account
    summary: >-
      A customer account goes to the departure rescue, an open deal to urgent multi threading, and a prospect
      to a warm follow at the new company.
    builds: workflow
    description: >-
      Branch: was the contact at a CUSTOMER account, OPEN-DEAL account, or PROSPECT account? Each gets
      different downstream treatment. Customer to champion-departure rescue. Open-deal to urgent multi-threading.
      Prospect to warm-follow at new company. Use the result of "Run both plays on a move", "Refresh where
      they work".
    dependsOn:
      - s1
      - s3
  - id: s5
    title: Find who replaces them
    summary: >-
      On the customer and deal branches, the old company's leadership page and public search are read
      for two or three likely replacements in similar roles, with titles and inferred contact details,
      so the rep does not have to hunt.
    builds: workflow
    description: >-
      AI research step on the customer/deal branch: scrape the old company's leadership page + LinkedIn-via-public-search
      to identify likely replacement decision-makers in similar roles. Outputs 2-3 candidate names with
      titles and inferred contact info. Saves AE the manual hunt. Use the result of "Run both plays on
      a move", "Split by kind of account".
    dependsOn:
      - s1
      - s4
  - id: s6
    title: Tell the CSM or AE to act
    summary: >-
      An urgent task naming who left, where they went and the replacement candidates, suggesting a warm
      introduction through the departed champion if the relationship was good and cold outreach to the
      replacement if it was not. Contact within five working days, because deals without a champion stall
      fast.
    builds: workflow
    description: >-
      Create urgent task for the assigned CSM (customer) or AE (open deal): 'Your champion [Name] just
      left for [New Company]. Replacement candidates identified: [list]. Suggested action: warm intro
      through [Departed champion] if relationship is good, else cold outreach to replacement.' SLA: contact
      within 5 business days: champion-gone deals stall fast. Use the result of "Run both plays on a move",
      "Find who replaces them".
    dependsOn:
      - s1
      - s5
  - id: s7
    title: Check if we know the new firm
    summary: >-
      If their new employer is already an account, the contact is linked and the relationship surfaced
      to the AE. If not, an account and contact are created, flagged as a warm signal because a champion
      from an existing customer now works there.
    builds: workflow
    description: >-
      Find-records step on the departed-to-new-company branch: is the new company already in our CRM?
      If yes (link the contact, surface the relationship to the assigned AE. If no) create new Account
      + contact record with 'warm signal: ex-customer champion now here' flag. Use the result of "Run
      both plays on a move", "Split by kind of account".
    dependsOn:
      - s1
      - s4
  - id: s8
    title: Chase them at the new place
    summary: >-
      An SDR task explaining the connection and suggesting they congratulate the move and ask whether
      the same approach would help in the new role. High priority, because warm signals decay within about
      30 days.
    builds: workflow
    description: >-
      Create SDR task for the new-company outreach: 'Warm signal: [Champion name] (your ally at [Old company])
      just joined [New company]. Suggested outreach: congratulate the move, ask if they could use the
      same approach at their new role.' Priority: HIGH (warm signals decay; reach out within 30 days of
      job change). Use the result of "Run both plays on a move", "Check if we know the new firm".
    dependsOn:
      - s1
      - s7
  - id: s9
    title: Publish and track both sides
    summary: >-
      Validated and published, tracking job changes detected each quarter, how many of the affected deals
      avoid stalling, and how many pursuits at the new company turn into meetings.
    builds: workflow
    description: >-
      Validate and publish. Monitor: job-change detection volume per quarter, old-account-save rate (champion-departure
      deals that DIDN'T stall), new-account-conversion rate (departed-champion pursuits that became meetings).
      These are some of the highest-quality signals in B2B. Use the result of "Run both plays on a move",
      "Tell the CSM or AE to act", "Chase them at the new place".
    dependsOn:
      - s1
      - s6
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

# Follow a champion who moves

Given a known contact job change, routes two task plays: an AE task to protect the old account and an SDR task to pursue the new account.

## Steps

1. **Run both plays on a move** (builds workflow)

   Triggered when a contact at a customer or open deal account changes employer, picked up by a scheduled enrichment refresh or a signal provider. It splits into two parallel plays: protect the old account, pursue the new one.

2. **Scan champions every Monday** (builds workflow)

   Weekly, it goes through every contact marked champion or economic buyer on an active deal or a customer account. That cadence is the engine behind the whole workflow.

3. **Refresh where they work** (builds workflow)

   Employment data is refreshed for the tracked contacts, and most providers flag it when the mapping between an email domain and a company changes. The output is the list of people whose company has changed since the last run.

4. **Split by kind of account** (builds workflow)

   A customer account goes to the departure rescue, an open deal to urgent multi threading, and a prospect to a warm follow at the new company.

5. **Find who replaces them** (builds workflow)

   On the customer and deal branches, the old company's leadership page and public search are read for two or three likely replacements in similar roles, with titles and inferred contact details, so the rep does not have to hunt.

6. **Tell the CSM or AE to act** (builds workflow)

   An urgent task naming who left, where they went and the replacement candidates, suggesting a warm introduction through the departed champion if the relationship was good and cold outreach to the replacement if it was not. Contact within five working days, because deals without a champion stall fast.

7. **Check if we know the new firm** (builds workflow)

   If their new employer is already an account, the contact is linked and the relationship surfaced to the AE. If not, an account and contact are created, flagged as a warm signal because a champion from an existing customer now works there.

8. **Chase them at the new place** (builds workflow)

   An SDR task explaining the connection and suggesting they congratulate the move and ask whether the same approach would help in the new role. High priority, because warm signals decay within about 30 days.

9. **Publish and track both sides** (builds workflow)

   Validated and published, tracking job changes detected each quarter, how many of the affected deals avoid stalling, and how many pursuits at the new company turn into meetings.

## What you end up with

- **workflow** (workflow): Workflow produced by this recipe.
- **step** (step): Workflow Step produced by this recipe.

## What this recipe touches

Reads:

- The external_signal_received event in your project

Writes:

- A new workflow, from step 1 "Run both plays on a move"
- A new workflow, from step 2 "Scan champions every Monday"
- A new workflow, from step 3 "Refresh where they work"
- A new workflow, from step 4 "Split by kind of account"
- A new workflow, from step 5 "Find who replaces them"
- A new workflow, from step 6 "Tell the CSM or AE to act"
- A new workflow, from step 7 "Check if we know the new firm"
- A new workflow, from step 8 "Chase them at the new place"
- A new workflow, from step 9 "Publish and track both sides"

Never:

- Nothing runs until you approve the plan in Blu.

## Availability

Coming soon: waiting on the engine to build workflow.
